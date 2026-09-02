"""
Unit tests for etl_pipeline.py
Jenkins will run these automatically in the "Test" stage of the pipeline.
If any test fails, the Jenkins build fails and stops before "deploying".
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from etl_pipeline import extract, transform, load


def test_extract_returns_records():
    records = extract()
    assert len(records) > 0
    assert "txn_id" in records[0]


def test_transform_drops_invalid_amounts():
    raw = [
        {"txn_id": "T001", "merchant": "M1", "amount": "100.00", "status": "SUCCESS"},
        {"txn_id": "T002", "merchant": "M2", "amount": "-5.00", "status": "FAILED"},
        {"txn_id": "T003", "merchant": "M3", "amount": "0.00", "status": "PENDING"},
    ]
    cleaned = transform(raw)
    assert len(cleaned) == 1
    assert cleaned[0]["txn_id"] == "T001"


def test_transform_converts_amount_to_float():
    raw = [{"txn_id": "T001", "merchant": "M1", "amount": "42.50", "status": "SUCCESS"}]
    cleaned = transform(raw)
    assert isinstance(cleaned[0]["amount"], float)
    assert cleaned[0]["amount"] == 42.50


def test_load_writes_csv(tmp_path):
    records = [{"txn_id": "T001", "merchant": "M1", "amount": 10.0, "status": "SUCCESS"}]
    output_file = tmp_path / "output" / "test_output.csv"
    path = load(records, output_path=str(output_file))
    assert os.path.exists(path)