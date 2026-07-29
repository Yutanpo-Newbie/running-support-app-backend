from fastapi import APIRouter
from app.schemas.route_request import RouteRequest
from app.schemas.route_response import RouteResponse
from app.services.route_service import generate_mock_routes

router = APIRouter(prefix="/api", tags=["routes"])

@router.post("/routes/suggest", response_model=RouteResponse)
def suggest_routes(request: RouteRequest):
    routes = generate_mock_routes(request)

    return RouteResponse(routes=routes)