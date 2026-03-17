"""Database seed script — populates FalkorDB with realistic travel data.

Run from the backend directory:
    python -m db.seed
"""

import logging
import sys

# Ensure Unicode output works on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from datetime import date, datetime, timezone
from typing import Any
from uuid import uuid4

from core.security import hash_password
from db.connection import _connect_with_retry  # noqa: PLC2701 — intentional internal use

logging.basicConfig(level=logging.WARNING)

# ── Seed data ─────────────────────────────────────────────────────────────────

_CATEGORIES: list[dict] = [
    {"id": str(uuid4()), "name": "Museum",       "icon": "🏛️"},
    {"id": str(uuid4()), "name": "Nature",        "icon": "🌿"},
    {"id": str(uuid4()), "name": "Food & Drink",  "icon": "🍽️"},
]

_SEASONS: list[dict] = [
    {
        "id": str(uuid4()), "name": "Spring", "months": [3, 4, 5],
        "avg_temp_c": 15.0, "weather_description": "Mild temperatures and blooming flora",
    },
    {
        "id": str(uuid4()), "name": "Summer", "months": [6, 7, 8],
        "avg_temp_c": 27.0, "weather_description": "Hot and sunny with long days",
    },
    {
        "id": str(uuid4()), "name": "Autumn", "months": [9, 10, 11],
        "avg_temp_c": 13.0, "weather_description": "Cool breezes and colourful foliage",
    },
    {
        "id": str(uuid4()), "name": "Winter", "months": [12, 1, 2],
        "avg_temp_c": 3.0,  "weather_description": "Cold, festive, and often snowy",
    },
]

_TAGS: list[dict] = [
    {"id": str(uuid4()), "name": "family-friendly", "color": "#4CAF50"},
    {"id": str(uuid4()), "name": "romantic",         "color": "#E91E63"},
    {"id": str(uuid4()), "name": "budget",           "color": "#FF9800"},
    {"id": str(uuid4()), "name": "adventure",        "color": "#9C27B0"},
    {"id": str(uuid4()), "name": "cultural",         "color": "#2196F3"},
    {"id": str(uuid4()), "name": "foodie",           "color": "#FF5722"},
]

# Each destination entry: base properties + best_seasons list
_DESTINATIONS: list[dict] = [
    {
        "name": "Istanbul",   "country": "Turkey",
        "lat": 41.0082,       "lng": 28.9784,
        "description": "Transcontinental city bridging Europe and Asia with millennia of history.",
        "best_seasons": ["Summer", "Autumn"],
    },
    {
        "name": "Paris",      "country": "France",
        "lat": 48.8566,       "lng": 2.3522,
        "description": "The City of Light, famed for art, cuisine, and the Eiffel Tower.",
        "best_seasons": ["Spring", "Summer"],
    },
    {
        "name": "Barcelona",  "country": "Spain",
        "lat": 41.3851,       "lng": 2.1734,
        "description": "Vibrant Catalan capital with Gaudí architecture and golden beaches.",
        "best_seasons": ["Summer"],
    },
    {
        "name": "Rome",       "country": "Italy",
        "lat": 41.9028,       "lng": 12.4964,
        "description": "The Eternal City, home to the Colosseum, Vatican, and world-class cuisine.",
        "best_seasons": ["Spring", "Autumn"],
    },
    {
        "name": "Tokyo",      "country": "Japan",
        "lat": 35.6762,       "lng": 139.6503,
        "description": "Ultra-modern metropolis seamlessly blending ancient temples and neon streets.",
        "best_seasons": ["Spring", "Autumn"],
    },
    {
        "name": "New York",   "country": "USA",
        "lat": 40.7128,       "lng": -74.0060,
        "description": "The city that never sleeps, featuring iconic skylines and cultural diversity.",
        "best_seasons": ["Summer"],
    },
    {
        "name": "Bali",       "country": "Indonesia",
        "lat": -8.3405,       "lng": 115.0920,
        "description": "Tropical island paradise with rice terraces, temples, and surf spots.",
        "best_seasons": ["Summer"],
    },
    {
        "name": "Prague",     "country": "Czech Republic",
        "lat": 50.0755,       "lng": 14.4378,
        "description": "The City of a Hundred Spires with Gothic architecture and vibrant nightlife.",
        "best_seasons": ["Summer"],
    },
    {
        "name": "Amsterdam",  "country": "Netherlands",
        "lat": 52.3676,       "lng": 4.9041,
        "description": "Charming canal city celebrated for museums, cycling culture, and tulip fields.",
        "best_seasons": ["Spring", "Summer"],
    },
    {
        "name": "Lisbon",     "country": "Portugal",
        "lat": 38.7223,       "lng": -9.1393,
        "description": "Sun-drenched capital perched on seven hills with Fado music and pastéis de nata.",
        "best_seasons": ["Summer"],
    },
]

