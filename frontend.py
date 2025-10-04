import json
import os
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Questionnaire sportif", layout="wide")

st.title("🏅 Questionnaire pour recommandation de sport")
st.write(
    "Réponds aux questions ci-dessous pour que nous puissions analyser ton profil et te recommander un sport adapté."
)

# --- 🏃 Compétences physiques ---
st.header("🏃 Compétences physiques")
endurance = st.slider(
    "Sur une échelle de 1 à 5, comment évalues-tu ton endurance ?", 1, 5, 3
)
vitesse = st.slider(
    "Sur une échelle de 1 à 5, comment évalues-tu ta vitesse ?", 1, 5, 3
)
souplesse = st.slider(
    "Sur une échelle de 1 à 5, comment évalues-tu ta souplesse ?", 1, 5, 3
)
equilibre = st.radio(
    "Arrives-tu facilement à tenir ton équilibre sur une surface instable ?",
    ["Oui", "Non"],
)
explosivite = st.radio(
    "Te considères-tu explosif(ve) dans tes mouvements ?", ["Oui", "Non"]
)
effort_pref = st.selectbox(
    "Quel type d’effort préfères-tu ?",
    [
        "Courir longtemps",
        "Effort court et explosif",
        "Porter/pousser des charges",
        "Mouvements techniques et souplesse",
    ],
)
points_forts_physiques = st.text_area(
    "Quels sont selon toi tes points forts physiques ?"
)

# --- 🧠 Compétences cognitives & mentales ---
st.header("🧠 Compétences cognitives & mentales")
concentration = st.slider(
    "À quel point arrives-tu à rester concentré malgré les distractions ?", 1, 5, 3
)
stress = st.slider("Comment gères-tu ton stress en compétition ?", 1, 5, 3)
decision_rapide = st.radio(
    "Aimes-tu prendre des décisions rapides pendant une action ?", ["Oui", "Non"]
)
anticipation = st.radio(
    "Arrives-tu à anticiper facilement les actions des autres ?", ["Oui", "Non"]
)
reaction_situation = st.selectbox(
    "Face à une situation imprévue, tu es plutôt :",
    ["Bloqué(e)", "Calme", "Réactif(ve)", "Stratégique"],
)
situation_courage = st.text_area(
    "Décris une situation où tu as dû faire preuve de courage ou de persévérance."
)

# --- 🤝 Compétences sociales ---
st.header("🤝 Compétences sociales & relationnelles")
travail_equipe = st.slider(
    "À quel point préfères-tu travailler en équipe plutôt que seul(e) ?", 1, 5, 3
)
motiver_autres = st.slider(
    "Comment évalues-tu ta capacité à motiver les autres ?", 1, 5, 3
)
sport_collectif = st.radio(
    "Préfères-tu les sports collectifs aux sports individuels ?", ["Oui", "Non"]
)
leader = st.radio("Te considères-tu comme un leader dans une équipe ?", ["Oui", "Non"])
role_equipe = st.selectbox(
    "Quand tu joues en équipe, tu es plutôt :",
    [
        "Axé sur la coopération",
        "Axé sur la communication",
        "Leader",
        "Axé sur la performance individuelle",
    ],
)
experience_groupe = st.text_area(
    "Raconte une expérience sportive ou de groupe où tu t’es senti(e) à ta place."
)

# --- 🎯 Compétences techniques ---
st.header("🎯 Compétences techniques spécifiques")
precision = st.slider("Comment évalues-tu ta précision (tir, lancer, passe) ?", 1, 5, 3)
aisance_engin = st.slider(
    "Comment évalues-tu ton aisance avec un engin (raquette, vélo, ski, etc.) ?",
    1,
    5,
    3,
)
eau = st.radio("Es-tu à l’aise dans l’eau ?", ["Oui", "Non"])
combat = st.radio("As-tu déjà pratiqué un sport de combat ?", ["Oui", "Non"])
gestes_techniques = st.multiselect(
    "Parmi ces gestes techniques, lesquels aimerais-tu développer ?",
    [
        "Précision de tir",
        "Dribbles / feintes",
        "Techniques de combat",
        "Nage / respiration",
        "Acrobatie / rotation",
    ],
)
competence_souhaitee = st.text_area(
    "Décris une compétence technique que tu aimerais acquérir."
)

# --- 🌍 Compétences stratégiques ---
st.header("🌍 Compétences stratégiques / environnementales")
energie = st.slider(
    "À quel point sais-tu gérer ton énergie sur un effort long ?", 1, 5, 3
)
orientation = st.slider(
    "Comment évalues-tu ta capacité à t’orienter dans un espace ?", 1, 5, 3
)
adaptation = st.radio(
    "Aimes-tu t’adapter aux conditions extérieures (météo, terrain) ?", ["Oui", "Non"]
)
initiative = st.radio(
    "Prends-tu facilement des initiatives en pleine action ?", ["Oui", "Non"]
)
adapt_env = st.selectbox(
    "Quand tu dois t’adapter à l’environnement, tu préfères :",
    [
        "Jouer avec les conditions",
        "Optimiser ton placement",
        "Gérer ton rythme",
        "Maîtriser ton matériel",
    ],
)
experience_env = st.text_area(
    "Raconte une fois où tu as dû t’adapter rapidement à ton environnement."
)


# --- Bouton validation ---
if st.button("📩 Soumettre mes réponses"):
    # Créer un dictionnaire avec toutes les réponses
    reponses = {
        "endurance": "endurance",
        "vitesse": "vitesse",
        "souplesse": "souplesse",
        "equilibre": "equilibre",
        "explosivite": "explosivite",
        "effort_pref": "effort_pref",
        "points_forts_physiques": "points_forts_physiques",
        "concentration": "concentration",
        "stress": "stress",
        "decision_rapide": "decision_rapide",
        "anticipation": "anticipation",
        "reaction_situation": "reaction_situation",
        "travail_equipe": "travail_equipe",
        "motiver_autres": "motiver_autres",
        "sport_collectif": "sport_collectif",
        "leader": "leader",
        "role_equipe": "role_equipe",
        "experience_groupe": "experience_groupe",
        "precision": "precision",
        "aisance_engin": "aisance_engin",
        "combat": "combat",
        "gestes_techniques": "gestes_techniques",
        "souhaitee": "souhaitee",
        "energie": "energie",
        "orientation": "orientation",
        "adaptation": "adaptation",
        "initiative": "initiative",
        "adapt_env": "adapt_env",
        "experience_env": "experience_env",
    }

    # Vérifier si le fichier existe déjà
    fichier = "reponses.json"
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    # Ajouter les nouvelles réponses
    data.append(reponses)

    # Sauvegarder dans le fichier
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    st.success("✅ Réponses enregistrées avec succès dans reponses.json")
