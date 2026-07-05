import math
import random

class GeoService:
    def __init__(self):
        # Mock coordinates for known locations
        self.location_map = {
            "Delhi": (28.7041, 77.1025),
            "Mumbai": (19.0760, 72.8777),
            "Bangalore": (12.9716, 77.5946),
            "Hyderabad": (17.3850, 78.4867),
            "Chennai": (13.0827, 80.2707),
            "Ahmedabad": (23.0225, 72.5714),
            "Kolkata": (22.5726, 88.3639),
            "Pune": (18.5204, 73.8567),
            "Jaipur": (26.9124, 75.7873),
            "Lucknow": (26.8467, 80.9462),
            # Default fallback
            "Unknown": (0.0, 0.0)
        }

    def get_coordinates(self, location_name):
        """Mock Geocoding"""
        return self.location_map.get(location_name, (random.uniform(30, 50), random.uniform(-120, -70)))

    def calculate_distance(self, loc1, loc2):
        """Haversine distance in km"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        R = 6371  # radius of Earth in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def find_nearby(self, user_location, items, max_distance_km=50):
        """
        items: list of dicts with 'location' key
        user_location: string name or (lat, lon) tuple
        """
        user_coords = user_location if isinstance(user_location, tuple) else self.get_coordinates(user_location)
        
        results = []
        for item in items:
            item_loc = item.get('location', 'Unknown')
            item_coords = self.get_coordinates(item_loc)
            dist = self.calculate_distance(user_coords, item_coords)
            if dist <= max_distance_km:
                item_copy = item.copy()
                item_copy['distance_km'] = round(dist, 1)
                results.append(item_copy)
        
        return sorted(results, key=lambda x: x['distance_km'])

geo_service = GeoService()