# Activities: 2 per destination, keyed by destination name
_ACTIVITIES: dict[str, list[dict]] = {
    "Istanbul": [
        {
            "name": "Topkapi Palace Tour",
            "description": "Explore the opulent palace that was home to Ottoman sultans for four centuries.",
            "duration_hours": 3.0, "price": 25.0, "address": "Topkapı Sarayı, Fatih, Istanbul",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Bosphorus Sunset Cruise",
            "description": "Sail between two continents and watch the city skyline glow at dusk.",
            "duration_hours": 2.0, "price": 30.0, "address": "Eminönü Ferry Terminal, Istanbul",
            "categories": ["Nature"], "tags": ["romantic", "family-friendly"],
        },
    ],
    "Paris": [
        {
            "name": "Louvre Museum Visit",
            "description": "Discover masterpieces including the Mona Lisa and Venus de Milo.",
            "duration_hours": 4.0, "price": 17.0, "address": "Rue de Rivoli, 75001 Paris",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Seine River Picnic Walk",
            "description": "Stroll along the Seine's quays and enjoy a classic Parisian picnic.",
            "duration_hours": 2.5, "price": 0.0, "address": "Quai de la Tournelle, Paris",
            "categories": ["Nature"], "tags": ["romantic", "budget"],
        },
    ],
    "Barcelona": [
        {
            "name": "Sagrada Família Tour",
            "description": "Gaudí's unfinished basilica — a UNESCO World Heritage masterpiece.",
            "duration_hours": 2.0, "price": 26.0, "address": "C/ de Mallorca 401, Barcelona",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Barceloneta Beach Day",
            "description": "Relax on Barcelona's famous urban beach with the Mediterranean at your feet.",
            "duration_hours": 4.0, "price": 0.0, "address": "Barceloneta, Barcelona",
            "categories": ["Nature"], "tags": ["budget", "family-friendly"],
        },
    ],
    "Rome": [
        {
            "name": "Colosseum & Roman Forum",
            "description": "Step inside ancient Rome's most iconic amphitheatre and civic centre.",
            "duration_hours": 3.5, "price": 18.0, "address": "Piazza del Colosseo 1, Rome",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Trastevere Food Walk",
            "description": "Taste traditional Roman street food through the cobblestone alleys of Trastevere.",
            "duration_hours": 2.5, "price": 40.0, "address": "Piazza Santa Maria in Trastevere, Rome",
            "categories": ["Food & Drink"], "tags": ["foodie", "romantic"],
        },
    ],
    "Tokyo": [
        {
            "name": "Senso-ji Temple & Asakusa",
            "description": "Visit Tokyo's oldest temple and browse traditional Nakamise shopping street.",
            "duration_hours": 2.0, "price": 0.0, "address": "2-3-1 Asakusa, Taito, Tokyo",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Tsukiji Outer Market Food Tour",
            "description": "Sample fresh sushi, tamagoyaki, and street snacks at the legendary fish market.",
            "duration_hours": 2.0, "price": 35.0, "address": "4-16-2 Tsukiji, Chuo, Tokyo",
            "categories": ["Food & Drink"], "tags": ["foodie", "budget"],
        },
    ],
    "New York": [
        {
            "name": "Metropolitan Museum of Art",
            "description": "One of the world's largest art museums with over 5,000 years of culture.",
            "duration_hours": 4.0, "price": 30.0, "address": "1000 Fifth Ave, New York, NY",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Central Park Cycling",
            "description": "Rent a bike and explore 843 acres of green space in the heart of Manhattan.",
            "duration_hours": 3.0, "price": 20.0, "address": "Central Park, New York, NY",
            "categories": ["Nature"], "tags": ["adventure", "family-friendly"],
        },
    ],
    "Bali": [
        {
            "name": "Tegalalang Rice Terrace Trek",
            "description": "Hike through emerald green rice terraces carved into Bali's volcanic hillside.",
            "duration_hours": 3.0, "price": 10.0, "address": "Tegalalang, Gianyar, Bali",
            "categories": ["Nature"], "tags": ["adventure", "romantic"],
        },
        {
            "name": "Ubud Cooking Class",
            "description": "Learn to cook authentic Balinese dishes using fresh market ingredients.",
            "duration_hours": 4.0, "price": 45.0, "address": "Ubud, Gianyar, Bali",
            "categories": ["Food & Drink"], "tags": ["foodie", "cultural"],
        },
    ],
    "Prague": [
        {
            "name": "Prague Castle Complex",
            "description": "Explore the largest ancient castle in the world overlooking the Vltava river.",
            "duration_hours": 3.0, "price": 15.0, "address": "Hradčany, 119 08 Prague",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Old Town Square Night Walk",
            "description": "Watch the Astronomical Clock chime and admire Gothic spires by night.",
            "duration_hours": 1.5, "price": 0.0, "address": "Staroměstské nám., Prague 1",
            "categories": ["Nature"], "tags": ["romantic", "budget"],
        },
    ],
    "Amsterdam": [
        {
            "name": "Rijksmuseum Tour",
            "description": "Dutch Golden Age paintings including Rembrandt and Vermeer masterpieces.",
            "duration_hours": 3.0, "price": 22.5, "address": "Museumstraat 1, Amsterdam",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "Canal Ring Boat Tour",
            "description": "Glide through UNESCO-listed 17th-century canal rings on a classic saloon boat.",
            "duration_hours": 1.5, "price": 18.0, "address": "Prins Hendrikkade, Amsterdam",
            "categories": ["Nature"], "tags": ["romantic", "family-friendly"],
        },
    ],
    "Lisbon": [
        {
            "name": "Jerónimos Monastery",
            "description": "Magnificent Manueline monastery and resting place of Vasco da Gama.",
            "duration_hours": 2.0, "price": 10.0, "address": "Praça do Império, Belém, Lisbon",
            "categories": ["Museum"], "tags": ["cultural", "family-friendly"],
        },
        {
            "name": "LX Factory Market & Food",
            "description": "Wander a repurposed industrial complex packed with street food, crafts, and music.",
            "duration_hours": 3.0, "price": 0.0, "address": "R. Rodrigues de Faria 103, Lisbon",
            "categories": ["Food & Drink"], "tags": ["foodie", "budget"],
        },
    ],
}

