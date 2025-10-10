import json

import streamlit as st

from skill_analyzer import SkillAnalyzer
from sports_recommender import SportRecommender

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# Initialize analyzer and recommender
analyzer = SkillAnalyzer("skill.json")
recommender = SportRecommender("sports.json")

st.title("🏅 Sport Orientation Form")

# Store answers
answers = {}

# Render questions dynamically
for q in questions:
    qtype = q["type"]

    if qtype == "open":
        answers[q["id"]] = st.text_area(q["text"], key=q["id"])

    elif qtype == "likert":
        scale = q.get("scale", {"min": 1, "max": 10, "default": 5})
        answers[q["id"]] = st.slider(
            q["text"],
            min_value=scale["min"],
            max_value=scale["max"],
            value=scale["default"],
            key=q["id"],
        )

    elif qtype == "mcq":
        options = list(q["options"].keys())
        answers[q["id"]] = st.radio(q["text"], options, key=q["id"])

    elif qtype == "checkbox":
        options = list(q["options"].keys())
        answers[q["id"]] = st.multiselect(q["text"], options, key=q["id"])

# Process results
if st.button("Analyze Results"):
    open_answers = []
    numeric_data = {}

    # Map answers to skills
    for q in questions:
        qid = q["id"]
        qtype = q["type"]

        if qtype == "open":
            if answers[qid].strip():
                open_answers.append(answers[qid])

        elif qtype == "likert":
            for skill, weight in q["skills"].items():
                numeric_data[skill] = numeric_data.get(skill, 0) + answers[qid] * weight

        elif qtype in ["mcq", "checkbox"]:
            selected_options = answers[qid]
            if isinstance(selected_options, str):
                selected_options = [selected_options]  # mcq
            for opt in selected_options:
                for skill, weight in q["options"][opt].items():
                    numeric_data[skill] = numeric_data.get(skill, 0) + weight

    # Semantic analysis
    if open_answers:
        semantic_scores = analyzer.analyze_semantic(" ".join(open_answers))
    else:
        semantic_scores = {s: 0.0 for s in analyzer.skill_names}

    # Numeric analysis
    numeric_scores = analyzer.analyze_numeric(numeric_data)

    # Combine
    final_profile = analyzer.combine_scores(semantic_scores, numeric_scores)

    # Display user skill profile
    st.write("### 🧠 Your Skill Profile")
    st.bar_chart(final_profile)

    # Recommend sports
    recommendations = recommender.recommend(final_profile, top_n=3)

    st.write("### 🏆 Best Sports for You")
    for sport, score in recommendations:
        st.write(f"- **{sport}** ({score})")

    # Show skill differences for top sport
    top_sport = recommendations[0][0]
    differences = recommender.explain(final_profile, top_sport)
    st.write(f"### Skill Difference vs {top_sport}")
    st.write(differences)
