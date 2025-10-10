import json

import streamlit as st

from skill_analyzer import SkillAnalyzer
from sports_recommender import SportRecommender

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# Initialize analyzer
analyzer = SkillAnalyzer("skill.json")

open_answers = []
numeric_data = []

st.title("🏅 Sport Orientation Form")

for q in questions:
    st.markdown(f"### {q['text']}")

    # --- OPEN QUESTION ---
    if q["type"] == "open":
        answer = st.text_area("", key=q["id"])
        if answer:
            open_answers.append(answer)

    # --- LIKERT SCALE ---
    elif q["type"] == "likert":
        val = st.slider(
            "", q["scale"]["min"], q["scale"]["max"], q["scale"]["default"], key=q["id"]
        )
        numeric_data.append(
            {skill: val * weight for skill, weight in q["skills"].items()}
        )

    # --- MULTIPLE CHOICE QUESTION (MCQ) ---
    elif q["type"] == "mcq":
        choice = st.radio("", list(q["options"].keys()), key=q["id"])
        numeric_data.append(q["options"][choice])

    # --- CHECKBOX QUESTION ---
    elif q["type"] == "checkbox":
        selections = st.multiselect("", list(q["options"].keys()), key=q["id"])
        for s in selections:
            numeric_data.append(q["options"][s])

# Once all questions are filled
if st.button("Analyze Results"):
    # Combine open text and numeric answers
    if open_answers:
        semantic_scores = analyzer.analyze_semantic(" ".join(open_answers))
    else:
        semantic_scores = {s: 0.0 for s in analyzer.skill_names}

    numeric_scores = analyzer.analyze_numeric(numeric_data)
    final_profile = analyzer.combine_scores(semantic_scores, numeric_scores)

    st.write("### 🧠 Your Skill Profile")
    st.bar_chart(final_profile)

    # After user answers your form
    analyzer = SkillAnalyzer("skill.json")
    recommender = SportRecommender("sports.json")

    semantic_scores = analyzer.analyze_semantic(" ".join(open_answers))
    numeric_scores = analyzer.analyze_numeric(numeric_data)
    final_profile = analyzer.combine_scores(semantic_scores, numeric_scores)

    # Get sport recommendations
    recommendations = recommender.recommend(final_profile, top_n=3)

    st.write("### 🏆 Best Sports for You")
    for sport, score in recommendations:
        st.write(f"- **{sport}** ({score})")

    # Optional: show comparison for top sport
    top_sport = recommendations[0][0]
    differences = recommender.explain(final_profile, top_sport)
    st.write(f"### Skill Difference vs {top_sport}")
    st.write(differences)