_RESTAURANTS: dict[str, list[dict]] = {
    "Istanbul": [
        {"name": "Mikla", "cuisine_type": "Modern Turkish", "price_range": "luxury",
         "address": "Meşrutiyet Cad. 15, Beyoğlu, Istanbul", "rating": 4.7},
        {"name": "Karaköy Lokantası", "cuisine_type": "Traditional Turkish", "price_range": "mid",
         "address": "Kemankeş Cad. 37A, Karaköy, Istanbul", "rating": 4.4},
    ],
    "Paris": [
        {"name": "Le Comptoir du Relais", "cuisine_type": "French Bistro", "price_range": "mid",
         "address": "9 Carrefour de l'Odéon, 75006 Paris", "rating": 4.5},
        {"name": "L'Ami Jean", "cuisine_type": "Basque", "price_range": "mid",
         "address": "27 Rue Malar, 75007 Paris", "rating": 4.6},
    ],
    "Barcelona": [
        {"name": "Bar Cañete", "cuisine_type": "Catalan Tapas", "price_range": "mid",
         "address": "C/ de la Unió 17, Barcelona", "rating": 4.5},
    ],
    "Rome": [
        {"name": "Da Enzo al 29", "cuisine_type": "Roman", "price_range": "mid",
         "address": "Via dei Vascellari 29, Trastevere, Rome", "rating": 4.6},
        {"name": "Supplì Roma", "cuisine_type": "Italian Street Food", "price_range": "budget",
         "address": "Via di San Francesco a Ripa 137, Rome", "rating": 4.3},
    ],
    "Tokyo": [
        {"name": "Sukiyabashi Jiro Honten", "cuisine_type": "Japanese Sushi", "price_range": "luxury",
         "address": "4 Chome-2-15 Ginza, Chuo, Tokyo", "rating": 4.9},
        {"name": "Ichiran Shibuya", "cuisine_type": "Japanese Ramen", "price_range": "budget",
         "address": "1-22-7 Jinnan, Shibuya, Tokyo", "rating": 4.4},
    ],
    "New York": [
        {"name": "Katz's Delicatessen", "cuisine_type": "American Deli", "price_range": "mid",
         "address": "205 E Houston St, New York, NY", "rating": 4.4},
        {"name": "Le Bernardin", "cuisine_type": "French Seafood", "price_range": "luxury",
         "address": "155 W 51st St, New York, NY", "rating": 4.8},
    ],
    "Bali": [
        {"name": "Locavore", "cuisine_type": "Modern Indonesian", "price_range": "luxury",
         "address": "Jl. Dewi Sita, Ubud, Bali", "rating": 4.7},
    ],
    "Prague": [
        {"name": "Lokál", "cuisine_type": "Czech", "price_range": "budget",
         "address": "Dlouhá 33, Staré Město, Prague", "rating": 4.3},
        {"name": "Field", "cuisine_type": "Modern European", "price_range": "luxury",
         "address": "U Milosrdných 12, Prague 1", "rating": 4.6},
    ],
    "Amsterdam": [
        {"name": "De Kas", "cuisine_type": "Dutch Farm-to-Table", "price_range": "luxury",
         "address": "Kamerlingh Onneslaan 3, Amsterdam", "rating": 4.6},
        {"name": "Brouwerij 't IJ", "cuisine_type": "Dutch Pub Food", "price_range": "budget",
         "address": "Funenkade 7, Amsterdam", "rating": 4.3},
    ],
    "Lisbon": [
        {"name": "Belcanto", "cuisine_type": "Portuguese Fine Dining", "price_range": "luxury",
         "address": "R. Serpa Pinto 10A, Lisbon", "rating": 4.8},
        {"name": "Time Out Market", "cuisine_type": "Portuguese Street Food", "price_range": "mid",
         "address": "Av. 24 de Julho 49, Lisbon", "rating": 4.4},
    ],
}

