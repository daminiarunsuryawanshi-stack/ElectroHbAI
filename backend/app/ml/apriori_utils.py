import json
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent
RULES_PATH = BASE / "rules.json"


def load_rules():
    try:
        return json.loads(RULES_PATH.read_text())
    except FileNotFoundError:
        return []


_rules = load_rules()


def recommend_next(cart_items, top_n=5):
    cart_set = set(cart_items)
    candidates = defaultdict(lambda: {"confidence": 0, "lift": 0, "support": 0})
    for r in _rules:
        if set(r.get("antecedent", [])).issubset(cart_set):
            for item in r.get("consequent", []):
                if item not in cart_set:
                    if r["confidence"] > candidates[item]["confidence"]:
                        candidates[item] = {"confidence": r["confidence"], "lift": r.get("lift", 0), "support": r.get("support", 0)}
    ranked = sorted(((item, v["confidence"], v["lift"], v["support"]) for item, v in candidates.items()), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


def save_rules(records):
    RULES_PATH.write_text(json.dumps(records, indent=2))
