import pytest, asyncio
from src.scanner import TokenRisk
def test_risk_score_starts_at_100():
    risk = TokenRisk(address="0x1234")
    assert risk.score == 100
def test_add_risk_decreases_score():
    risk = TokenRisk(address="0x1234")
    risk.add_risk("Honeypot", 30)
    assert risk.score == 70
def test_label_high_risk():
    risk = TokenRisk(address="0x1234")
    risk.score = 20
    assert "HIGH RISK" in risk.label()