_ACCOMMODATIONS: dict[str, list[dict]] = {
    "Istanbul": [
        {"name": "Four Seasons Sultanahmet", "type": "hotel", "star_rating": 5,
         "price_per_night": 420.0, "address": "Tevkifhane Sok. 1, Sultanahmet, Istanbul"},
        {"name": "Istanbul Hostel", "type": "hostel", "star_rating": 2,
         "price_per_night": 25.0, "address": "Akbıyık Cad. 33, Sultanahmet, Istanbul"},
    ],
    "Paris": [
        {"name": "Hôtel Plaza Athénée", "type": "hotel", "star_rating": 5,
         "price_per_night": 850.0, "address": "25 Avenue Montaigne, 75008 Paris"},
        {"name": "Le Marais Apartment", "type": "apartment", "star_rating": 3,
         "price_per_night": 130.0, "address": "12 Rue de Bretagne, 75003 Paris"},
    ],
    "Barcelona": [
        {"name": "Hotel Arts Barcelona", "type": "hotel", "star_rating": 5,
         "price_per_night": 390.0, "address": "C/ de la Marina 19-21, Barcelona"},
        {"name": "Gothic Quarter Hostel", "type": "hostel", "star_rating": 2,
         "price_per_night": 20.0, "address": "C/ Ferran 36, Barcelona"},
    ],
    "Rome": [
        {"name": "Hotel de Russie", "type": "hotel", "star_rating": 5,
         "price_per_night": 480.0, "address": "Via del Babuino 9, Rome"},
        {"name": "Trastevere Apartment", "type": "apartment", "star_rating": 3,
         "price_per_night": 95.0, "address": "Via della Lungaretta 55, Rome"},
    ],
    "Tokyo": [
        {"name": "Park Hyatt Tokyo", "type": "hotel", "star_rating": 5,
         "price_per_night": 560.0, "address": "3-7-1-2 Nishi-Shinjuku, Shinjuku, Tokyo"},
        {"name": "Khaosan Tokyo Origami", "type": "hostel", "star_rating": 2,
         "price_per_night": 28.0, "address": "1-20-4 Asakusa, Taito, Tokyo"},
    ],
    "New York": [
        {"name": "The Plaza Hotel", "type": "hotel", "star_rating": 5,
         "price_per_night": 700.0, "address": "768 Fifth Ave, New York, NY"},
        {"name": "HI NYC Hostel", "type": "hostel", "star_rating": 2,
         "price_per_night": 45.0, "address": "891 Amsterdam Ave, New York, NY"},
    ],
    "Bali": [
        {"name": "COMO Uma Ubud", "type": "hotel", "star_rating": 5,
         "price_per_night": 310.0, "address": "Jl. Raya Sanggingan, Ubud, Bali"},
        {"name": "Ubud Backpacker", "type": "hostel", "star_rating": 1,
         "price_per_night": 12.0, "address": "Jl. Monkey Forest, Ubud, Bali"},
    ],
    "Prague": [
        {"name": "Augustine Hotel", "type": "hotel", "star_rating": 5,
         "price_per_night": 280.0, "address": "Letenská 12/33, Malá Strana, Prague"},
        {"name": "Czech Inn Hostel", "type": "hostel", "star_rating": 2,
         "price_per_night": 18.0, "address": "Francouzská 76, Vinohrady, Prague"},
    ],
    "Amsterdam": [
        {"name": "Conservatorium Hotel", "type": "hotel", "star_rating": 5,
         "price_per_night": 450.0, "address": "Van Baerlestraat 27, Amsterdam"},
        {"name": "Canal House Apartment", "type": "apartment", "star_rating": 4,
         "price_per_night": 175.0, "address": "Herengracht 120, Amsterdam"},
    ],
    "Lisbon": [
        {"name": "Bairro Alto Hotel", "type": "hotel", "star_rating": 5,
         "price_per_night": 380.0, "address": "Praça Luís de Camões 2, Lisbon"},
        {"name": "Lisbon Lounge Hostel", "type": "hostel", "star_rating": 2,
         "price_per_night": 22.0, "address": "R. de São Nicolau 41, Lisbon"},
    ],
}

