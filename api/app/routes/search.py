from fastapi import APIRouter, HTTPException
from typing import List, Optional
from ..models.schemas import RestaurantResponse
from ..services.mongodb import mongodb
from pymongo import TEXT
import numpy as np
from sentence_transformers import SentenceTransformer

router = APIRouter()

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

@router.get("/text", response_model=List[RestaurantResponse])
async def text_search(query: str, limit: int = 10):
    """Search restaurants using MongoDB text search"""
    db = await mongodb.async_connect()

    # Create text index if it doesn't exist
    await db.restaurants.create_index([
        ("Name", TEXT),
        ("michelin_info.Cuisine", TEXT),
        ("michelin_info.Description", TEXT)
    ])

    # Perform text search
    restaurants = await db.restaurants.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(limit).to_list(length=limit)

    return restaurants

@router.get("/vector", response_model=List[RestaurantResponse])
async def vector_search(query: str, limit: int = 10):
    """Search restaurants using vector similarity"""
    db = await mongodb.async_connect()

    # Generate query embedding
    query_embedding = model.encode(query)

    # Perform vector search using MongoDB Atlas
    restaurants = await db.restaurants.aggregate([
        {
            "$search": {
                "index": "restaurant_embeddings",
                "knnBeta": {
                    "vector": query_embedding.tolist(),
                    "path": "embedding",
                    "k": limit
                }
            }
        },
        {
            "$project": {
                "Name": 1,
                "michelin_info": 1,
                "google_info": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]).to_list(length=limit)

    return restaurants

@router.get("/hybrid", response_model=List[RestaurantResponse])
async def hybrid_search(
    query: str,
    cuisine: Optional[str] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[str] = None,
    limit: int = 10
):
    """Hybrid search combining text, vector, and filters"""
    db = await mongodb.async_connect()

    # Build filter conditions
    filter_conditions = []
    if cuisine:
        filter_conditions.append({"text": {"query": cuisine, "path": "michelin_info.Cuisine"}})
    if min_rating is not None:
        filter_conditions.append({"range": {"path": "google_info.google_rating", "gte": min_rating}})
    if max_price:
        filter_conditions.append({"text": {"query": max_price, "path": "michelin_info.Price"}})

    # Generate query embedding
    query_embedding = model.encode(query)

    # Perform hybrid search
    restaurants = await db.restaurants.aggregate([
        {
            "$search": {
                "index": "restaurant_hybrid",
                "compound": {
                    "must": [
                        {
                            "knnBeta": {
                                "vector": query_embedding.tolist(),
                                "path": "embedding",
                                "k": limit
                            }
                        },
                        {
                            "text": {
                                "query": query,
                                "path": ["Name", "michelin_info.Cuisine", "michelin_info.Description"]
                            }
                        }
                    ],
                    "filter": filter_conditions
                }
            }
        },
        {
            "$project": {
                "Name": 1,
                "michelin_info": 1,
                "google_info": 1,
                "score": {"$meta": "searchScore"}
            }
        }
    ]).to_list(length=limit)

    return restaurants
