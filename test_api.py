import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from src.app import create_app
from src.storage import ExpenseStore


@pytest.fixture
def client():
    app = create_app(store=ExpenseStore())
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def add_sample_expense(client, **overrides):
    payload = {
        "title": "Lunch",
        "amount": 12.5,
        "category": "Food",
        "date": "2026-07-01",
    }
    payload.update(overrides)
    return client.post("/expenses", json=payload)


def test_health_check(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_add_expense_success(client):
    resp = add_sample_expense(client)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["title"] == "Lunch"
    assert body["amount"] == 12.5
    assert body["category"] == "Food"
    assert body["date"] == "2026-07-01"
    assert "id" in body


def test_add_expense_missing_field(client):
    resp = client.post(
        "/expenses", json={"title": "Lunch", "amount": 10, "category": "Food"}
    )
    assert resp.status_code == 400
    assert "date" in resp.get_json()["error"]


def test_add_expense_invalid_amount(client):
    resp = add_sample_expense(client, amount=-5)
    assert resp.status_code == 400

    resp2 = add_sample_expense(client, amount="ten")
    assert resp2.status_code == 400


def test_add_expense_invalid_date(client):
    resp = add_sample_expense(client, date="07-01-2026")
    assert resp.status_code == 400


def test_add_expense_blank_title(client):
    resp = add_sample_expense(client, title="   ")
    assert resp.status_code == 400


def test_list_expenses(client):
    add_sample_expense(client)
    add_sample_expense(client, title="Bus ticket", amount=3.0, category="Transport")

    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 2


def test_filter_by_category(client):
    add_sample_expense(client)
    add_sample_expense(client, title="Bus ticket", amount=3.0, category="Transport")

    resp = client.get("/expenses?category=Food")
    assert resp.status_code == 200
    body = resp.get_json()
    assert len(body) == 1
    assert body[0]["category"] == "Food"


def test_filter_by_category_case_insensitive(client):
    add_sample_expense(client, category="Food")
    resp = client.get("/expenses?category=food")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_filter_by_category_no_match(client):
    add_sample_expense(client, category="Food")
    resp = client.get("/expenses?category=Travel")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_single_expense(client):
    created = add_sample_expense(client).get_json()
    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["id"] == created["id"]


def test_get_single_expense_not_found(client):
    resp = client.get("/expenses/does-not-exist")
    assert resp.status_code == 404


def test_delete_expense(client):
    created = add_sample_expense(client).get_json()
    resp = client.delete(f"/expenses/{created['id']}")
    assert resp.status_code == 200
    assert resp.get_json()["deleted"] is True

    resp2 = client.get(f"/expenses/{created['id']}")
    assert resp2.status_code == 404


def test_delete_expense_not_found(client):
    resp = client.delete("/expenses/does-not-exist")
    assert resp.status_code == 404


def test_total_overall(client):
    add_sample_expense(client, amount=10)
    add_sample_expense(client, title="Bus", amount=5, category="Transport")

    resp = client.get("/expenses/total")
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 15


def test_total_by_category(client):
    add_sample_expense(client, amount=10, category="Food")
    add_sample_expense(client, title="Bus", amount=5, category="Transport")

    resp = client.get("/expenses/total?category=Food")
    assert resp.status_code == 200
    assert resp.get_json()["total"] == 10


def test_summary(client):
    add_sample_expense(client, amount=10, category="Food")
    add_sample_expense(client, title="Bus", amount=5, category="Transport")
    add_sample_expense(client, title="Dinner", amount=20, category="Food")

    resp = client.get("/expenses/summary")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["overall_total"] == 35
    assert body["by_category"]["Food"] == 30
    assert body["by_category"]["Transport"] == 5
