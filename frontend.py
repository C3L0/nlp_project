import json
import streamlit as st

from skill_analyzer import SkillAnalyzer
from sports_recommender import SportRecommender

# Initialisation du state
if "final_profile" not in st.session_state:
    st.session_state.final_profile = None
if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

# Load questions
with open("questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)["questions"]

# Initialize analyzer and recommender
analyzer = SkillAnalyzer("skill.json")
recommender = SportRecommender("sports_l2.json")

st.title("Sport Orientation Form")

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
    st.session_state.final_profile = analyzer.combine_scores(
        semantic_scores, numeric_scores
    )
    st.session_state.recommendations = recommender.recommend(
        st.session_state.final_profile, top_n=3
    )

if st.session_state.final_profile is not None:
    final_profile = st.session_state.final_profile

    # Display user skill profile
    st.write("### Your Skill Profile")
    st.bar_chart(final_profile)

    # Recommend sports
    recommendations = recommender.recommend(final_profile, top_n=3)
    
    # Best sports
    st.write("### Best Sports for You")
    top_sport, top_score = recommendations[0]
    worst_sport, worst_score = recommendations[-1]

    st.write(f"- **{top_sport}** ({top_score})")
    st.write(f"- **{recommendations[1][0]}** ({recommendations[1][1]})")
    st.write(f"- **{recommendations[2][0]}** ({recommendations[2][1]})")

    # Show skill differences for top sport
    top_sport = recommendations[0][0]
    differences = recommender.explain(final_profile, top_sport)
    st.write(f"### Skill Difference vs {top_sport}")
    st.write(differences)

    # Recommend sports
    recommendations = recommender.recommend(
        final_profile, top_n=len(recommender.sports_data)
    )

    st.divider()

    # Show differences for top sport
    st.write(f"## Skill Differences for {top_sport}")

    # Display radar for top sport
    fig_best = recommender.plot_hexagon(final_profile, top_sport)
    st.pyplot(fig_best)

    st.divider()

    # Now show the most distant sport
    st.write(f"## Least Matching Sport: {worst_sport} ({worst_score})")
    fig_worst = recommender.plot_hexagon(final_profile, worst_sport)
    st.pyplot(fig_worst)

    st.divider()

    # Select manually the sport to compare
    sport_names = list(recommender.sports_data.keys())
    selected_sport = st.selectbox(
        "Choisis un sport à comparer avec ton profil :", sport_names
    )

    if selected_sport:
        st.write(f"## Comparaison avec {selected_sport}")

        # Affichage du graphe radar
        fig = recommender.plot_hexagon(final_profile, selected_sport)
        st.pyplot(fig)
