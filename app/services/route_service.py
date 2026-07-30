from app.schemas.route_request import RouteRequest
from app.schemas.route_response import RouteCandidate, RoutePoint, TurnPoint
from app.utils.geo import calculate_route_distance_km
from app.algorithms.scoring import calculate_total_score

def generate_mock_routes(request: RouteRequest) -> list[RouteCandidate]:
    """
    仮ルート候補を複数生成する関数。

    現段階ではOSMやMapboxは使わず、
    スタート地点を基準にした疑似的なルートを3本作る。
    """

    start_lat = request.start.lat
    start_lon = request.start.lon

    mock_route_data = [
        {
            "id": "route_test001",
            "name": "仮ルート:信号少なめ",
            "coordinates": [
                {"lat": start_lat, "lon": start_lon},
                {"lat": start_lat + 0.001, "lon": start_lon + 0.001},
                {"lat": start_lat + 0.002, "lon": start_lon},
                {"lat": start_lat, "lon": start_lon},
            ],
            "elevation_gain_m": 25.0,
            "signals": 5,
            "intersections": 12,
            "traffic_score": 8.5,
            "turn_points": [
                {
                    "lat": start_lat + 0.001,
                    "lon": start_lon + 0.001,
                    "direction": "right",
                    "instruction": "次は右折です",
                }
            ],
        },
        {
            "id": "route_test002",
            "name": "仮ルート:距離優先",
            "coordinates": [
                {"lat": start_lat, "lon": start_lon},
                {"lat": start_lat + 0.002, "lon": start_lon + 0.001},
                {"lat": start_lat + 0.003, "lon": start_lon - 0.001},
                {"lat": start_lat + 0.001, "lon": start_lon - 0.002},
                {"lat": start_lat, "lon": start_lon},
            ],
            "elevation_gain_m": 35.0,
            "signals": 8,
            "intersections": 18,
            "traffic_score": 10.0,
            "turn_points": [
                {
                    "lat": start_lat + 0.002,
                    "lon": start_lon + 0.001,
                    "direction": "left",
                    "instruction": "次は左折です",
                },
                {
                    "lat": start_lat + 0.003,
                    "lon": start_lon - 0.001,
                    "direction": "right",
                    "instruction": "次は右折です",
                },
            ],
        },
        {
            "id": "route_test003",
            "name": "仮ルート:坂道少なめ",
            "coordinates": [
                {"lat": start_lat, "lon": start_lon},
                {"lat": start_lat + 0.001, "lon": start_lon - 0.001},
                {"lat": start_lat + 0.0015, "lon": start_lon - 0.002},
                {"lat": start_lat, "lon": start_lon - 0.001},
                {"lat": start_lat, "lon": start_lon},
            ],
            "elevation_gain_m": 10.0,
            "signals": 7,
            "intersections": 14,
            "traffic_score": 6.0,
            "turn_points": [
                {
                    "lat": start_lat + 0.001,
                    "lon": start_lon - 0.001,
                    "direction": "straight",
                    "instruction": "次は道なりです",
                }
            ],
        },
    ]

    route_candidates = []

    for route_data in mock_route_data:
        coordinates = route_data["coordinates"]

        actual_distance_km = calculate_route_distance_km(coordinates)

        total_score = calculate_total_score(
            target_distance_km=request.distance_km,
            actual_distance_km=actual_distance_km,
            elevation_gain_m=route_data["elevation_gain_m"],
            signals=route_data["signals"],
            intersections=route_data["intersections"],
            traffic_score=route_data["traffic_score"],
            preferences=request.preferences,
        )

        route_candidate = RouteCandidate(
            id=route_data["id"],
            name=route_data["name"],
            distance_km=round(actual_distance_km, 2),
            elevation_gain_m=route_data["elevation_gain_m"],
            signals=route_data["signals"],
            intersections=route_data["intersections"],
            traffic_score=route_data["traffic_score"],
            total_score=total_score,
            coordinates=[
                RoutePoint(
                    lat=point["lat"],
                    lon=point["lon"],
                )
                for point in coordinates
            ],
            turn_points=[
                TurnPoint(
                    lat=point["lat"],
                    lon=point["lon"],
                    direction=point["direction"],
                    instruction=point["instruction"],
                )
                for point in route_data["turn_points"]
            ],
        )

        route_candidates.append(route_candidate)

    route_candidates.sort(key=lambda route: route.total_score)

    return route_candidates