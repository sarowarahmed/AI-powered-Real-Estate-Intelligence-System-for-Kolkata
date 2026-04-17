import osmnx as ox
from geopy.distance import geodesic

# Cache to avoid repeated API calls
location_cache = {}

def get_coordinates(location):
    try:
        if location in location_cache:
            return location_cache[location]

        point = ox.geocode(f"{location}, Kolkata, India")
        location_cache[location] = point
        return point

    except:
        return None


def get_nearby_places(location, tag_key, tag_value):
    coords = get_coordinates(location)
    
    if not coords:
        return []

    try:
        tags = {tag_key: tag_value}
        gdf = ox.geometries_from_point(coords, tags, dist=3000)  # 3km radius
        
        points = []
        for _, row in gdf.iterrows():
            if row.geometry.geom_type == "Point":
                points.append((row.geometry.y, row.geometry.x))
        
        return points

    except:
        return []


def get_min_distance(location, places):
    coords = get_coordinates(location)
    
    if not coords or not places:
        return None

    min_dist = float("inf")

    for place in places:
        dist = geodesic(coords, place).km
        min_dist = min(min_dist, dist)

    return round(min_dist, 2)

def get_hospital_distance(location):
    places = get_nearby_places(location, "amenity", "hospital")
    return get_min_distance(location, places)


def get_school_distance(location):
    places = get_nearby_places(location, "amenity", "school")
    return get_min_distance(location, places)

def get_college_distance(location):
    places = get_nearby_places(location, "amenity", "college")
    return get_min_distance(location, places)


def get_transport_distance(location):
    places = get_nearby_places(location, "highway", "bus_stop")
    return get_min_distance(location, places)

def get_railway_distance(location):
    places = get_nearby_places(location, "railway", "station")
    return get_min_distance(location, places)

def get_police_distance(location):
    places = get_nearby_places(location, "amenity", "police")
    return get_min_distance(location, places)

def get_postoffice_distance(location):
    places = get_nearby_places(location, "amenity", "postoffice")
    return get_min_distance(location, places)