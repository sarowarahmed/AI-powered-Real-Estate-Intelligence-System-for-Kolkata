import re
import math
from .geo_features import get_distance_to_metro
from .geo_osm import (
    get_hospital_distance,
    get_school_distance,
    get_transport_distance,
    get_college_distance,
    get_railway_distance,
    get_police_distance,
    get_postoffice_distance
)

LOCATION_MAP = {
    "new town": "New Town",
    "rajarhat": "Rajarhat",
    "salt lake": "Salt Lake",
    "garia": "Garia",
    "behala": "Behala",
    "vip nagar": "VIP Nagar",
    "chinar park": "Chinar Park",
    "nayabad": "Nayabad",
    "dum dum": "Dum Dum",
    "barasat": "Barasat",
    "howrah": "Howrah",
    "shyambazar": "Shyambazar",
    "beleghata": "Beleghata",
    "intally": "Intally",
    "rash behari avenue": "Rash Behari Avenue",
    "lake market": "Lake Market",
    "jadavpur": "Jadavpur",
    "bijoygarh": "Bijoygarh",
    "tiljala": "Tiljala",
    "kankurgachi": "Kankurgachi",
    "sealdah": "Sealdah",
    "haridevpur": "Haridevpur",
    "sodepur": "Sodepur",
    "sonarpur": "Sonarpur",
    "madhyamgram": "Madhyamgram",
    "belgharia": "Belgharia",
    "barrackpore": "Barrackpore",
    "bidhan nagar": "Bidhan Nagar",
    "tollygunge": "Tollygunge",
    "ballygunge": "Ballygunge",
    "alipore": "Alipore"
}

def clean_price(price):
    price = price.replace(",", "")
    
    # Extract number (handles Lac/Cr roughly)
    if "Cr" in price:
        num = float(re.findall(r'\d+\.?\d*', price)[0])
        return int(num * 10000000)
    elif "Lac" in price:
        num = float(re.findall(r'\d+\.?\d*', price)[0])
        return int(num * 100000)
    
    return None


def extract_sqft(area):
    match = re.search(r'(\d+)\s*sqft', area)
    return int(match.group(1)) if match else None

def extract_location(text):
    
    text = text.lower()
    
    for key, value in LOCATION_MAP.items():
        if key in text:
            return value
    
    return text

def clean_data(df):
    df["price"] = df["price"].apply(clean_price)
    df["sqft"] = df["area"].apply(extract_sqft)
    df["location"] = df["location_text"].apply(extract_location)

    # ✅ Only drop critical fields
    df = df.dropna(subset=["price", "sqft"])

    df["metro_distance_km"] = 5
    df["hospital_distance_km"] = 5
    df["school_distance_km"] = 5
    df["college_distance_km"] = 5
    df["bus_stop_distance_km"] = 5
    df["railway_distance_km"] = 5
    df["police_distance_km"] = 5
    df["postoffice_distance_km"] = 5

    print("DEBUG LOCATIONS:")
    print(df["location"].unique())
    
    # --- OTHER FEATURES ---
    df["price_per_sqft"] = df["price"] / df["sqft"]
    df["location_score"] = df["location"].apply(get_location_score)

    df["livability_score"] = df.apply(compute_livability, axis=1)

    return df

def get_location_score(location):
    """
    Returns a score from 10 to 5 based on the cost of living 
    for specific locations in Kolkata.
    """
    scores = {
        # Category 10: Elite residential hubs
        "Alipore": 10, 
        "Ballygunge": 10,

        # Category 9: Planned townships and prime South Kolkata
        "Salt Lake": 9, 
        "New Town": 9, 
        "Rash Behari Avenue": 9, 
        "Lake Market": 9,

        # Category 8: Established residential with high demand
        "Tollygunge": 8, 
        "Kankurgachi": 8, 
        "Bidhan Nagar": 8, 
        "Jadavpur": 8, 
        "Beleghata": 8,

        # Category 7: Popular residential zones
        "Rajarhat": 7, 
        "Behala": 7, 
        "Garia": 7, 
        "VIP Nagar": 7, 
        "Chinar Park": 7, 
        "Shyambazar": 7, 
        "Sealdah": 7,

        # Category 6: Emerging or high-density residential
        "Dum Dum": 6, 
        "Nayabad": 6, 
        "Bijoygarh": 6, 
        "Intally": 6, 
        "Tiljala": 6, 
        "Haridevpur": 6,
        
        # Category 5: Extended suburbs and budget-friendly zones
        "Barasat": 5,
        "Howrah": 5,
        "Sodepur": 5,
        "Sonarpur": 5,
        "Madhyamgram": 5,
        "Belgharia": 5,
        "Barrackpore": 5
    }

    # Returns the score if found, otherwise defaults to 5
    return scores.get(location, 4)

def compute_livability(row):
    distances = [
        row["metro_distance_km"],
        row["railway_distance_km"],
        row["bus_stop_distance_km"],
        row["hospital_distance_km"],
        row["school_distance_km"],
        row["college_distance_km"],
        row["police_distance_km"],
        row["postoffice_distance_km"]
    ]

    # Remove None values
    distances = [d for d in distances if d is not None and not math.isnan(d)]


    if not distances:
        return 0

    avg_dist = sum(distances) / len(distances)

    # NORMALIZED SCORING
    score = 10 * (1 / (1 + avg_dist / 2))

    return round(score, 2)
