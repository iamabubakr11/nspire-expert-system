"""Run with: python -m pytest -q"""
import itertools
import pytest
from app import app
from expert.engine import evaluate


@pytest.mark.parametrize("answers,expected,rule", [
    ({"goal": "products", "payment": "yes", "accounts": "no"}, "online_store", "R02"),
    ({"goal": "products", "payment": "no", "accounts": "no"}, "catalog", "R03"),
    ({"goal": "company", "payment": "no", "accounts": "no"}, "corporate", "R04"),
    ({"goal": "campaign", "payment": "no", "accounts": "no"}, "landing", "R05"),
    ({"goal": "company", "payment": "yes", "accounts": "yes"}, "web_app", "R01"),
])
def test_expected_recommendations(answers, expected, rule):
    result = evaluate(answers)
    assert result["code"] == expected
    assert result["rule_id"] == rule
    assert result["rules_fired"] == 1
    assert result["rule"]


def test_all_twelve_combinations_choose_once():
    for goal, payment, accounts in itertools.product(
        ["products", "company", "campaign"], ["yes", "no"], ["yes", "no"]
    ):
        result = evaluate({"goal": goal, "payment": payment, "accounts": accounts})
        assert result["rules_fired"] == 1
        assert result["code"]


@pytest.mark.parametrize("invalid", [
    {}, None, [],
    {"goal": "unknown", "payment": "yes", "accounts": "no"},
    {"goal": "products", "payment": "yes"},
    {"goal": "products", "payment": "yes", "accounts": "no", "extra": 1},
])
def test_invalid_inputs(invalid):
    with pytest.raises(ValueError):
        evaluate(invalid)


def test_api_success_and_errors():
    client = app.test_client()
    assert client.get("/api/health").status_code == 200
    assert client.get("/").status_code == 200
    result = client.post("/api/recommend", json={"goal": "products", "payment": "yes", "accounts": "no"})
    assert result.status_code == 200
    assert result.json["code"] == "online_store"
    assert client.post("/api/recommend", json={}).status_code == 400
    assert client.post("/api/recommend", data="hello", content_type="text/plain").status_code == 415
