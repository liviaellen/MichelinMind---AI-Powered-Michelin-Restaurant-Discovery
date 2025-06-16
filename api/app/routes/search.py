from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional, Dict
from ..models.schemas import RestaurantSearchParams, RestaurantResponse, MichelinRestaurant
from ..services.michelin_service import MichelinService

router = APIRouter()
michelin_service = MichelinService()

@router.get("/search", response_model=RestaurantResponse)
async def search_restaurants(
    query: Optional[str] = None,
    cuisine: Optional[str] = None,
    price: Optional[str] = None,
    location: Optional[str] = None,
    award: Optional[str] = None,
    has_green_star: Optional[bool] = None,
    facilities: Optional[List[str]] = Query(None),
    skip: int = 0,
    limit: int = 10
):
    """
    Search for Michelin restaurants with various filters.

    - **query**: Search in name, cuisine, and description
    - **cuisine**: Filter by cuisine type
    - **price**: Filter by price range
    - **location**: Filter by location
    - **award**: Filter by award (e.g., "3 Stars", "2 Stars", "1 Star", "Bib Gourmand")
    - **has_green_star**: Filter by green star status
    - **facilities**: Filter by available facilities
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    try:
        params = RestaurantSearchParams(
            query=query,
            cuisine=cuisine,
            price=price,
            location=location,
            award=award,
            has_green_star=has_green_star,
            facilities=facilities,
            skip=skip,
            limit=limit
        )
        return michelin_service.search_restaurants(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/restaurants/{name}", response_model=MichelinRestaurant)
async def get_restaurant_by_name(name: str):
    """
    Get a specific restaurant by name.
    """
    restaurant = michelin_service.get_restaurant_by_name(name)
    if not restaurant:
        raise HTTPException(status_code=404, detail=f"Restaurant '{name}' not found")
    return restaurant

@router.get("/price-range", response_model=List[MichelinRestaurant])
async def find_by_price_range(
    min_price: Optional[int] = Query(None, description="Minimum price level (1-4)"),
    max_price: Optional[int] = Query(None, description="Maximum price level (1-4)"),
    location: Optional[str] = Query(None, description="Location to filter by")
):
    """Find restaurants within a specific price range."""
    return michelin_service.find_by_price_range(min_price, max_price, location)

@router.get("/price-comparison", response_model=Dict[str, Dict[str, float]])
async def compare_prices_by_location(
    locations: List[str] = Query(..., description="List of locations to compare")
):
    """Compare average prices across different locations."""
    return michelin_service.compare_prices_by_location(locations)

@router.get("/best-value", response_model=List[dict])
async def find_best_value(
    location: Optional[str] = Query(None, description="Location to filter by"),
    limit: int = Query(10, description="Maximum number of results")
):
    """Find best value restaurants based on award level and price."""
    return michelin_service.find_best_value(location, limit)

@router.get("/radius", response_model=List[dict])
async def find_within_radius(
    latitude: float = Query(..., description="Latitude of the center point"),
    longitude: float = Query(..., description="Longitude of the center point"),
    radius_km: float = Query(..., description="Radius in kilometers"),
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants within a specific radius."""
    return michelin_service.find_within_radius(latitude, longitude, radius_km, limit)

@router.get("/area/{area}", response_model=List[MichelinRestaurant])
async def find_by_area(
    area: str,
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants in a specific area/neighborhood."""
    return michelin_service.find_by_area(area, limit)

@router.get("/multi-cuisine", response_model=List[MichelinRestaurant])
async def find_multiple_cuisines(
    cuisines: List[str] = Query(..., description="List of cuisines to search for"),
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants serving multiple cuisines."""
    return michelin_service.find_multiple_cuisines(cuisines, limit)

@router.get("/dietary/{dietary}", response_model=List[MichelinRestaurant])
async def find_by_dietary(
    dietary: str,
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants with specific dietary options."""
    return michelin_service.find_by_dietary(dietary, limit)

@router.get("/unique-cuisines", response_model=List[dict])
async def find_unique_cuisines(
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants with unique or rare cuisines."""
    return michelin_service.find_unique_cuisines(limit)

@router.get("/amenities", response_model=List[MichelinRestaurant])
async def find_by_amenities(
    amenities: List[str] = Query(..., description="List of amenities to search for"),
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants with specific amenities."""
    return michelin_service.find_by_amenities(amenities, limit)

@router.get("/features", response_model=List[MichelinRestaurant])
async def find_by_features(
    features: List[str] = Query(..., description="List of features to search for"),
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants with special features."""
    return michelin_service.find_by_features(features, limit)

@router.get("/services", response_model=List[MichelinRestaurant])
async def find_by_services(
    services: List[str] = Query(..., description="List of services to search for"),
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants with specific services."""
    return michelin_service.find_by_services(services, limit)

@router.get("/multiple-awards", response_model=List[MichelinRestaurant])
async def find_multiple_awards():
    """Find restaurants with multiple awards."""
    return michelin_service.find_multiple_awards()

@router.get("/green-stars", response_model=List[MichelinRestaurant])
async def find_green_stars(
    limit: int = Query(10, description="Maximum number of results")
):
    """Find restaurants with green stars."""
    return michelin_service.find_green_stars(limit)

@router.get("/nearest", response_model=List[dict])
async def find_nearest_restaurants(
    latitude: float = Query(..., description="Latitude of the center point"),
    longitude: float = Query(..., description="Longitude of the center point"),
    limit: int = Query(5, description="Maximum number of results")
):
    """Find the nearest restaurants to a given location."""
    return michelin_service.find_nearest_restaurants(latitude, longitude, limit)
