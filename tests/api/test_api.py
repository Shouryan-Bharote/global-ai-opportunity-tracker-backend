import pytest
from fastapi.testclient import TestClient

from api.main import create_app
from shared.database.session import init_db
from shared.database.models import OpportunityCreate
from shared.database.repository import OpportunityRepository


@pytest.fixture(scope="module")
def client():
    init_db()
    app = create_app()
    with TestClient(app) as test_client:
        yield test_client


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database_connected"] is True


def test_list_opportunities(client):
    response = client.get("/api/v1/opportunities?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert data["limit"] == 10
    assert data["offset"] == 0


def test_opportunity_stats(client):
    response = client.get("/api/v1/opportunities/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_opportunities" in data
    assert "by_source" in data
    assert "by_type" in data
    assert "by_status" in data


def test_get_opportunity_not_found(client):
    response = client.get("/api/v1/opportunities/non-existent-uuid-or-url-1234")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_list_jobs(client):
    response = client.get("/api/v1/jobs?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
