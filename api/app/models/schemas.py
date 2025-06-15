from pydantic import BaseModel, Field
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
