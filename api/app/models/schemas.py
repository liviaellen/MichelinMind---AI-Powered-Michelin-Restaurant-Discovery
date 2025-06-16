from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    type: str = "Point"
    coordinates: List[float]

class MichelinInfo(BaseModel):
    Address: str
    Location: str
    Price: str
    Cuisine: str
    Longitude: float
    Latitude: float
    PhoneNumber: Optional[str] = None
    Url: Optional[str] = None
    WebsiteUrl: Optional[str] = None
    Award: Optional[str] = None
    GreenStar: int = 0
    FacilitiesAndServices: Optional[str] = None
    Description: Optional[str] = None

class GoogleInfo(BaseModel):
    google_rating: Optional[float] = None
    google_reviews: Optional[int] = None

class Restaurant(BaseModel):
    Name: str
    michelin_info: MichelinInfo
    google_info: GoogleInfo
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RestaurantCreate(Restaurant):
    pass

class RestaurantUpdate(BaseModel):
    Name: Optional[str] = None
    michelin_info: Optional[MichelinInfo] = None
    google_info: Optional[GoogleInfo] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RestaurantResponse(Restaurant):
    id: str = Field(..., alias="_id")

class MichelinRestaurant(BaseModel):
    name: str
    address: Optional[str] = None
    location: Optional[str] = None
    price: Optional[str] = None
    cuisine: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    phone_number: Optional[str] = None
    michelin_url: Optional[HttpUrl] = None
    website_url: Optional[HttpUrl] = None
    award: Optional[str] = None
    green_star: Optional[int] = 0
    facilities: Optional[List[str]] = None
    description: Optional[str] = None

class RestaurantSearchParams(BaseModel):
    query: Optional[str] = None
    cuisine: Optional[str] = None
    price: Optional[str] = None
    location: Optional[str] = None
    award: Optional[str] = None
    has_green_star: Optional[bool] = None
    facilities: Optional[List[str]] = None
    skip: int = 0
    limit: int = 10

class RestaurantResponse(BaseModel):
    results: List[MichelinRestaurant]
    total: int
    skip: int
    limit: int
