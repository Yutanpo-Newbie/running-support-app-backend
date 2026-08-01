from fastapi.testclient import TestClient

from app.main import app
#a

client = TestClient(app)


def test_suggest_routes_returns_200():
    request_body = {
        "start": {
            "lat": 35.8721,
            "lon": 140.0106,
        },
        "distance_km": 5.0,
        "preferences": {
            "avoid_traffic": True,
            "avoid_signals": True,
            "avoid_intersections": True,
            "elevation_mode": "low",
        },
    }

    response = client.post("/api/routes/suggest", json=request_body)

    assert response.status_code == 200


def test_suggest_routes_returns_three_routes():
    request_body = {
        "start": {
            "lat": 35.8721,
            "lon": 140.0106,
        },
        "distance_km": 5.0,
        "preferences": {
            "avoid_traffic": True,
            "avoid_signals": True,
            "avoid_intersections": True,
            "elevation_mode": "low",
        },
    }

    response = client.post("/api/routes/suggest", json=request_body)
    data = response.json()

    assert "routes" in data
    assert len(data["routes"]) == 3


def test_routes_have_geometry_linestring():
    request_body = {
        "start": {
            "lat": 35.8721,
            "lon": 140.0106,
        },
        "distance_km": 5.0,
        "preferences": {
            "avoid_traffic": True,
            "avoid_signals": True,
            "avoid_intersections": True,
            "elevation_mode": "low",
        },
    }

    response = client.post("/api/routes/suggest", json=request_body)
    data = response.json()

    for route in data["routes"]:
        assert "geometry" in route
        assert route["geometry"]["type"] == "LineString"
        assert len(route["geometry"]["coordinates"]) >= 2


def test_routes_are_sorted_by_total_score():
    request_body = {
        "start": {
            "lat": 35.8721,
            "lon": 140.0106,
        },
        "distance_km": 5.0,
        "preferences": {
            "avoid_traffic": True,
            "avoid_signals": True,
            "avoid_intersections": True,
            "elevation_mode": "low",
        },
    }

    response = client.post("/api/routes/suggest", json=request_body)
    data = response.json()

    scores = [
        route["total_score"]
        for route in data["routes"]
    ]

    assert scores == sorted(scores)