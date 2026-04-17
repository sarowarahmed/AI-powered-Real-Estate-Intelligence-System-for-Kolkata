from geopy.distance import geodesic

# Sample Kolkata metro stations (expand later)
METRO_STATIONS = {
    # --- BLUE LINE (North-South) ---
    "Dakshineswar": (22.6548, 88.3582),
    "Baranagar": (22.6433, 88.3654),
    "Noapara": (22.6402, 88.3934),
    "Dum Dum": (22.6246, 88.4250),
    "Belgachia": (22.6042, 88.3811),
    "Shyambazar": (22.6015, 88.3712),
    "Shobhabazar Sutanuti": (22.5947, 88.3662),
    "Girish Park": (22.5855, 88.3615),
    "Mahatma Gandhi Road": (22.5822, 88.3591),
    "Central": (22.5678, 88.3617),
    "Chandni Chowk": (22.5631, 88.3609),
    "Esplanade": (22.5647, 88.3533),
    "Park Street": (22.5534, 88.3503),
    "Maidan": (22.5452, 88.3475),
    "Rabindra Sadan": (22.5381, 88.3456),
    "Netaji Bhavan": (22.5317, 88.3444),
    "Jatin Das Park": (22.5234, 88.3431),
    "Kalighat": (22.5183, 88.3426),
    "Rabindra Sarobar": (22.5085, 88.3461),
    "Mahanayak Uttam Kumar": (22.4951, 88.3459),
    "Netaji": (22.4831, 88.3468),
    "Masterda Surya Sen": (22.4746, 88.3562),
    "Gitanjali": (22.4719, 88.3725),
    "Kavi Nazrul": (22.4678, 88.3845),
    "Shahid Khudiram": (22.4712, 88.3965),
    "Kavi Subhash": (22.4741, 88.3995),

    # --- GREEN LINE (East-West) ---
    "Howrah Maidan": (22.5816, 88.3243),
    "Howrah": (22.5847, 88.3315),
    "Mahakaran": (22.5714, 88.3491),
    "Sealdah": (22.5684, 88.3720),
    "Phoolbagan": (22.5711, 88.3917),
    "Salt Lake Stadium": (22.5714, 88.4064),
    "Bengal Chemical": (22.5794, 88.4082),
    "City Centre": (22.5891, 88.4093),
    "Central Park": (22.5898, 88.4167),
    "Karunamoyee": (22.5878, 88.4233),
    "Salt Lake Sector V": (22.5804, 88.4337),

    # --- PURPLE LINE (Joka-Esplanade) ---
    "Joka": (22.4522, 88.3018),
    "Thakurpukur": (22.4632, 88.3054),
    "Sakher Bazar": (22.4754, 88.3101),
    "Behala Chowrasta": (22.4842, 88.3129),
    "Behala Bazar": (22.4925, 88.3148),
    "Taratala": (22.5034, 88.3182),
    "Majerhat": (22.5184, 88.3246),

    # --- ORANGE LINE (Kavi Subhash-Airport) ---
    "Hemanta Mukhopadhyay": (22.5173, 88.4005),
    "VIP Bazar": (22.5285, 88.4011),
    "Ritwik Ghatak": (22.5372, 88.4022),
    "Barun Sengupta": (22.5434, 88.4036),
    "Beliaghata": (22.5539, 88.4055),

    #Yellow Line (Noapara – Barasat)
    "Noapara": (22.6402, 88.3934),
    "Dum Dum Cantt": (22.6417, 88.4069),
    "Jessore Road": (22.6515, 88.4214),
    "Jai Hind (Airport)": (22.6534, 88.4446),
    "Birati": (22.6683, 88.4371),
    "Michael Nagar": (22.6811, 88.4428),
    "New Barrackpore": (22.6954, 88.4445),
    "Madhyamgram": (22.7011, 88.4526),
    "Hridaypur": (22.7128, 88.4685),
    "Barasat": (22.7214, 88.4851),

    #Pink Line (Baranagar – Barrackpore)
    "Baranagar": (22.6433, 88.3654),
    "Kamarhati": (22.6715, 88.3698),
    "Agarpara": (22.6852, 88.3741),
    "Sodepur": (22.6974, 88.3765),
    "Panihati": (22.7092, 88.3782),
    "Subhash Nagar": (22.7221, 88.3795),
    "Khardah": (22.7294, 88.3802),
    "Tata Gate": (22.7441, 88.3775),
    "Titagarh": (22.7538, 88.3761),
    "Barrackpore": (22.7604, 88.3734)

}

# Approx location coordinates (simple mapping)
LOCATION_COORDS = {
    # Tier 10
    "Alipore": (22.5310, 88.3330),
    "Ballygunge": (22.5280, 88.3650),

    # Tier 9
    "Salt Lake": (22.5800, 88.4200),
    "New Town": (22.5750, 88.4786),
    "Rash Behari Avenue": (22.5180, 88.3540),
    "Lake Market": (22.5170, 88.3510),

    # Tier 8
    "Tollygunge": (22.4950, 88.3458),
    "Kankurgachi": (22.5790, 88.3890),
    "Bidhan Nagar": (22.5900, 88.3900),
    "Jadavpur": (22.4950, 88.3700),
    "Beleghata": (22.5650, 88.3900),

    # Tier 7
    "Rajarhat": (22.6100, 88.4800),
    "Behala": (22.5000, 88.3150),
    "Garia": (22.4620, 88.4000),
    "VIP Nagar": (22.5380, 88.4000),
    "Chinar Park": (22.6250, 88.4500),
    "Shyambazar": (22.6020, 88.3710),
    "Sealdah": (22.5670, 88.3710),

    # Tier 6
    "Dum Dum": (22.6200, 88.4000),
    "Nayabad": (22.4810, 88.4110),
    "Bijoygarh": (22.4920, 88.3640),
    "Intally": (22.5550, 88.3680),
    "Tiljala": (22.5380, 88.3840),
    "Haridevpur": (22.4830, 88.3380),

    # Tier 5
    "Barasat": (22.7200, 88.4800),
    "Howrah": (22.5850, 88.3300),
    "Sodepur": (22.6950, 88.3830),
    "Sonarpur": (22.4350, 88.4300),
    "Madhyamgram": (22.6900, 88.4500),
    "Belgharia": (22.6570, 88.3850),
    "Barrackpore": (22.7600, 88.3700)
}

def get_distance_to_metro(location):
    if location not in LOCATION_COORDS:
        return None

    property_coord = LOCATION_COORDS[location]

    min_distance = float("inf")

    for metro, coord in METRO_STATIONS.items():
        dist = geodesic(property_coord, coord).km
        min_distance = min(min_distance, dist)

    return round(min_distance, 2)