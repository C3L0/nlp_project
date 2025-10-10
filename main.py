import json

import numpy as np


def normalize_by_l2(vec: dict) -> dict:
    """
    Apply L2 normalization to a vector represented as a dict.
    """
    norm = np.sqrt(sum(v**2 for v in vec.values()))
    if norm == 0:
        return vec
    return {k: v / norm for k, v in vec.items()}


def main():
    # Load sports data
    with open("sports.json", "r", encoding="utf-8") as f:
        sports = json.load(f)["sports"]

    # Apply L2 normalization to each sport vector
    sports_l2 = {sport: normalize_by_l2(skills) for sport, skills in sports.items()}

    # Save to a new file
    with open("sports_l2.json", "w", encoding="utf-8") as f:
        json.dump({"sports": sports_l2}, f, indent=4, ensure_ascii=False)

    print("✅ All sport vectors have been L2-normalized and saved to sports_l2.json")


if __name__ == "__main__":
    main()
