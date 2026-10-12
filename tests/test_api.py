from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_branches_returns_four():
    response = client.get("/branches")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 4
    expected_keys = {"branch_id", "name", "city", "address"}
    for item in data:
        assert expected_keys.issubset(item.keys())


def test_low_stock_rows_are_at_or_below_reorder_level():
    response = client.get("/reports/low-stock")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for row in data:
        assert row["quantity"] <= row["reorder_level"]


def test_low_stock_filter_by_branch():
    response = client.get("/reports/low-stock?branch_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for row in data:
        assert row["branch_name"] == "Manila Main Branch"


def test_low_stock_invalid_branch_id_returns_422():
    response = client.get("/reports/low-stock?branch_id=abc")
    assert response.status_code == 422


def test_expiring_requires_branch_id():
    response = client.get("/reports/expiring")
    assert response.status_code == 422


def test_top_sellers_max_five_per_branch():
    response = client.get("/reports/top-sellers")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for row in data:
        assert 1 <= row["rank_in_branch"] <= 5