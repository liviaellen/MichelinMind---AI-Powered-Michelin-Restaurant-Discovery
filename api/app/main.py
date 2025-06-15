from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MichelinMind API",
    description="AI-Powered Michelin Restaurant Discovery API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to MichelinMind API",
        "version": "1.0.0",
        "status": "active"
    }

# Import and include routers
from .routes import restaurants, search, recommendations

app.include_router(restaurants.router, prefix="/api/v1/restaurants", tags=["restaurants"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
