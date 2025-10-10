import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SportRecommender:
    def __init__(self, sports_file: str = "sports.json"):
        with open(sports_file, "r", encoding="utf-8") as f:
            self.sports_data = json.load(f)["sports"]

    @staticmethod
    def _to_vector(skill_dict, all_skills):
        """Convert dict of skills into a consistent vector."""
        return np.array([skill_dict.get(s, 0) for s in all_skills])

    def recommend(self, user_vector: dict, top_n: int = 3):
        """Return top-N recommended sports based on cosine similarity."""
        skills = list(user_vector.keys())
        user_vec = self._to_vector(user_vector, skills)

        sport_scores = {}
        for sport, sport_vec_dict in self.sports_data.items():
            sport_vec = self._to_vector(sport_vec_dict, skills)
            sim = cosine_similarity([user_vec], [sport_vec])[0][0]
            sport_scores[sport] = round(sim, 3)

        sorted_sports = sorted(sport_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_sports[:top_n]

    def explain(self, user_vector: dict, sport_name: str):
        """Show which skills match or mismatch for a given sport."""
        sport_vec = self.sports_data.get(sport_name)
        if not sport_vec:
            return {}

        diff = {
            s: round(user_vector.get(s, 0) - sport_vec.get(s, 0), 2)
            for s in user_vector
        }
        return diff
