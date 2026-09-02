"""
Mini ETL Pipeline - Practice Project for CI/CD (Jenkins + Git)
Simulates a small data pipeline: Extract -> Transform -> Load
"""

import csv
import os

RAW_DATA = [
    {"txn_id": "T001", "merchant": "Merchant A", "amount": "150.00", "status": "SUCCESS"},
    {"txn_id": "T002", "merchant": "Merchant B", "amount": "-20.00", "status": "FAILED"},
    {"txn_id": "T003", "merchant": "Merchant A", "amount": "75.50", "status": "SUCCESS"},
    {"txn_id": "T004", "merchant": "Merchant C", "amount": "0.00", "status": "PENDING"},
]

OUTPUT_FILE = "output/processed_transactions.csv"


def extract():
    """Simulates pulling raw transaction data (e.g., from a source system/API)."""
    return RAW_DATA


def transform(records):
    """Cleans and validates records: drops invalid amounts."""
    cleaned = []
    for r in records:
        amount = float(r["amount"])
        if amount <= 0:
            continue
        cleaned.append({
            "txn_id": r["txn_id"],
            "merchant": r["merchant"],
            "amount": amount,
            "status": r["status"],
        })
    return cleaned


def load(records, output_path=OUTPUT_FILE):
    """Writes transformed records to a CSV file (simulating a load into a warehouse)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["txn_id", "merchant", "amount", "status"])
        writer.writeheader()
        writer.writerows(records)
    return output_path


def run_pipeline():
    raw = extract()
    cleaned = transform(raw)
    path = load(cleaned)
    print(f"Pipeline complete. {len(cleaned)} records written to {path}")
    return cleaned


if __name__ == "__main__":
    run_pipeline()
