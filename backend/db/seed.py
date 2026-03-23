"""FalkorDB seed script for TravelGraph."""
from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from core.security import hash_password
from db.connection import get_db

def create_uuid() -> str:
    return str(uuid4())

def main() -> None:
    db = next(get_db())
    print("Clearing existing database...")
    db.query("MATCH (n) DETACH DELETE n")
    print("Database cleared.\n")

    # Users
    users = []
    print("Creating 5 Users...")
    for i in range(1, 6):
        uid = create_uuid()
        db.query(
            "CREATE (u:User {id: $id, email: $email, name: $name, password_hash: $ph, created_at: $ca})",
            {
                "id": uid,
                "email": f"user{i}@example.com",
                "name": f"User {i}",
                "ph": hash_password("password123"),
                "ca": datetime.now(timezone.utc).isoformat()
            }
        )
        users.append(uid)

    # Destinations
    dest_data = [
        {"name": "Istanbul",  "country": "Türkiye",     "lat": 41.0082,  "lng": 28.9784},
        {"name": "Paris",     "country": "Fransa",      "lat": 48.8566,  "lng":  2.3522},
        {"name": "Barcelona", "country": "İspanya",     "lat": 41.3851,  "lng":  2.1734},
        {"name": "Roma",      "country": "İtalya",      "lat": 41.9028,  "lng": 12.4964},
        {"name": "Tokyo",     "country": "Japonya",     "lat": 35.6762,  "lng": 139.6503},
        {"name": "New York",  "country": "ABD",         "lat": 40.7128,  "lng": -74.0060},
        {"name": "Bali",      "country": "Endonezya",   "lat": -8.3405,  "lng": 115.0920},
        {"name": "Prag",      "country": "Çekya",       "lat": 50.0755,  "lng": 14.4378},
        {"name": "Amsterdam", "country": "Hollanda",    "lat": 52.3676,  "lng":  4.9041},
        {"name": "Lizbon",    "country": "Portekiz",    "lat": 38.7223,  "lng": -9.1393},
    ]
    destinations = []
    print("Creating 10 Destinations...")
    for d in dest_data:
        did = create_uuid()
        db.query(
            "CREATE (d:Destination {id: $id, name: $name, country: $country, description: $desc, lat: $lat, lng: $lng})",
            {
                "id": did,
                "name": d["name"],
                "country": d["country"],
                "desc": f"The beautiful city of {d['name']}.",
                "lat": d["lat"],
                "lng": d["lng"],
            }
        )
        destinations.append(did)

    # Categories
    cat_names = ["Museum", "Nature", "Food & Drink"]
    categories = []
    print("Creating 3 Categories...")
    for cname in cat_names:
        cid = create_uuid()
        db.query(
            "CREATE (c:Category {id: $id, name: $name, description: $desc})",
            {"id": cid, "name": cname, "desc": f"{cname} category."}
        )
        categories.append(cid)

    # Seasons
    season_names = ["Spring", "Summer", "Autumn", "Winter"]
    print("Creating 4 Seasons...")
    for sname in season_names:
        db.query(
            "CREATE (s:Season {id: $id, name: $name})",
            {"id": create_uuid(), "name": sname}
        )

    # Tags
    tag_names = ["Popular", "Hidden Gem", "Budget", "Luxury", "Family Friendly"]
    tags = []
    print("Creating Tags...")
    for tname in tag_names:
        tid = create_uuid()
        db.query(
            "CREATE (t:Tag {id: $id, name: $name})",
            {"id": tid, "name": tname}
        )
        tags.append(tid)

    # Activities (20, 2 per destination)
    activities = []
    print("Creating 20 Activities...")
    for did in destinations:
        for j in range(2):
            aid = create_uuid()
            act_name = f"Activity {j+1} in Destination"
            db.query(
                "MATCH (d:Destination {id: $did}) "
                "CREATE (a:Activity {id: $id, name: $name, description: $desc, duration_minutes: 120, price: 50.0}) "
                "CREATE (d)-[:HAS_ACTIVITY]->(a)",
                {
                    "did": did,
                    "id": aid,
                    "name": act_name,
                    "desc": "An exciting activity."
                }
            )
            activities.append(aid)
            
            # Link Category
            cid = random.choice(categories)
            db.query(
                "MATCH (a:Activity {id: $aid}), (c:Category {id: $cid}) "
                "CREATE (a)-[:BELONGS_TO]->(c)",
                {"aid": aid, "cid": cid}
            )
            
            # Link Tags
            for tid in random.sample(tags, 2):
                db.query(
                    "MATCH (a:Activity {id: $aid}), (t:Tag {id: $tid}) "
                    "CREATE (a)-[:HAS_TAG]->(t)",
                    {"aid": aid, "tid": tid}
                )

    # Restaurants (15)
    cuisines = ["Turkish", "French", "Japanese", "Italian", "Fusion"]
    restaurants = []
    print("Creating 15 Restaurants...")
    for i in range(15):
        rid = create_uuid()
        did = random.choice(destinations)
        db.query(
            "MATCH (d:Destination {id: $did}) "
            "CREATE (r:Restaurant {id: $id, name: $name, cuisine_type: $cuisine, price_range: $price, address: 'Sample Address', rating: $rating}) "
            "CREATE (d)-[:HAS_RESTAURANT]->(r)",
            {
                "did": did,
                "id": rid,
                "name": f"Restaurant {i+1}",
                "cuisine": cuisines[i % len(cuisines)],
                "price": random.choice(["budget", "mid", "luxury"]),
                "rating": round(random.uniform(3.5, 5.0), 1)
            }
        )
        restaurants.append(rid)

    # Festivals (10)
    print("Creating 10 Festivals...")
    for i in range(10):
        fid = create_uuid()
        did = random.choice(destinations)
        season = random.choice(season_names)
        start = datetime.now() + timedelta(days=random.randint(10, 100))
        end = start + timedelta(days=random.randint(1, 5))
        db.query(
            "MATCH (d:Destination {id: $did}) "
            "CREATE (f:Festival {id: $id, name: $name, description: 'Annual festival', start_date: $sd, end_date: $ed, is_recurring: true, ticket_price: $price, season: $season}) "
            "CREATE (d)-[:HAS_FESTIVAL]->(f)",
            {
                "did": did,
                "id": fid,
                "name": f"Festival {i+1}",
                "sd": start.strftime("%Y-%m-%d"),
                "ed": end.strftime("%Y-%m-%d"),
                "price": float(random.randint(0, 100)),
                "season": season
            }
        )

    # Accommodations (10)
    accommodations = []
    print("Creating 10 Accommodations...")
    for i in range(10):
        accid = create_uuid()
        did = random.choice(destinations)
        db.query(
            "MATCH (d:Destination {id: $did}) "
            "CREATE (acc:Accommodation {id: $id, name: $name, type: $type, star_rating: $stars, price_per_night: $price, address: 'Hotel Avenue'}) "
            "CREATE (d)-[:HAS_ACCOMMODATION]->(acc)",
            {
                "did": did,
                "id": accid,
                "name": f"Accommodation {i+1}",
                "type": random.choice(["hotel", "hostel", "apartment"]),
                "stars": random.randint(3, 5),
                "price": float(random.randint(50, 300))
            }
        )
        accommodations.append(accid)

    # Reviews (15)
    print("Creating 15 Reviews...")
    reviewables = activities + restaurants + accommodations
    for i in range(15):
        uid = random.choice(users)
        tid = random.choice(reviewables)
        db.query(
            "MATCH (u:User {id: $uid}), (t {id: $tid}) "
            "CREATE (r:Review {id: $id, target_id: $tid, target_type: 'mixed', rating: $rating, comment: 'Great experience!', created_at: $ca}) "
            "CREATE (u)-[:WROTE]->(r) "
            "CREATE (r)-[:ABOUT]->(t)",
            {
                "uid": uid,
                "tid": tid,
                "id": create_uuid(),
                "rating": random.randint(3, 5),
                "ca": datetime.now(timezone.utc).isoformat()
            }
        )

    # (User)-[:VISITED]->(Destination) (3-5 per user)
    print("Linking Users to Visited Destinations...")
    for uid in users:
        visited = random.sample(destinations, random.randint(3, 5))
        for did in visited:
            db.query(
                "MATCH (u:User {id: $uid}), (d:Destination {id: $did}) "
                "MERGE (u)-[:VISITED]->(d)",
                {"uid": uid, "did": did}
            )

    print("Seed process successfully completed!")

if __name__ == "__main__":
    main()