_FESTIVALS: dict[str, dict] = {
    "Istanbul": {
        "name": "Istanbul Music Festival",
        "description": "Month-long celebration of classical and world music at historic venues.",
        "start_date": "2025-06-01", "end_date": "2025-06-30",
        "is_recurring": True, "ticket_price": 35.0,
    },
    "Paris": {
        "name": "Fête de la Musique",
        "description": "Free open-air concerts across every neighbourhood on the summer solstice.",
        "start_date": "2025-06-21", "end_date": "2025-06-22",
        "is_recurring": True, "ticket_price": None,
    },
    "Barcelona": {
        "name": "La Mercè Festival",
        "description": "Barcelona's biggest street festival honouring its patron saint with concerts and castellers.",
        "start_date": "2025-09-20", "end_date": "2025-09-25",
        "is_recurring": True, "ticket_price": None,
    },
    "Rome": {
        "name": "Rome Film Festival",
        "description": "International cinema showcase screening world premieres at the Auditorium Parco della Musica.",
        "start_date": "2025-10-15", "end_date": "2025-10-25",
        "is_recurring": True, "ticket_price": 12.0,
    },
    "Tokyo": {
        "name": "Sumida River Fireworks",
        "description": "One of Tokyo's oldest and grandest fireworks displays lighting up the summer sky.",
        "start_date": "2025-07-26", "end_date": "2025-07-27",
        "is_recurring": True, "ticket_price": None,
    },
    "New York": {
        "name": "NYC Pride March",
        "description": "One of the world's largest Pride celebrations marching through Manhattan.",
        "start_date": "2025-06-29", "end_date": "2025-06-30",
        "is_recurring": True, "ticket_price": None,
    },
    "Bali": {
        "name": "Bali Arts Festival",
        "description": "Month-long showcase of traditional Balinese dance, music, and crafts.",
        "start_date": "2025-06-14", "end_date": "2025-07-12",
        "is_recurring": True, "ticket_price": 5.0,
    },
    "Prague": {
        "name": "Prague Spring International Music Festival",
        "description": "Prestigious classical music festival opening with Smetana's Má vlast.",
        "start_date": "2025-05-12", "end_date": "2025-06-04",
        "is_recurring": True, "ticket_price": 25.0,
    },
    "Amsterdam": {
        "name": "King's Day Amsterdam",
        "description": "The Netherlands' national day — the entire city turns orange for open-air parties.",
        "start_date": "2025-04-27", "end_date": "2025-04-28",
        "is_recurring": True, "ticket_price": None,
    },
    "Lisbon": {
        "name": "Festas de Lisboa",
        "description": "June festival honouring Saint Anthony with sardine grills and street parades.",
        "start_date": "2025-06-01", "end_date": "2025-06-30",
        "is_recurring": True, "ticket_price": None,
    },
}

_USERS: list[dict] = [
    {"name": "Alice Martin",   "email": "alice@example.com"},
    {"name": "Bob Rossi",      "email": "bob@example.com"},
    {"name": "Ceren Yıldız",   "email": "ceren@example.com"},
    {"name": "David Park",     "email": "david@example.com"},
    {"name": "Elena Novak",    "email": "elena@example.com"},
]

