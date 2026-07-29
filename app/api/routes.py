from fastapi import APIRouter
from app.schemas.route_request import RouteRequest
from app.schemas.route_response import RouteResponse, RouteCandidate, RoutePoint, TurnPoint
from app.utils.geo import calculate_route_distance_km
from app.algorithms.scoring import calculate_total_score


router = APIRouter(prefix="/api", tags=["routes"])

@router.post("/routes/suggest", response_model=RouteResponse)
def suggest_routes(request: RouteRequest):
    start_lat = request.start.lat
    start_lon = request.start.lon

    coordinates = [
        {"lat": start_lat, "lon": start_lon},
        {"lat": start_lat + 0.001, "lon": start_lon + 0.001},
        {"lat": start_lat + 0.002, "lon": start_lon},
        {"lat": start_lat, "lon": start_lon},
    ]   

    calculated_distance_km = calculate_route_distance_km(coordinates)
    total_score = calculate_total_score(
        target_distance_km=request.distance_km,
        actual_distance_km=calculated_distance_km,
        elevation_gain_m=25.0,
        signals=5,
        intersections=12,
        traffic_score=8.5,
    )

    sample_route = RouteCandidate(
        id="route_test001",
        name="仮ルート:信号少なめ",
        distance_km=round(calculated_distance_km, 2),
        elevation_gain_m=25.0,
        signals=5,
        intersections=12,
        traffic_score=8.5,
        total_score=total_score,
        coordinates=[
            RoutePoint(lat=point["lat"], lon=point["lon"])
            for point in coordinates
        ],
        turn_points=[
            TurnPoint(
                lat=start_lat + 0.001,
                lon=start_lon + 0.001,
                direction="right",
                instruction="次は右折です",
            )
        ],
    )

    return RouteResponse(routes=[sample_route])