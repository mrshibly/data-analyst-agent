"""Tests for the health check endpoint."""


def test_health_check(client):
    """Health endpoint should return 200 with expected body."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "data-analyst-agent"
    assert "version" in data