# VISITED edges: user email → list of destination names
_VISITED: dict[str, list[str]] = {
    "alice@example.com":  ["Istanbul", "Paris", "Barcelona"],
    "bob@example.com":    ["Tokyo", "New York", "Bali", "Prague"],
    "ceren@example.com":  ["Rome", "Amsterdam", "Lisbon"],
    "david@example.com":  ["Istanbul", "Tokyo", "Paris", "Barcelona", "Rome"],
    "elena@example.com":  ["New York", "Bali", "Prague", "Amsterdam"],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(db: Any, cypher: str, params: dict | None = None) -> Any:
    """Execute *cypher* with *params* and return the QueryResult."""
    return db.query(cypher, params or {})


# ── Step functions ────────────────────────────────────────────────────────────

def _clean(db: Any) -> None:
    _run(db, "MATCH (n) DETACH DELETE n")
    print("✓ Veritabanı temizlendi")


def _create_categories(db: Any) -> None:
    for cat in _CATEGORIES:
        _run(
            db,
            "CREATE (:Category {id: $id, name: $name, icon: $icon})",
            cat,
        )
    print(f"✓ {len(_CATEGORIES)} Category oluşturuldu")


def _create_seasons(db: Any) -> None:
    for s in _SEASONS:
        _run(
            db,
            "CREATE (:Season {id: $id, name: $name, months: $months, "
            "avg_temp_c: $avg_temp_c, weather_description: $weather_description})",
            s,
        )
    print(f"✓ {len(_SEASONS)} Season oluşturuldu")


def _create_tags(db: Any) -> None:
    for tag in _TAGS:
        _run(
            db,
            "CREATE (:Tag {id: $id, name: $name, color: $color})",
            tag,
        )
    print(f"✓ {len(_TAGS)} Tag oluşturuldu")


def _create_destinations(db: Any) -> dict[str, str]:
    """Create Destination nodes and BEST_IN edges. Returns {name: id} mapping."""
    dest_ids: dict[str, str] = {}

    for dest in _DESTINATIONS:
        dest_id = str(uuid4())
        dest_ids[dest["name"]] = dest_id
        _run(
            db,
            "CREATE (:Destination {id: $id, name: $name, country: $country, "
            "description: $description, lat: $lat, lng: $lng, created_at: $ca})",
            {
                "id": dest_id,
                "name": dest["name"],
                "country": dest["country"],
                "description": dest["description"],
                "lat": dest["lat"],
                "lng": dest["lng"],
                "ca": _now(),
            },
        )
        for season_name in dest["best_seasons"]:
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}), (s:Season {name: $season_name}) "
                "CREATE (d)-[:BEST_IN]->(s)",
                {"dest_id": dest_id, "season_name": season_name},
            )

    print(f"✓ {len(_DESTINATIONS)} Destination oluşturuldu (BEST_IN kenarları dahil)")
    return dest_ids


