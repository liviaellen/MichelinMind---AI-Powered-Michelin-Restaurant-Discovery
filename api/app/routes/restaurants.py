from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from ..models.schemas import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from ..services.mongodb import mongodb
from bson import ObjectId

router = APIRouter()

@router.get("/", response_model=List[RestaurantResponse])
async def get_restaurants(skip: int = 0, limit: int = 10):
    """Get all restaurants with pagination"""
    db = await mongodb.async_connect()
    restaurants = await db.restaurants.find().skip(skip).limit(limit).to_list(length=limit)
    return restaurants

@router.get("/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(restaurant_id: str):
    """Get a specific restaurant by ID"""
    db = await mongodb.async_connect()
    restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.post("/", response_model=RestaurantResponse)
async def create_restaurant(restaurant: RestaurantCreate):
    """Create a new restaurant"""
    db = await mongodb.async_connect()
    restaurant_dict = restaurant.dict()
    result = await db.restaurants.insert_one(restaurant_dict)
    created_restaurant = await db.restaurants.find_one({"_id": result.inserted_id})
    return created_restaurant

@router.put("/{restaurant_id}", response_model=RestaurantResponse)
async def update_restaurant(restaurant_id: str, restaurant: RestaurantUpdate):
    """Update a restaurant"""
    db = await mongodb.async_connect()
    update_data = {k: v for k, v in restaurant.dict().items() if v is not None}
    result = await db.restaurants.update_one(
        {"_id": ObjectId(restaurant_id)},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    updated_restaurant = await db.restaurants.find_one({"_id": ObjectId(restaurant_id)})
    return updated_restaurant

@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    """Delete a restaurant"""
    db = await mongodb.async_connect()
    result = await db.restaurants.delete_one({"_id": ObjectId(restaurant_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return {"message": "Restaurant deleted successfully"}

@router.get("/search", response_model=List[RestaurantResponse])
async def search_restaurants(
    name: Optional[str] = None,
    cuisine: Optional[str] = None,
    location: Optional[str] = None,
    price: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    """Search restaurants with various filters."""
    db = await mongodb.async_connect()
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if cuisine:
        query["cuisine"] = {"$regex": cuisine, "$options": "i"}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if price:
        query["price"] = {"$regex": price, "$options": "i"}
    restaurants = await db.restaurants.find(query).skip(skip).limit(limit).to_list(length=limit)
    return restaurants
