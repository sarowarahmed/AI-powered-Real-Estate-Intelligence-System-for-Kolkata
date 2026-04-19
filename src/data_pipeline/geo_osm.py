import osmnx as ox
from geopy.distance import geodesic
from functools import lru_cache

# -----------------------------
# CORE FUNCTION (MAIN ENTRY)
# -----------------------------
@lru_cache(maxsize=100)
def get_nearest_places(lat, lon):
    """
    Given latitude & longitude, return distances (in km)
    to nearby infrastructure using OpenStreetMap.
    """

    location = (lat, lon)

    return {
        "metro": get_distance(location, {"railway": "station"}),
        "hospital": get_distance(location, {"amenity": "hospital"}),
        "school": get_distance(location, {"amenity": "school"}),
        "college": get_distance(location, {"amenity": "college"}),
        "bus": get_distance(location, {"highway": "bus_stop"}),
        "railway": get_distance(location, {"railway": "station"}),
        "police": get_distance(location, {"amenity": "police"}),
        "post_office": get_distance(location, {"amenity": "post_office"}),
    }


# -----------------------------
# HELPER: FETCH PLACES
# -----------------------------
@lru_cache(maxsize=100)
def fetch_places(lat, lon, tag_key, tag_value):
    """
    Fetch nearby places from OSM within 3km radius
    """
    try:
        tags = {tag_key: tag_value}

        gdf = ox.geometries_from_point(
            (lat, lon),
            tags,
            dist=3000
        )

        points = []

        for _, row in gdf.iterrows():
            if row.geometry.geom_type == "Point":
                points.append((row.geometry.y, row.geometry.x))

        return points

    except Exception:
        return []


# -----------------------------
# HELPER: DISTANCE CALCULATION
# -----------------------------
def get_distance(origin, tags):
    """
    Calculate minimum distance to nearest place
    """
    lat, lon = origin

    key, value = list(tags.items())[0]

    places = fetch_places(lat, lon, key, value)

    if not places:
        return 5  # fallback

    min_dist = float("inf")

    for place in places:
        dist = geodesic((lat, lon), place).km
        min_dist = min(min_dist, dist)

    return round(min_dist, 2)