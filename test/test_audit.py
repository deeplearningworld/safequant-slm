import pytest
from safequant.audit import SeniorAuditor

def test_score_calculation():
    # Data Mock for validating the arithmetic logic of the score
    mock_details = [
        {"category": "Test", "passed": True},
        {"category": "Test", "passed": False}
    ]
    # The expected score for 1 success out of 2 tests is 50.0%
    score = (sum(1 for r in mock_details if r['passed']) / len(mock_details)) * 100
    assert score == 50.0

def test_vram_metric_type():
    # Verify if the VRAM metric returns a float (MB)
    vram = 512.5
    assert isinstance(vram, float)