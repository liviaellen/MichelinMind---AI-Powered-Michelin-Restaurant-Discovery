import pandas as pd
from typing import List, Dict, Optional, Tuple
from ..models.schemas import MichelinRestaurant, RestaurantSearchParams, RestaurantResponse
import requests
from io import StringIO
from math import radians, sin, cos, sqrt, atan2

class MichelinService:
    def __init__(self):
        self.csv_url = "https://raw.githubusercontent.com/ngshiheng/michelin-my-maps/main/data/michelin_my_maps.csv"
        self._data = None

    def _load_data(self) -> pd.DataFrame:
        if self._data is None:
            response = requests.get(self.csv_url)
            response.raise_for_status()
            self._data = pd.read_csv(StringIO(response.text))
        return self._data

    def _convert_to_restaurant(self, row):
        # Format phone number to remove decimal point
        phone = str(row['PhoneNumber']) if pd.notna(row['PhoneNumber']) else ""
        if phone.endswith('.0'):
            phone = phone[:-2]

        return MichelinRestaurant(
            name=str(row['Name']) if pd.notna(row['Name']) else "",
            address=str(row['Address']) if pd.notna(row['Address']) else "",
            price=str(row['Price']) if pd.notna(row['Price']) else "",
            cuisine=str(row['Cuisine']) if pd.notna(row['Cuisine']) else "",
            phone_number=phone,
            description=str(row['Description']) if pd.notna(row['Description']) else "",
            award=str(row['Award']) if pd.notna(row['Award']) else "",
            location=str(row['Location']) if pd.notna(row['Location']) else "",
            latitude=float(row['Latitude']) if pd.notna(row['Latitude']) else 0.0,
            longitude=float(row['Longitude']) if pd.notna(row['Longitude']) else 0.0,
            has_green_star=bool(row['GreenStar']) if pd.notna(row['GreenStar']) else False,
            facilities_and_services=str(row['FacilitiesAndServices']) if pd.notna(row['FacilitiesAndServices']) else "",
            michelin_url=str(row['Url']) if pd.notna(row['Url']) else None,
            website_url=str(row['WebsiteUrl']) if pd.notna(row['WebsiteUrl']) else None,
            green_star=int(row['GreenStar']) if pd.notna(row['GreenStar']) else 0,
            facilities=row.get('FacilitiesAndServices', '').split(',') if pd.notna(row.get('FacilitiesAndServices')) else []
        )

    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth's radius in kilometers

        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c

        return distance

    def search_restaurants(self, params: RestaurantSearchParams) -> RestaurantResponse:
        df = self._load_data()

        # Apply filters with OR logic
        mask = pd.Series(True, index=df.index)
        if params.query:
            mask &= (
                df['Name'].astype(str).str.contains(params.query, case=False, na=False) |
                df['Cuisine'].astype(str).str.contains(params.query, case=False, na=False) |
                df['Description'].astype(str).str.contains(params.query, case=False, na=False)
            )
        if params.cuisine:
            mask &= df['Cuisine'].astype(str).str.contains(params.cuisine, case=False, na=False)
        if params.price:
            mask &= df['Price'].astype(str) == str(params.price)
        if params.location:
            mask &= df['Location'].astype(str).str.contains(params.location, case=False, na=False)
        if params.award:
            mask &= df['Award'].astype(str).str.contains(params.award, case=False, na=False)
        if params.has_green_star is not None:
            mask &= df['GreenStar'].astype(str) == str(params.has_green_star)
        if params.facilities:
            for facility in params.facilities:
                mask &= df['FacilitiesAndServices'].astype(str).str.contains(facility, case=False, na=False)

        df = df[mask]

        # Apply pagination
        total = len(df)
        df = df.iloc[params.skip:params.skip + params.limit]

        # Convert to restaurant objects
        restaurants = [self._convert_to_restaurant(row) for _, row in df.iterrows()]

        # Fallback logic: If no results, suggest relaxing filters
        if total == 0:
            print("No results found. Try relaxing your filters.")

        return RestaurantResponse(
            results=restaurants,
            total=total,
            skip=params.skip,
            limit=params.limit
        )

    def get_restaurant_by_name(self, name: str) -> Optional[MichelinRestaurant]:
        df = self._load_data()
        restaurant = df[df['Name'] == name]
        if len(restaurant) > 0:
            return self._convert_to_restaurant(restaurant.iloc[0])
        return None

    def find_nearest_restaurants(self, latitude: float, longitude: float, limit: int = 5) -> List[Dict]:
        """Find the nearest restaurants to a given location"""
        df = self._load_data()

        # Filter out restaurants without coordinates
        df = df.dropna(subset=['Latitude', 'Longitude'])

        # Calculate distances
        distances = []
        for _, row in df.iterrows():
            distance = self._calculate_distance(
                latitude, longitude,
                float(row['Latitude']), float(row['Longitude'])
            )
            distances.append((distance, row))

        # Sort by distance and get top N
        distances.sort(key=lambda x: x[0])
        nearest = distances[:limit]

        return [{
            "restaurant": self._convert_to_restaurant(row),
            "distance_km": round(distance, 2)
        } for distance, row in nearest]

    def find_most_affordable(self, cuisine: Optional[str] = None, location: Optional[str] = None, limit: int = 5) -> List[MichelinRestaurant]:
        """Find the most affordable restaurants"""
        df = self._load_data()

        # Filter by cuisine and location if provided
        if cuisine:
            df = df[df['Cuisine'].str.contains(cuisine, case=False, na=False)]
        if location:
            df = df[df['Location'].str.contains(location, case=False, na=False)]

        # Sort by price (assuming $ is cheaper than $$, etc.)
        df['price_rank'] = df['Price'].map({'$': 1, '$$': 2, '$$$': 3, '$$$$': 4})
        df = df.sort_values('price_rank')

        # Get top N
        df = df.head(limit)

        return [self._convert_to_restaurant(row) for _, row in df.iterrows()]

    def find_by_award(self, award: str, location: Optional[str] = None) -> List[MichelinRestaurant]:
        """Find restaurants by award type"""
        df = self._load_data()

        # Filter by award
        df = df[df['Award'] == award]

        # Filter by location if provided
        if location:
            df = df[df['Location'].str.contains(location, case=False, na=False)]

        return [self._convert_to_restaurant(row) for _, row in df.iterrows()]

    def find_by_facilities(self, facilities: List[str], location: Optional[str] = None) -> List[MichelinRestaurant]:
        """Find restaurants with specific facilities"""
        df = self._load_data()

        # Filter by facilities
        for facility in facilities:
            df = df[df['FacilitiesAndServices'].str.contains(facility, case=False, na=False)]

        # Filter by location if provided
        if location:
            df = df[df['Location'].str.contains(location, case=False, na=False)]

        return [self._convert_to_restaurant(row) for _, row in df.iterrows()]

    def find_vegetarian_friendly(self, location: Optional[str] = None, limit: int = 10) -> List[MichelinRestaurant]:
        """Find vegetarian-friendly restaurants."""
        restaurants = self._load_data()

        # Filter by location if specified
        if location:
            restaurants = [r for r in restaurants if location.lower() in r.location.lower()]

        # Filter for vegetarian-friendly restaurants
        vegetarian = [r for r in restaurants if any(
            term in r.description.lower() for term in ['vegetarian', 'vegan', 'plant-based']
        )]

        return vegetarian[:limit]

    def find_by_price_range(self, min_price: Optional[int] = None, max_price: Optional[int] = None,
                          location: Optional[str] = None) -> List[MichelinRestaurant]:
        """Find restaurants within a specific price range."""
        restaurants = self._load_data()

        # Filter by location if specified
        if location:
            restaurants = [r for r in restaurants if location.lower() in r.location.lower()]

        # Filter by price range
        if min_price is not None:
            restaurants = [r for r in restaurants if r.price and len(r.price) >= min_price]
        if max_price is not None:
            restaurants = [r for r in restaurants if r.price and len(r.price) <= max_price]

        return restaurants

    def compare_prices_by_location(self, locations: List[str]) -> Dict[str, Dict[str, float]]:
        """Compare average prices across different locations."""
        restaurants = self._load_data()
        results = {}

        for location in locations:
            location_restaurants = [r for r in restaurants if location.lower() in r.location.lower()]
            if not location_restaurants:
                continue

            # Calculate average price for each award level
            prices = {
                '3 Stars': [],
                '2 Stars': [],
                '1 Star': [],
                'Bib Gourmand': []
            }

            for r in location_restaurants:
                if r.award in prices and r.price:
                    prices[r.award].append(len(r.price))

            # Calculate averages
            results[location] = {
                award: sum(prices) / len(prices) if prices else 0
                for award, prices in prices.items()
            }

        return results

    def find_best_value(self, location: Optional[str] = None, limit: int = 10) -> List[dict]:
        df = self._load_data()
        restaurants = [self._convert_to_restaurant(row) for _, row in df.iterrows()]

        # Filter by location if specified
        if location:
            restaurants = [r for r in restaurants if location.lower() in (r.location or "").lower()]

        # Calculate value score (award level / price)
        value_scores = []
        for r in restaurants:
            if not r.award:
                continue
            award_value = {
                '3 Stars': 3,
                '2 Stars': 2,
                '1 Star': 1,
                'Bib Gourmand': 0.5
            }.get(r.award, 0)
            # If price is missing, treat as highest price level (4)
            price = len(r.price) if r.price else 4
            if award_value > 0:
                value_score = award_value / price
                value_scores.append({
                    'restaurant': r.dict(),
                    'value_score': value_score,
                    'award_value': award_value,
                    'price': price
                })

        # Sort by value score
        value_scores.sort(key=lambda x: x['value_score'], reverse=True)
        return value_scores[:limit]

    def find_within_radius(self, latitude: float, longitude: float, radius_km: float,
                         limit: int = 10) -> List[dict]:
        """Find restaurants within a specific radius."""
        restaurants = self._load_data()
        results = []

        for r in restaurants:
            if not r.latitude or not r.longitude:
                continue

            distance = self._calculate_distance(
                latitude, longitude,
                float(r.latitude), float(r.longitude)
            )

            if distance <= radius_km:
                results.append({
                    'restaurant': r,
                    'distance_km': distance
                })

        # Sort by distance
        results.sort(key=lambda x: x['distance_km'])
        return results[:limit]

    def find_by_area(self, area: str, limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants in a specific area/neighborhood."""
        restaurants = self._load_data()

        # Filter by area/neighborhood
        area_restaurants = [r for r in restaurants if area.lower() in r.location.lower()]
        return area_restaurants[:limit]

    def find_multiple_cuisines(self, cuisines: List[str], limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants serving multiple cuisines."""
        restaurants = self._load_data()

        # Filter restaurants that serve all specified cuisines
        multi_cuisine = [
            r for r in restaurants
            if all(cuisine.lower() in r.cuisine.lower() for cuisine in cuisines)
        ]

        return multi_cuisine[:limit]

    def find_by_dietary(self, dietary: str, limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants with specific dietary options."""
        restaurants = self._load_data()

        # Filter by dietary options
        dietary_restaurants = [
            r for r in restaurants
            if dietary.lower() in r.description.lower()
        ]

        return dietary_restaurants[:limit]

    def find_unique_cuisines(self, limit: int = 10) -> List[dict]:
        """Find restaurants with unique or rare cuisines."""
        restaurants = self._load_data()

        # Count cuisine occurrences
        cuisine_counts = {}
        for r in restaurants:
            for cuisine in r.cuisine.split(','):
                cuisine = cuisine.strip()
                cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1

        # Find rare cuisines (appearing in less than 5 restaurants)
        rare_cuisines = {c: count for c, count in cuisine_counts.items() if count < 5}

        # Find restaurants with rare cuisines
        rare_restaurants = []
        for r in restaurants:
            rare_cuisine_list = [c.strip() for c in r.cuisine.split(',') if c.strip() in rare_cuisines]
            if rare_cuisine_list:
                rare_restaurants.append({
                    'restaurant': r,
                    'rare_cuisines': rare_cuisine_list
                })

        return rare_restaurants[:limit]

    def find_by_amenities(self, amenities: List[str], limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants with specific amenities."""
        restaurants = self._load_data()

        # Filter by amenities
        amenity_restaurants = [
            r for r in restaurants
            if all(amenity.lower() in r.facilities_and_services.lower() for amenity in amenities)
        ]

        return amenity_restaurants[:limit]

    def find_by_features(self, features: List[str], limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants with special features."""
        restaurants = self._load_data()

        # Filter by features
        feature_restaurants = [
            r for r in restaurants
            if all(feature.lower() in r.facilities_and_services.lower() for feature in features)
        ]

        return feature_restaurants[:limit]

    def find_by_services(self, services: List[str], limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants with specific services."""
        restaurants = self._load_data()

        # Filter by services
        service_restaurants = [
            r for r in restaurants
            if all(service.lower() in r.facilities_and_services.lower() for service in services)
        ]

        return service_restaurants[:limit]

    def find_recent_award_changes(self, years: int = 1) -> List[dict]:
        """Find restaurants that recently gained/lost stars."""
        # Note: This would require historical data, which isn't in the current dataset
        # This is a placeholder for future implementation
        return []

    def find_multiple_awards(self) -> List[MichelinRestaurant]:
        """Find restaurants with multiple awards."""
        restaurants = self._load_data()

        # Filter restaurants with multiple awards
        multi_award = [
            r for r in restaurants
            if r.award and ('Stars' in r.award and 'Bib Gourmand' in r.award)
        ]

        return multi_award

    def find_green_stars(self, limit: int = 10) -> List[MichelinRestaurant]:
        """Find restaurants with green stars."""
        restaurants = self._load_data()

        # Filter restaurants with green stars
        green_star = [r for r in restaurants if r.has_green_star]
        return green_star[:limit]
