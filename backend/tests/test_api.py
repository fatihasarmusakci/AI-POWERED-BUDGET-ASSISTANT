import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_hotels_endpoint(client: TestClient) -> None:
    response = client.get("/hotels?city=london")
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "london"
    assert len(data["items"]) > 0


def test_game_guess_validation(client: TestClient) -> None:
    bad_response = client.post("/game/guess", json={"prompt_id": "p1", "guess": "other"})
    assert bad_response.status_code == 200
    assert bad_response.json()["accepted"] is False

    good_response = client.post("/game/guess", json={"prompt_id": "p1", "guess": "real"})
    assert good_response.status_code == 200
    assert good_response.json()["accepted"] is True
