"""FalkorDB seed script — real Turkey data for TravelGraph."""
from __future__ import annotations

import random
from datetime import datetime, timezone
from uuid import uuid4

from core.security import hash_password
from db.connection import get_db


def uid() -> str:
    return str(uuid4())


def main() -> None:
    db = next(get_db())
    print("Clearing existing database...")
    db.query("MATCH (n) DETACH DELETE n")
    print("Database cleared.\n")

    # ── Users ──────────────────────────────────────────────────────────────────
    users: list[str] = []
    print("Creating 5 Users...")
    for i in range(1, 6):
        user_id = uid()
        db.query(
            "CREATE (u:User {id: $id, email: $email, name: $name, "
            "password_hash: $ph, created_at: $ca})",
            {
                "id": user_id,
                "email": f"user{i}@example.com",
                "name": f"Traveler {i}",
                "ph": hash_password("password123"),
                "ca": datetime.now(timezone.utc).isoformat(),
            },
        )
        users.append(user_id)

    # ── Destinations (10 Turkey cities) ────────────────────────────────────────
    dest_data = [
        {
            "name": "Istanbul",
            "country": "Turkey",
            "lat": 41.0082,
            "lng": 28.9784,
            "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=800",
            "description": "The city where East meets West, spanning two continents across the Bosphorus.",
        },
        {
            "name": "Cappadocia",
            "country": "Turkey",
            "lat": 38.6431,
            "lng": 34.8289,
            "image_url": "https://images.unsplash.com/photo-1570939274717-7eda259b50ed?w=800",
            "description": "Famous for its unique fairy chimneys, hot air balloons and underground cities.",
        },
        {
            "name": "Antalya",
            "country": "Turkey",
            "lat": 36.8969,
            "lng": 30.7133,
            "image_url": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=800",
            "description": "Gateway to the Turkish Riviera with stunning beaches and ancient ruins.",
        },
        {
            "name": "Ephesus",
            "country": "Turkey",
            "lat": 37.9395,
            "lng": 27.3417,
            "image_url": "https://images.unsplash.com/photo-1589308078059-be1415eab4c3?w=800",
            "description": "One of the best-preserved ancient Greek cities and a UNESCO World Heritage Site.",
        },
        {
            "name": "Pamukkale",
            "country": "Turkey",
            "lat": 37.9213,
            "lng": 29.1200,
            "image_url": "https://images.unsplash.com/photo-1574351406668-5d2b6c040d94?w=800",
            "description": "Natural thermal pools on white calcium terraces, known as the Cotton Castle.",
        },
        {
            "name": "Ankara",
            "country": "Turkey",
            "lat": 39.9334,
            "lng": 32.8597,
            "image_url": "https://images.unsplash.com/photo-1596423230819-3e77f2072a8a?w=800",
            "description": "Turkey's capital city with Atatürk's mausoleum and vibrant modern culture.",
        },
        {
            "name": "Trabzon",
            "country": "Turkey",
            "lat": 41.0015,
            "lng": 39.7178,
            "image_url": "https://images.unsplash.com/photo-1634128221889-82ed6efebfc3?w=800",
            "description": "Black Sea gem with the legendary Sumela Monastery carved into cliffsides.",
        },
        {
            "name": "Bodrum",
            "country": "Turkey",
            "lat": 37.0344,
            "lng": 27.4305,
            "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800",
            "description": "Iconic whitewashed town on the Aegean with a medieval castle and crystal waters.",
        },
        {
            "name": "Gaziantep",
            "country": "Turkey",
            "lat": 37.0662,
            "lng": 37.3833,
            "image_url": "https://images.unsplash.com/photo-1539814858141-928517f6afd3?w=800",
            "description": "UNESCO Creative City of Gastronomy, home of baklava and ancient mosaics.",
        },
        {
            "name": "Konya",
            "country": "Turkey",
            "lat": 37.8746,
            "lng": 32.4932,
            "image_url": "https://images.unsplash.com/photo-1636832557069-4e2ab74b3b3e?w=800",
            "description": "Spiritual heart of Turkey and home of the Whirling Dervishes of Rumi.",
        },
    ]

    destinations: dict[str, str] = {}  # name -> id
    print("Creating 10 Destinations...")
    for d in dest_data:
        dest_id = uid()
        db.query(
            "CREATE (d:Destination {id: $id, name: $name, country: $country, "
            "description: $desc, lat: $lat, lng: $lng, image_url: $img})",
            {
                "id": dest_id,
                "name": d["name"],
                "country": d["country"],
                "desc": d["description"],
                "lat": d["lat"],
                "lng": d["lng"],
                "img": d["image_url"],
            },
        )
        destinations[d["name"]] = dest_id

    # ── Categories ─────────────────────────────────────────────────────────────
    cat_names = ["Museum", "Nature", "Food & Drink", "Historical", "Adventure", "Culture"]
    categories: list[str] = []
    print("Creating Categories...")
    for cname in cat_names:
        cid = uid()
        db.query(
            "CREATE (c:Category {id: $id, name: $name, description: $desc})",
            {"id": cid, "name": cname, "desc": f"{cname} experiences."},
        )
        categories.append(cid)

    # ── Seasons ────────────────────────────────────────────────────────────────
    season_names = ["Spring", "Summer", "Autumn", "Winter"]
    print("Creating Seasons...")
    for sname in season_names:
        db.query(
            "CREATE (s:Season {id: $id, name: $name})",
            {"id": uid(), "name": sname},
        )

    # ── Tags ───────────────────────────────────────────────────────────────────
    tag_names = ["UNESCO", "Hidden Gem", "Budget Friendly", "Luxury", "Family Friendly", "Adventure"]
    tags: list[str] = []
    print("Creating Tags...")
    for tname in tag_names:
        tid = uid()
        db.query(
            "CREATE (t:Tag {id: $id, name: $name})",
            {"id": tid, "name": tname},
        )
        tags.append(tid)

    # ── Activities (20, mapped to real destinations) ───────────────────────────
    activities_by_dest: dict[str, list[dict]] = {
        "Istanbul": [
            {"name": "Bosphorus Cruise", "duration_minutes": 120, "price": 25.0},
            {"name": "Hagia Sophia Tour", "duration_minutes": 90, "price": 15.0},
            {"name": "Grand Bazaar Shopping", "duration_minutes": 180, "price": 0.0},
            {"name": "Topkapi Palace Visit", "duration_minutes": 150, "price": 20.0},
            {"name": "Turkish Bath (Hammam)", "duration_minutes": 90, "price": 40.0},
        ],
        "Cappadocia": [
            {"name": "Hot Air Balloon Ride", "duration_minutes": 90, "price": 150.0},
            {"name": "Underground City Tour", "duration_minutes": 120, "price": 18.0},
            {"name": "ATV Safari", "duration_minutes": 180, "price": 45.0},
            {"name": "Hiking in Rose Valley", "duration_minutes": 240, "price": 0.0},
            {"name": "Pottery Workshop", "duration_minutes": 120, "price": 30.0},
        ],
        "Antalya": [
            {"name": "Duden Waterfalls Hike", "duration_minutes": 120, "price": 0.0},
            {"name": "Konyaalti Beach Day", "duration_minutes": 300, "price": 0.0},
            {"name": "Old City (Kaleici) Walking Tour", "duration_minutes": 150, "price": 10.0},
        ],
        "Ephesus": [
            {"name": "Ancient Ruins Guided Tour", "duration_minutes": 180, "price": 22.0},
            {"name": "House of the Virgin Mary Visit", "duration_minutes": 60, "price": 8.0},
        ],
        "Pamukkale": [
            {"name": "Thermal Pool Swimming", "duration_minutes": 180, "price": 12.0},
            {"name": "Hierapolis Ancient City Walk", "duration_minutes": 120, "price": 10.0},
        ],
        "Trabzon": [
            {"name": "Sumela Monastery Visit", "duration_minutes": 150, "price": 12.0},
            {"name": "Uzungol Lake Tour", "duration_minutes": 240, "price": 5.0},
        ],
        "Bodrum": [
            {"name": "Boat Trip to Aegean Islands", "duration_minutes": 480, "price": 35.0},
            {"name": "Bodrum Castle & Museum of Underwater Archaeology", "duration_minutes": 120, "price": 15.0},
        ],
        "Gaziantep": [
            {"name": "Zeugma Mosaic Museum", "duration_minutes": 150, "price": 8.0},
            {"name": "Baklava Making Workshop", "duration_minutes": 120, "price": 25.0},
        ],
        "Konya": [
            {"name": "Mevlana Museum Tour", "duration_minutes": 90, "price": 5.0},
            {"name": "Whirling Dervishes Ceremony", "duration_minutes": 60, "price": 10.0},
        ],
    }

    activity_ids: list[str] = []
    print("Creating 20 Activities...")
    for dest_name, acts in activities_by_dest.items():
        dest_id = destinations.get(dest_name)
        if not dest_id:
            continue
        for act in acts:
            aid = uid()
            db.query(
                "MATCH (d:Destination {id: $did}) "
                "CREATE (a:Activity {id: $id, name: $name, description: $desc, "
                "duration_minutes: $dur, price: $price}) "
                "CREATE (d)-[:HAS_ACTIVITY]->(a)",
                {
                    "did": dest_id,
                    "id": aid,
                    "name": act["name"],
                    "desc": f"Experience {act['name']} in {dest_name}.",
                    "dur": act["duration_minutes"],
                    "price": act["price"],
                },
            )
            activity_ids.append(aid)
            # Link random category and tags
            db.query(
                "MATCH (a:Activity {id: $aid}), (c:Category {id: $cid}) "
                "CREATE (a)-[:BELONGS_TO]->(c)",
                {"aid": aid, "cid": random.choice(categories)},
            )
            for tid in random.sample(tags, 2):
                db.query(
                    "MATCH (a:Activity {id: $aid}), (t:Tag {id: $tid}) "
                    "CREATE (a)-[:HAS_TAG]->(t)",
                    {"aid": aid, "tid": tid},
                )

    # ── Restaurants (15, real Turkey restaurants) ──────────────────────────────
    restaurants_data = [
        {"name": "Nusr-Et Steakhouse", "city": "Istanbul", "cuisine_type": "Steakhouse", "price_range": "luxury", "rating": 4.8, "address": "Etiler, Istanbul"},
        {"name": "Karakoy Gulluoglu", "city": "Istanbul", "cuisine_type": "Baklava & Turkish Sweets", "price_range": "budget", "rating": 4.9, "address": "Karakoy, Istanbul"},
        {"name": "Hamdi Restaurant", "city": "Istanbul", "cuisine_type": "Kebab & Turkish Cuisine", "price_range": "mid", "rating": 4.7, "address": "Eminonu, Istanbul"},
        {"name": "Seki Restaurant", "city": "Cappadocia", "cuisine_type": "Turkish Fine Dining", "price_range": "luxury", "rating": 4.6, "address": "Uchisar, Cappadocia"},
        {"name": "Dibek Restaurant", "city": "Cappadocia", "cuisine_type": "Traditional Cave Dining", "price_range": "mid", "rating": 4.5, "address": "Goreme, Cappadocia"},
        {"name": "Vanilla Restaurant", "city": "Antalya", "cuisine_type": "Mediterranean", "price_range": "mid", "rating": 4.5, "address": "Kaleici, Antalya"},
        {"name": "Hasanaga Restaurant", "city": "Antalya", "cuisine_type": "Traditional Turkish", "price_range": "mid", "rating": 4.4, "address": "Antalya"},
        {"name": "Mehmet & Ali Baba", "city": "Ephesus", "cuisine_type": "Aegean Seafood", "price_range": "mid", "rating": 4.3, "address": "Selcuk, Ephesus"},
        {"name": "Imam Cagdas", "city": "Gaziantep", "cuisine_type": "Baklava & Kebab", "price_range": "mid", "rating": 4.9, "address": "Gaziantep Bazaar"},
        {"name": "Zeugma Restaurant", "city": "Gaziantep", "cuisine_type": "Traditional Gaziantep Cuisine", "price_range": "mid", "rating": 4.4, "address": "Gaziantep"},
        {"name": "Kocadon Restaurant", "city": "Bodrum", "cuisine_type": "Aegean Cuisine", "price_range": "mid", "rating": 4.6, "address": "Bodrum Marina"},
        {"name": "Melrose Viewpoint", "city": "Pamukkale", "cuisine_type": "Local Turkish Cuisine", "price_range": "mid", "rating": 4.2, "address": "Pamukkale"},
        {"name": "Cemil Usta", "city": "Trabzon", "cuisine_type": "Black Sea Cuisine", "price_range": "mid", "rating": 4.5, "address": "Trabzon"},
        {"name": "Trilye Restaurant", "city": "Ankara", "cuisine_type": "Seafood", "price_range": "luxury", "rating": 4.7, "address": "Kavaklidere, Ankara"},
        {"name": "Somaci", "city": "Konya", "cuisine_type": "Traditional Konya Cuisine", "price_range": "mid", "rating": 4.5, "address": "Konya"},
    ]

    restaurant_ids: list[str] = []
    print("Creating 15 Restaurants...")
    for r in restaurants_data:
        rid = uid()
        dest_id = destinations.get(r["city"])
        if not dest_id:
            continue
        db.query(
            "MATCH (d:Destination {id: $did}) "
            "CREATE (r:Restaurant {id: $id, name: $name, cuisine_type: $cuisine, "
            "price_range: $price, address: $addr, rating: $rating}) "
            "CREATE (d)-[:HAS_RESTAURANT]->(r)",
            {
                "did": dest_id,
                "id": rid,
                "name": r["name"],
                "cuisine": r["cuisine_type"],
                "price": r["price_range"],
                "addr": r["address"],
                "rating": r["rating"],
            },
        )
        restaurant_ids.append(rid)

    # ── Accommodations (10) ────────────────────────────────────────────────────
    accommodations: list[str] = []
    print("Creating 10 Accommodations...")
    acc_data = [
        {"name": "Four Seasons Istanbul", "city": "Istanbul", "type": "hotel", "stars": 5, "price": 350.0},
        {"name": "Sultan Cave Suites", "city": "Cappadocia", "type": "boutique", "stars": 5, "price": 280.0},
        {"name": "Titanic Beach Lara", "city": "Antalya", "type": "hotel", "stars": 5, "price": 180.0},
        {"name": "Caravanserai Cave Hotel", "city": "Cappadocia", "type": "boutique", "stars": 4, "price": 150.0},
        {"name": "Ephesus Boutique Hotel", "city": "Ephesus", "type": "hotel", "stars": 4, "price": 120.0},
        {"name": "Pamukkale Thermal Hotel", "city": "Pamukkale", "type": "hotel", "stars": 4, "price": 100.0},
        {"name": "Bodrum Bay Resort", "city": "Bodrum", "type": "resort", "stars": 5, "price": 300.0},
        {"name": "Ankara Hilton", "city": "Ankara", "type": "hotel", "stars": 5, "price": 200.0},
        {"name": "Trabzon Grand Hotel", "city": "Trabzon", "type": "hotel", "stars": 4, "price": 90.0},
        {"name": "Konya Dedeman", "city": "Konya", "type": "hotel", "stars": 4, "price": 110.0},
    ]
    for a in acc_data:
        accid = uid()
        dest_id = destinations.get(a["city"])
        if not dest_id:
            continue
        db.query(
            "MATCH (d:Destination {id: $did}) "
            "CREATE (acc:Accommodation {id: $id, name: $name, type: $type, "
            "star_rating: $stars, price_per_night: $price, address: $city}) "
            "CREATE (d)-[:HAS_ACCOMMODATION]->(acc)",
            {
                "did": dest_id,
                "id": accid,
                "name": a["name"],
                "type": a["type"],
                "stars": a["stars"],
                "price": a["price"],
                "city": a["city"],
            },
        )
        accommodations.append(accid)

    # ── Festivals (10, 2026 dates) ─────────────────────────────────────────────
    festivals_data = [
        {
            "name": "Istanbul Tulip Festival",
            "city": "Istanbul",
            "start_date": "2026-04-01",
            "end_date": "2026-04-30",
            "description": "Millions of tulips bloom across Istanbul's parks and gardens every April.",
            "ticket_price": 0.0,
            "season": "Spring",
        },
        {
            "name": "Cappadocia Hot Air Balloon Festival",
            "city": "Cappadocia",
            "start_date": "2026-05-10",
            "end_date": "2026-05-13",
            "description": "International balloon competition with 100+ balloons filling the Cappadocian sky.",
            "ticket_price": 50.0,
            "season": "Spring",
        },
        {
            "name": "Istanbul Jazz Festival",
            "city": "Istanbul",
            "start_date": "2026-06-28",
            "end_date": "2026-07-12",
            "description": "World-class jazz festival held across iconic Istanbul venues since 1994.",
            "ticket_price": 80.0,
            "season": "Summer",
        },
        {
            "name": "Bodrum Ballet Festival",
            "city": "Bodrum",
            "start_date": "2026-07-15",
            "end_date": "2026-07-20",
            "description": "International ballet performances in the open-air ancient amphitheater.",
            "ticket_price": 60.0,
            "season": "Summer",
        },
        {
            "name": "Gaziantep Gastronomy Festival",
            "city": "Gaziantep",
            "start_date": "2026-09-05",
            "end_date": "2026-09-08",
            "description": "Celebrating UNESCO gastronomy city status with local chefs and food tours.",
            "ticket_price": 0.0,
            "season": "Autumn",
        },
        {
            "name": "Antalya Film Festival",
            "city": "Antalya",
            "start_date": "2026-10-01",
            "end_date": "2026-10-08",
            "description": "Turkey's oldest and most prestigious film festival, the Golden Orange.",
            "ticket_price": 30.0,
            "season": "Autumn",
        },
        {
            "name": "Konya Mevlana Commemoration",
            "city": "Konya",
            "start_date": "2026-12-07",
            "end_date": "2026-12-17",
            "description": "Annual Whirling Dervishes ceremony commemorating Rumi's reunion with God.",
            "ticket_price": 0.0,
            "season": "Winter",
        },
        {
            "name": "Trabzon Akcaabat Music Festival",
            "city": "Trabzon",
            "start_date": "2026-07-20",
            "end_date": "2026-07-23",
            "description": "Traditional Black Sea folk music and dance festival on the coast.",
            "ticket_price": 0.0,
            "season": "Summer",
        },
        {
            "name": "Ephesus Culture Festival",
            "city": "Ephesus",
            "start_date": "2026-05-20",
            "end_date": "2026-05-25",
            "description": "Classical music concerts and theater performances in the ancient ruins.",
            "ticket_price": 40.0,
            "season": "Spring",
        },
        {
            "name": "Pamukkale Triathlon",
            "city": "Pamukkale",
            "start_date": "2026-06-14",
            "end_date": "2026-06-15",
            "description": "International triathlon set against the stunning white travertine terraces.",
            "ticket_price": 25.0,
            "season": "Summer",
        },
    ]

    print("Creating 10 Festivals...")
    for f in festivals_data:
        fid = uid()
        dest_id = destinations.get(f["city"])
        if not dest_id:
            continue
        db.query(
            "MATCH (d:Destination {id: $did}) "
            "CREATE (fest:Festival {id: $id, name: $name, description: $desc, "
            "start_date: $sd, end_date: $ed, is_recurring: true, "
            "ticket_price: $price, season: $season, city: $city}) "
            "CREATE (d)-[:HAS_FESTIVAL]->(fest)",
            {
                "did": dest_id,
                "id": fid,
                "name": f["name"],
                "desc": f["description"],
                "sd": f["start_date"],
                "ed": f["end_date"],
                "price": f["ticket_price"],
                "season": f["season"],
                "city": f["city"],
            },
        )

    # ── Reviews (10) ───────────────────────────────────────────────────────────
    reviewables = activity_ids + restaurant_ids + accommodations
    print("Creating 10 Reviews...")
    for _ in range(10):
        uid_ = random.choice(users)
        tid = random.choice(reviewables)
        db.query(
            "MATCH (u:User {id: $uid}), (t {id: $tid}) "
            "CREATE (r:Review {id: $id, target_id: $tid, target_type: 'mixed', "
            "rating: $rating, comment: $comment, created_at: $ca}) "
            "CREATE (u)-[:WROTE]->(r) "
            "CREATE (r)-[:ABOUT]->(t)",
            {
                "uid": uid_,
                "tid": tid,
                "id": uid(),
                "rating": random.randint(4, 5),
                "comment": random.choice([
                    "Absolutely amazing experience!",
                    "Highly recommend to all visitors.",
                    "A must-see destination in Turkey.",
                    "Exceeded all expectations.",
                    "Unforgettable memories.",
                ]),
                "ca": datetime.now(timezone.utc).isoformat(),
            },
        )

    # ── User → Visited → Destination ──────────────────────────────────────────
    dest_ids = list(destinations.values())
    print("Linking Users to Visited Destinations...")
    for user_id in users:
        for dest_id in random.sample(dest_ids, random.randint(2, 4)):
            db.query(
                "MATCH (u:User {id: $uid}), (d:Destination {id: $did}) "
                "MERGE (u)-[:VISITED]->(d)",
                {"uid": user_id, "did": dest_id},
            )

    print("\nSeed completed successfully!")
    print(f"  {len(dest_data)} destinations")
    print(f"  {sum(len(v) for v in activities_by_dest.values())} activities")
    print(f"  {len(restaurants_data)} restaurants")
    print(f"  {len(acc_data)} accommodations")
    print(f"  {len(festivals_data)} festivals")


if __name__ == "__main__":
    main()