def _create_activities(db: Any, dest_ids: dict[str, str]) -> dict[str, str]:
    """Create Activity nodes with category/tag edges. Returns {name: id} mapping."""
    act_ids: dict[str, str] = {}
    total = 0

    for dest_name, activities in _ACTIVITIES.items():
        dest_id = dest_ids[dest_name]
        for act in activities:
            act_id = str(uuid4())
            act_ids[act["name"]] = act_id
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (a:Activity {id: $id, name: $name, description: $description, "
                "duration_hours: $duration_hours, price: $price, address: $address, "
                "destination_id: $dest_id, categories: [], tags: [], created_at: $ca}) "
                "CREATE (d)-[:HAS_ACTIVITY]->(a) "
                "CREATE (a)-[:LOCATED_IN]->(d)",
                {
                    "dest_id": dest_id,
                    "id": act_id,
                    "name": act["name"],
                    "description": act["description"],
                    "duration_hours": act["duration_hours"],
                    "price": act["price"],
                    "address": act["address"],
                    "ca": _now(),
                },
            )
            for cat_name in act["categories"]:
                _run(
                    db,
                    "MATCH (a:Activity {id: $act_id}), (c:Category {name: $cat_name}) "
                    "CREATE (a)-[:IN_CATEGORY]->(c)",
                    {"act_id": act_id, "cat_name": cat_name},
                )
            for tag_name in act["tags"]:
                _run(
                    db,
                    "MATCH (a:Activity {id: $act_id}), (t:Tag {name: $tag_name}) "
                    "CREATE (a)-[:HAS_TAG]->(t)",
                    {"act_id": act_id, "tag_name": tag_name},
                )
            total += 1

    print(f"✓ {total} Activity oluşturuldu (IN_CATEGORY ve HAS_TAG kenarları dahil)")
    return act_ids


def _create_restaurants(db: Any, dest_ids: dict[str, str]) -> None:
    total = 0
    for dest_name, restaurants in _RESTAURANTS.items():
        dest_id = dest_ids[dest_name]
        for rest in restaurants:
            rest_id = str(uuid4())
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (r:Restaurant {id: $id, name: $name, cuisine_type: $cuisine_type, "
                "price_range: $price_range, address: $address, rating: $rating, "
                "destination_id: $dest_id, created_at: $ca}) "
                "CREATE (d)-[:HAS_RESTAURANT]->(r)",
                {
                    "dest_id": dest_id,
                    "id": rest_id,
                    "name": rest["name"],
                    "cuisine_type": rest["cuisine_type"],
                    "price_range": rest["price_range"],
                    "address": rest["address"],
                    "rating": rest.get("rating"),
                    "ca": _now(),
                },
            )
            total += 1
    print(f"✓ {total} Restaurant oluşturuldu")


def _create_accommodations(db: Any, dest_ids: dict[str, str]) -> dict[str, str]:
    """Create Accommodation nodes. Returns {name: id} mapping."""
    acc_ids: dict[str, str] = {}
    total = 0
    for dest_name, accommodations in _ACCOMMODATIONS.items():
        dest_id = dest_ids[dest_name]
        for acc in accommodations:
            acc_id = str(uuid4())
            acc_ids[acc["name"]] = acc_id
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (a:Accommodation {id: $id, name: $name, type: $type, "
                "star_rating: $star_rating, price_per_night: $price_per_night, "
                "address: $address, destination_id: $dest_id, created_at: $ca}) "
                "CREATE (d)-[:HAS_ACCOMMODATION]->(a) "
                "CREATE (a)-[:LOCATED_IN]->(d)",
                {
                    "dest_id": dest_id,
                    "id": acc_id,
                    "name": acc["name"],
                    "type": acc["type"],
                    "star_rating": acc["star_rating"],
                    "price_per_night": acc["price_per_night"],
                    "address": acc["address"],
                    "ca": _now(),
                },
            )
            total += 1
    print(f"✓ {total} Accommodation oluşturuldu (LOCATED_IN kenarları dahil)")
    return acc_ids


def _create_festivals(db: Any, dest_ids: dict[str, str]) -> None:
    total = 0
    for dest_name, fest in _FESTIVALS.items():
        dest_id = dest_ids[dest_name]
        fest_id = str(uuid4())
        _run(
            db,
            "MATCH (d:Destination {id: $dest_id}) "
            "CREATE (f:Festival {id: $id, name: $name, description: $description, "
            "start_date: $start_date, end_date: $end_date, "
            "is_recurring: $is_recurring, ticket_price: $ticket_price, "
            "destination_id: $dest_id, created_at: $ca}) "
            "CREATE (d)-[:HAS_FESTIVAL]->(f)",
            {
                "dest_id": dest_id,
                "id": fest_id,
                "name": fest["name"],
                "description": fest["description"],
                "start_date": fest["start_date"],
                "end_date": fest["end_date"],
                "is_recurring": fest["is_recurring"],
                "ticket_price": fest.get("ticket_price"),
                "ca": _now(),
            },
        )
        total += 1
    print(f"✓ {total} Festival oluşturuldu")


def _create_users(db: Any) -> dict[str, str]:
    """Create User nodes. Returns {email: id} mapping."""
    user_ids: dict[str, str] = {}
    pw_hash = hash_password("Test1234!")

    for user in _USERS:
        user_id = str(uuid4())
        user_ids[user["email"]] = user_id
        _run(
            db,
            "CREATE (:User {id: $id, name: $name, email: $email, "
            "password_hash: $ph, created_at: $ca})",
            {
                "id": user_id,
                "name": user["name"],
                "email": user["email"],
                "ph": pw_hash,
                "ca": _now(),
            },
        )
    print(f"✓ {len(_USERS)} User oluşturuldu (şifre: Test1234!)")
    return user_ids


def _create_visited_edges(
    db: Any,
    user_ids: dict[str, str],
    dest_ids: dict[str, str],
) -> None:
    total = 0
    for email, dest_names in _VISITED.items():
        user_id = user_ids[email]
        for dest_name in dest_names:
            dest_id = dest_ids[dest_name]
            _run(
                db,
                "MATCH (u:User {id: $user_id}), (d:Destination {id: $dest_id}) "
                "CREATE (u)-[:VISITED {visited_at: $va}]->(d)",
                {"user_id": user_id, "dest_id": dest_id, "va": _now()},
            )
            total += 1
    print(f"✓ {total} VISITED kenarı oluşturuldu")


def _create_reviews(
    db: Any,
    user_ids: dict[str, str],
    act_ids: dict[str, str],
    acc_ids: dict[str, str],
) -> None:
    # 15 reviews spread across users, activities, and accommodations
    reviews: list[dict] = [
        # Activity reviews
        {"user": "alice@example.com",  "target_name": "Bosphorus Sunset Cruise",
         "target_type": "activity", "rating": 5, "comment": "Absolutely magical — watching the skyline at sunset was unforgettable."},
        {"user": "alice@example.com",  "target_name": "Louvre Museum Visit",
         "target_type": "activity", "rating": 4, "comment": "Overwhelming in the best way. Go early to beat the crowds."},
        {"user": "bob@example.com",    "target_name": "Senso-ji Temple & Asakusa",
         "target_type": "activity", "rating": 5, "comment": "Serene and beautiful even with the crowds. A must-visit in Tokyo."},
        {"user": "bob@example.com",    "target_name": "Tsukiji Outer Market Food Tour",
         "target_type": "activity", "rating": 5, "comment": "Fresh uni and tuna at 8am — my life is complete."},
        {"user": "ceren@example.com",  "target_name": "Trastevere Food Walk",
         "target_type": "activity", "rating": 5, "comment": "The cacio e pepe alone was worth the trip to Rome."},
        {"user": "ceren@example.com",  "target_name": "Canal Ring Boat Tour",
         "target_type": "activity", "rating": 4, "comment": "Lovely way to see the city. The guide knew great stories about every canal house."},
        {"user": "david@example.com",  "target_name": "Topkapi Palace Tour",
         "target_type": "activity", "rating": 4, "comment": "Rich history, stunning views of the Bosphorus from the terraces."},
        {"user": "david@example.com",  "target_name": "Sagrada Família Tour",
         "target_type": "activity", "rating": 5, "comment": "Nothing prepares you for the interior. Gaudí was a genius."},
        {"user": "elena@example.com",  "target_name": "Central Park Cycling",
         "target_type": "activity", "rating": 4, "comment": "A great way to see the park without tourist crowds early in the morning."},
        {"user": "elena@example.com",  "target_name": "Tegalalang Rice Terrace Trek",
         "target_type": "activity", "rating": 5, "comment": "Jaw-dropping views. The sunrise hike is worth every step."},
        # Accommodation reviews
        {"user": "alice@example.com",  "target_name": "Istanbul Hostel",
         "target_type": "accommodation", "rating": 3, "comment": "Clean and friendly staff, but thin walls. Good value for the location."},
        {"user": "bob@example.com",    "target_name": "Khaosan Tokyo Origami",
         "target_type": "accommodation", "rating": 4, "comment": "Spotless hostel, great common areas, 5 mins walk to Senso-ji."},
        {"user": "ceren@example.com",  "target_name": "Trastevere Apartment",
         "target_type": "accommodation", "rating": 5, "comment": "Perfect Rome base. Woke up to the smell of the bakery downstairs every morning."},
        {"user": "david@example.com",  "target_name": "Gothic Quarter Hostel",
         "target_type": "accommodation", "rating": 4, "comment": "Tiny dorms but super social. Met my travel buddy there."},
        {"user": "elena@example.com",  "target_name": "Lisbon Lounge Hostel",
         "target_type": "accommodation", "rating": 5, "comment": "Best hostel I have ever stayed in. The rooftop terrace and free petiscos sealed it."},
    ]

    all_target_ids = {**act_ids, **acc_ids}
    total = 0

    for rev in reviews:
        review_id = str(uuid4())
        user_id = user_ids[rev["user"]]
        target_id = all_target_ids[rev["target_name"]]
        _run(
            db,
            "MATCH (u:User {id: $user_id}) "
            "CREATE (r:Review {id: $id, target_id: $target_id, "
            "target_type: $target_type, rating: $rating, comment: $comment, "
            "created_at: $ca}) "
            "CREATE (u)-[:WROTE]->(r)",
            {
                "user_id": user_id,
                "id": review_id,
                "target_id": target_id,
                "target_type": rev["target_type"],
                "rating": rev["rating"],
                "comment": rev["comment"],
                "ca": _now(),
            },
        )
        # Also create RATES edge from user to the target node for avg_rating queries
        _run(
            db,
            "MATCH (u:User {id: $user_id}), (r:Review {id: $review_id}) "
            "MATCH (target) WHERE target.id = $target_id "
            "CREATE (u)-[:RATES {score: $rating}]->(target)",
            {
                "user_id": user_id,
                "review_id": review_id,
                "target_id": target_id,
                "rating": rev["rating"],
            },
        )
        total += 1

    print(f"✓ {total} Review oluşturuldu (WROTE ve RATES kenarları dahil)")


# ── Entry point ───────────────────────────────────────────────────────────────

def seed() -> None:
    """Run the full seed sequence, aborting on any error."""
    print("FalkorDB'ye bağlanılıyor...")
    db = _connect_with_retry()
    print("✓ Bağlantı kuruldu\n")

    _clean(db)
    _create_categories(db)
    _create_seasons(db)
    _create_tags(db)
    dest_ids = _create_destinations(db)
    act_ids  = _create_activities(db, dest_ids)
    _create_restaurants(db, dest_ids)
    acc_ids  = _create_accommodations(db, dest_ids)
    _create_festivals(db, dest_ids)
    user_ids = _create_users(db)
    _create_visited_edges(db, user_ids, dest_ids)
    _create_reviews(db, user_ids, act_ids, acc_ids)

    print("\n✓ Seed tamamlandı.")


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:
        print(f"\n✗ Seed başarısız: {exc}", file=sys.stderr)
        sys.exit(1)
