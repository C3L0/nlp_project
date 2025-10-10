import json

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SportRecommender:
    def __init__(self, sports_file: str = "sports_l2.json"):
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

    def top_diff_skills(self, user_vector: dict, sport_name: str, n: int = 6):
        """Return the n skills with the largest absolute differences."""
        diff = self.explain(user_vector, sport_name)
        return dict(sorted(diff.items(), key=lambda x: abs(x[1]), reverse=True)[:n])

    def min_diff_skills(self, user_vector: dict, sport_name: str, n: int = 6):
        """Return the n skills with the smallest absolute differences."""
        diff = self.explain(user_vector, sport_name)
        return dict(sorted(diff.items(), key=lambda x: abs(x[1]))[:n])

    def plot_hexagon(
        self, user_vector: dict, sport_name: str, skills_subset: list = None
    ):
        """
        Display radar chart comparing user vs sport on given skills.
        If skills_subset is None, automatically use the top 6 differing skills.
        """
        sport_vec = self.sports_data.get(sport_name)
        if not sport_vec:
            raise ValueError(f"Sport '{sport_name}' not found.")

        if skills_subset is None:
            skills_subset = list(self.top_diff_skills(user_vector, sport_name).keys())

        user_values = [user_vector.get(s, 0) for s in skills_subset]
        sport_values = [sport_vec.get(s, 0) for s in skills_subset]

        # Repeat first value to close the polygon
        user_values += user_values[:1]
        sport_values += sport_values[:1]

        angles = np.linspace(0, 2 * np.pi, len(skills_subset), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        ax.plot(angles, user_values, linewidth=2, linestyle="solid", label="User")
        ax.fill(angles, user_values, alpha=0.25)

        ax.plot(angles, sport_values, linewidth=2, linestyle="dashed", label=sport_name)
        ax.fill(angles, sport_values, alpha=0.25)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(skills_subset)
        ax.set_title(f"Comparison: You vs {sport_name}", size=14, pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

        plt.tight_layout()
        return fig
