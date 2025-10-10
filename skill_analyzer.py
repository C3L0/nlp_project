import json
import re

import numpy as np
from sentence_transformers import SentenceTransformer, util


class SkillAnalyzer:
    """
    Analyze user answers (semantic and numeric) to produce a unified skill vector.
    """

    def __init__(self, skill_file: str, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

        # Load skill definitions
        with open(skill_file, "r", encoding="utf-8") as f:
            self.skills = json.load(f)

        self.skill_names = list(self.skills.keys())
        self.skill_texts = list(self.skills.values())
        self.skill_embeddings = self.model.encode(
            self.skill_texts, normalize_embeddings=True
        )

    # -------------------- TEXT PREPROCESSING -------------------- #
    @staticmethod
    def split_sentences(text: str):
        return [s.strip() for s in re.split(r"[.!?]+", text.strip()) if s.strip()]

    # -------------------- SEMANTIC ANALYSIS -------------------- #
    def analyze_semantic(self, answer: str) -> dict:
        sentences = self.split_sentences(answer)
        if not sentences:
            return {s: 0.0 for s in self.skill_names}

        skill_scores = np.zeros(len(self.skill_names))
        for sentence in sentences:
            emb = self.model.encode(sentence, normalize_embeddings=True)
            similarities = util.cos_sim(emb, self.skill_embeddings)[0].cpu().numpy()
            skill_scores += similarities

        skill_scores = (skill_scores / len(sentences)) * 10
        return dict(zip(self.skill_names, skill_scores.round(2)))

    # -------------------- NUMERIC ANALYSIS -------------------- #
    def analyze_numeric(self, numeric_answers: list[dict]) -> dict:
        """
        numeric_answers: list of dicts like:
        [
            {"strength": 8, "endurance": 7},
            {"teamwork": 9},
        ]
        """
        aggregated = {s: [] for s in self.skill_names}

        for answer in numeric_answers:
            for skill, score in answer.items():
                if skill in aggregated:
                    aggregated[skill].append(score)

        # Compute averages (or zeros if empty)
        return {
            skill: round(np.mean(scores), 2) if scores else 0.0
            for skill, scores in aggregated.items()
        }

    # -------------------- COMBINE BOTH -------------------- #
    def combine_scores(
        self, semantic_scores: dict, numeric_scores: dict, w_sem=0.6, w_num=0.4
    ) -> dict:
        """
        Combine semantic and numeric scores into a single weighted skill vector.
        You can adjust w_sem and w_num depending on how much weight each should have.
        """
        final_scores = {}
        for skill in self.skill_names:
            sem = semantic_scores.get(skill, 0)
            num = numeric_scores.get(skill, 0)
            final_scores[skill] = round((w_sem * sem + w_num * num), 2)
        return final_scores


analyzer = SkillAnalyzer("skill.json")

# Semantic answer
open_answer = "I enjoy planning strategies and staying consistent in long races."
semantic_scores = analyzer.analyze_semantic(open_answer)

# Numeric answers
numeric_data = [
    {"endurance": 9, "strength": 6},
    {"strategy": 8, "teamwork": 3},
]
numeric_scores = analyzer.analyze_numeric(numeric_data)

# Combine both
user_profile = analyzer.combine_scores(semantic_scores, numeric_scores)

print("Semantic:", semantic_scores)
print("Numeric:", numeric_scores)
print("Final user profile:", user_profile)
