import csv
import json
from pathlib import Path

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules


BASE = Path(__file__).resolve().parent
CSV_PATH = Path.cwd() / "transactions.csv"
OUT_PATH = BASE / "rules.json"


def export_transactions_from_db(path=CSV_PATH):
    # Import models here so SQLAlchemy mappers are registered
    from app.core.database import SessionLocal
    from app.models.order_item import OrderItem
    # Ensure related models are imported so relationship('Order') can be resolved
    from app.models.order import Order
    from app.models.product import Product

    db = SessionLocal()
    try:
        with open(path, "w", newline="", encoding="utf8") as f:
            w = csv.writer(f)
            w.writerow(["transaction_id", "item_name"])
            for oi in db.query(OrderItem).all():
                prod = oi.product
                if prod is None:
                    continue
                w.writerow([oi.order_id, prod.name])
    finally:
        db.close()


def load_transactions(path=CSV_PATH):
    if not path.exists():
        print(f"CSV not found at {path}, exporting from DB...")
        export_transactions_from_db(path)

    df = pd.read_csv(path)
    transactions = df.groupby("transaction_id")["item_name"].apply(list).tolist()
    return transactions


def train(min_support=0.01, min_confidence=0.3):
    transactions = load_transactions()
    if not transactions:
        print("No transactions found. Exiting.")
        return []

    te = TransactionEncoder()
    X = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(X, columns=te.columns_)

    freq = apriori(df, min_support=min_support, use_colnames=True)
    rules = association_rules(freq, metric="confidence", min_threshold=min_confidence)
    rules = rules.sort_values(["confidence", "lift"], ascending=False)

    records = []
    for _, r in rules.iterrows():
        records.append({
            "antecedent": list(r["antecedents"]),
            "consequent": list(r["consequents"]),
            "support": float(r["support"]),
            "confidence": float(r["confidence"]),
            "lift": float(r["lift"]),
        })

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(records, indent=2))
    print(f"Saved {len(records)} rules to {OUT_PATH}")
    return records


if __name__ == "__main__":
    train()