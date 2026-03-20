"""Database seed script — 30 Turkey destinations with real, distinct data.

Run from the backend directory:
    python -m db.seed
"""

import logging
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from core.security import hash_password
from db.connection import _connect_with_retry  # noqa: PLC2701

logging.basicConfig(level=logging.WARNING)

# ── Metadata ──────────────────────────────────────────────────────────────────

_CATEGORIES: list[dict] = [
    {"id": str(uuid4()), "name": "Museum",        "icon": "🏛️"},
    {"id": str(uuid4()), "name": "Nature",         "icon": "🌿"},
    {"id": str(uuid4()), "name": "Food & Drink",   "icon": "🍽️"},
    {"id": str(uuid4()), "name": "Historical",     "icon": "🏰"},
    {"id": str(uuid4()), "name": "Adventure",      "icon": "🧗"},
    {"id": str(uuid4()), "name": "Beach",          "icon": "🏖️"},
    {"id": str(uuid4()), "name": "Religious",      "icon": "🕌"},
]

_SEASONS: list[dict] = [
    {"id": str(uuid4()), "name": "Spring",  "months": [3, 4, 5],   "avg_temp_c": 16.0, "weather_description": "Mild and blooming"},
    {"id": str(uuid4()), "name": "Summer",  "months": [6, 7, 8],   "avg_temp_c": 29.0, "weather_description": "Hot and sunny"},
    {"id": str(uuid4()), "name": "Autumn",  "months": [9, 10, 11], "avg_temp_c": 14.0, "weather_description": "Cool and colourful"},
    {"id": str(uuid4()), "name": "Winter",  "months": [12, 1, 2],  "avg_temp_c": 4.0,  "weather_description": "Cold, sometimes snowy"},
]

_TAGS: list[dict] = [
    {"id": str(uuid4()), "name": "family-friendly", "color": "#4CAF50"},
    {"id": str(uuid4()), "name": "romantic",         "color": "#E91E63"},
    {"id": str(uuid4()), "name": "budget",           "color": "#FF9800"},
    {"id": str(uuid4()), "name": "adventure",        "color": "#9C27B0"},
    {"id": str(uuid4()), "name": "cultural",         "color": "#2196F3"},
    {"id": str(uuid4()), "name": "foodie",           "color": "#FF5722"},
    {"id": str(uuid4()), "name": "nature",           "color": "#00BCD4"},
]

# ── 30 Destinations ───────────────────────────────────────────────────────────

_DESTINATIONS: list[dict] = [
    {"name": "Istanbul",    "country": "Turkey", "lat": 41.0082,  "lng": 28.9784,  "best_seasons": ["Spring", "Autumn"],
     "description": "Transcontinental city on the Bosphorus, blending Byzantine grandeur with vibrant bazaars and modern life."},
    {"name": "Ankara",      "country": "Turkey", "lat": 39.9334,  "lng": 32.8597,  "best_seasons": ["Spring", "Autumn"],
     "description": "Turkey's capital city, home to Ataturk's mausoleum and a rich museum of Anatolian civilisations."},
    {"name": "Izmir",       "country": "Turkey", "lat": 38.4192,  "lng": 27.1287,  "best_seasons": ["Spring", "Summer"],
     "description": "Cosmopolitan Aegean port city with a lively waterfront promenade, ancient Ephesus nearby, and superb seafood."},
    {"name": "Antalya",     "country": "Turkey", "lat": 36.8969,  "lng": 30.7133,  "best_seasons": ["Spring", "Summer"],
     "description": "Gateway to the Turkish Riviera with Roman harbours, cascading waterfalls, and long golden beaches."},
    {"name": "Bursa",       "country": "Turkey", "lat": 40.1885,  "lng": 29.0610,  "best_seasons": ["Spring", "Autumn"],
     "description": "First Ottoman capital, famed for its silk market, green mountains, thermal baths, and Iskender kebab."},
    {"name": "Adana",       "country": "Turkey", "lat": 37.0000,  "lng": 35.3213,  "best_seasons": ["Spring", "Autumn"],
     "description": "Culinary capital of southern Turkey, home to the spicy Adana kebab and the historic Stone Bridge."},
    {"name": "Gaziantep",   "country": "Turkey", "lat": 37.0662,  "lng": 37.3833,  "best_seasons": ["Spring", "Autumn"],
     "description": "UNESCO Creative City of Gastronomy, world-famous for baklava, pistachios, and a rich Silk Road heritage."},
    {"name": "Konya",       "country": "Turkey", "lat": 37.8713,  "lng": 32.4846,  "best_seasons": ["Spring", "Autumn"],
     "description": "Spiritual heart of Turkey, home to Rumi's shrine and the whirling dervishes of the Mevlana Order."},
    {"name": "Mersin",      "country": "Turkey", "lat": 36.8000,  "lng": 34.6333,  "best_seasons": ["Spring", "Summer"],
     "description": "Bustling Mediterranean port with a mix of ancient ruins, fresh seafood, and beautiful coastal scenery."},
    {"name": "Diyarbakir",  "country": "Turkey", "lat": 37.9144,  "lng": 40.2306,  "best_seasons": ["Spring", "Autumn"],
     "description": "Ancient walled city on the Tigris, with massive basalt fortifications, historic mosques, and rich culture."},
    {"name": "Trabzon",     "country": "Turkey", "lat": 41.0015,  "lng": 39.7178,  "best_seasons": ["Spring", "Summer"],
     "description": "Black Sea city of lush green mountains, the mystical Sumela Monastery, and the serene Uzungol lake."},
    {"name": "Kayseri",     "country": "Turkey", "lat": 38.7312,  "lng": 35.4787,  "best_seasons": ["Spring", "Autumn"],
     "description": "Gateway to Cappadocia, famous for its historic covered bazaar, pastirma cured meat, and Mount Erciyes."},
    {"name": "Eskisehir",   "country": "Turkey", "lat": 39.7767,  "lng": 30.5206,  "best_seasons": ["Spring", "Summer"],
     "description": "Vibrant university city with colourful canals, meerschaum workshops, and a lively arts and café scene."},
    {"name": "Samsun",      "country": "Turkey", "lat": 41.2867,  "lng": 36.3300,  "best_seasons": ["Spring", "Summer"],
     "description": "Historic Black Sea port where Ataturk launched the War of Independence, surrounded by tobacco fields."},
    {"name": "Denizli",     "country": "Turkey", "lat": 37.7765,  "lng": 29.0864,  "best_seasons": ["Spring", "Autumn"],
     "description": "Base for Pamukkale's iconic white travertine terraces and the ancient Hierapolis spa city."},
    {"name": "Bodrum",      "country": "Turkey", "lat": 37.0344,  "lng": 27.4305,  "best_seasons": ["Summer"],
     "description": "Glamorous Aegean resort, home of the ancient Mausoleum wonder, windmills, and turquoise coves."},
    {"name": "Cappadocia",  "country": "Turkey", "lat": 38.6431,  "lng": 34.8289,  "best_seasons": ["Spring", "Autumn"],
     "description": "Otherworldly landscape of fairy chimneys, underground cities, cave hotels, and sunrise hot-air balloons."},
    {"name": "Safranbolu",  "country": "Turkey", "lat": 41.2517,  "lng": 32.6914,  "best_seasons": ["Spring", "Autumn"],
     "description": "UNESCO World Heritage Ottoman town with perfectly preserved half-timbered mansions and cobblestone lanes."},
    {"name": "Sanliurfa",   "country": "Turkey", "lat": 37.1591,  "lng": 38.7969,  "best_seasons": ["Spring", "Autumn"],
     "description": "City of prophets near Gobeklitepe, with sacred carp pools, a bazaar unchanged in centuries, and rich faith traditions."},
    {"name": "Van",         "country": "Turkey", "lat": 38.4891,  "lng": 43.4089,  "best_seasons": ["Spring", "Summer"],
     "description": "Eastern pearl beside a vast saline lake, home to the Akdamar Armenian Church and the famous Van cat."},
    {"name": "Erzurum",     "country": "Turkey", "lat": 39.9043,  "lng": 41.2679,  "best_seasons": ["Spring", "Summer"],
     "description": "High-altitude Silk Road crossroads with imposing fortresses, a twin-minareted mosque, and ski slopes."},
    {"name": "Mardin",      "country": "Turkey", "lat": 37.3212,  "lng": 40.7245,  "best_seasons": ["Spring", "Autumn"],
     "description": "Honey-coloured hilltop city overlooking Mesopotamia, famous for its Syriac churches and Artuqid architecture."},
    {"name": "Afyonkarahisar", "country": "Turkey", "lat": 38.7507, "lng": 30.5567, "best_seasons": ["Spring", "Autumn"],
     "description": "Land of thermal springs, poppy fields, and the best kaymak cream in Turkey, beneath a volcanic citadel."},
    {"name": "Canakkale",   "country": "Turkey", "lat": 40.1553,  "lng": 26.4142,  "best_seasons": ["Spring", "Autumn"],
     "description": "Dardanelles strait town near ancient Troy, Gallipoli battlefields, and ferry crossings between Europe and Asia."},
    {"name": "Edirne",      "country": "Turkey", "lat": 41.6818,  "lng": 26.5623,  "best_seasons": ["Spring", "Summer"],
     "description": "Former Ottoman capital with the magnificent Selimiye Mosque and host of the oldest oil wrestling festival in the world."},
    {"name": "Balikesir",   "country": "Turkey", "lat": 39.6484,  "lng": 27.8826,  "best_seasons": ["Spring", "Summer"],
     "description": "Aegean hinterland province with thermal springs, the coastal Ayvalik resort, and pristine olive groves."},
    {"name": "Malatya",     "country": "Turkey", "lat": 38.3552,  "lng": 38.3095,  "best_seasons": ["Summer", "Autumn"],
     "description": "Capital of the apricot world, producing over half of Turkey's famous sun-dried apricots on volcanic slopes."},
    {"name": "Kahramanmaras", "country": "Turkey", "lat": 37.5858, "lng": 36.9371, "best_seasons": ["Spring", "Autumn"],
     "description": "Birthplace of the legendary stretchy Maras dondurma ice cream, flanked by highlands and ancient castles."},
    {"name": "Alanya",      "country": "Turkey", "lat": 36.5441,  "lng": 32.0059,  "best_seasons": ["Summer"],
     "description": "Sun-drenched resort below a Seljuk hilltop castle, offering sea caves, 125 km of beach, and turquoise water."},
    {"name": "Pamukkale",   "country": "Turkey", "lat": 37.9272,  "lng": 29.1239,  "best_seasons": ["Spring", "Autumn"],
     "description": "Natural wonder of cotton-white calcium terraces cascading beside the ancient Roman spa city of Hierapolis."},
]

# ── Activities ────────────────────────────────────────────────────────────────

_ACTIVITIES: dict[str, list[dict]] = {
    "Istanbul": [
        {"name": "Ayasofya", "description": "Monumental Byzantine cathedral turned mosque, a UNESCO masterpiece of architecture spanning 1500 years.", "duration_hours": 2.0, "price": 680.0, "address": "Sultan Ahmet, Fatih", "categories": ["Museum", "Historical", "Religious"], "tags": ["cultural", "family-friendly"]},
        {"name": "Topkapi Sarayi", "description": "Opulent palace complex of Ottoman sultans housing priceless imperial treasures and harem chambers.", "duration_hours": 3.0, "price": 750.0, "address": "Sultanahmet, Fatih", "categories": ["Museum", "Historical"], "tags": ["cultural", "family-friendly"]},
        {"name": "Kapalicarsi", "description": "One of the world's oldest covered bazaars — 61 streets, 4000 shops, and centuries of trading tradition.", "duration_hours": 2.5, "price": 0.0, "address": "Beyazit, Fatih", "categories": ["Historical"], "tags": ["cultural", "budget", "family-friendly"]},
        {"name": "Bogaz Turu", "description": "Cruise between continents as the skyline of minarets and palaces glows in the golden hour light.", "duration_hours": 2.0, "price": 350.0, "address": "Eminonu Iskelesi", "categories": ["Nature"], "tags": ["romantic", "family-friendly"]},
        {"name": "Galata Kulesi", "description": "Medieval Genoese tower offering a 360-degree panoramic view over the Golden Horn and city skyline.", "duration_hours": 1.0, "price": 450.0, "address": "Galata, Beyoglu", "categories": ["Historical"], "tags": ["romantic", "cultural"]},
    ],
    "Ankara": [
        {"name": "Anitkabir", "description": "Grand mausoleum of Mustafa Kemal Ataturk, an emotionally powerful monument of modern Turkish history.", "duration_hours": 2.0, "price": 0.0, "address": "Anıtkabir, Cankaya", "categories": ["Museum", "Historical"], "tags": ["cultural", "family-friendly"]},
        {"name": "Anadolu Medeniyetleri Muzesi", "description": "World-class museum housing the finest Hittite, Phrygian, Urartian, and Neolithic artefacts in existence.", "duration_hours": 3.0, "price": 100.0, "address": "Hisarparkı Cad., Ulus", "categories": ["Museum", "Historical"], "tags": ["cultural", "family-friendly"]},
        {"name": "Ankara Kalesi", "description": "Hilltop Byzantine and Seljuk fortress overlooking the old city, with stunning views and a traditional bazaar below.", "duration_hours": 1.5, "price": 0.0, "address": "Ulus, Altindag", "categories": ["Historical"], "tags": ["cultural", "budget"]},
    ],
    "Izmir": [
        {"name": "Kordon Sahil Yuruyusu", "description": "Stroll along the iconic seafront promenade lined with cafes, palm trees, and views of Izmir Bay.", "duration_hours": 1.5, "price": 0.0, "address": "Kordon, Alsancak", "categories": ["Nature"], "tags": ["romantic", "budget", "family-friendly"]},
        {"name": "Kemeralti Carsisi", "description": "Bustling Ottoman bazaar district with historic hans, herb sellers, and hidden mosques dating to the 17th century.", "duration_hours": 2.0, "price": 0.0, "address": "Kemeralti, Konak", "categories": ["Historical"], "tags": ["cultural", "budget"]},
        {"name": "Efes Antik Kenti", "description": "Magnificent Roman city of Ephesus — walk down marble roads past the iconic Library of Celsus.", "duration_hours": 4.0, "price": 600.0, "address": "Selcuk, Izmir", "categories": ["Historical", "Museum"], "tags": ["cultural", "family-friendly"]},
        {"name": "Sirince Koyu", "description": "Charming Greek-Ottoman hillside village famous for fruit wines, stone houses, and mountain walks.", "duration_hours": 3.0, "price": 0.0, "address": "Sirince, Selcuk", "categories": ["Nature"], "tags": ["romantic", "foodie"]},
    ],
    "Antalya": [
        {"name": "Duden Selalesi", "description": "Spectacular waterfall plunging directly into the Mediterranean Sea at the base of dramatic limestone cliffs.", "duration_hours": 1.5, "price": 0.0, "address": "Varsak, Antalya", "categories": ["Nature"], "tags": ["family-friendly", "nature"]},
        {"name": "Kaleici Tarihi Semt", "description": "Roman harbour district with 2000-year-old city walls, Ottoman mansions, and Hadrian's Gate.", "duration_hours": 2.5, "price": 0.0, "address": "Kaleici, Muratpasa", "categories": ["Historical"], "tags": ["cultural", "romantic", "budget"]},
        {"name": "Aspendos Tiyatrosu", "description": "Best-preserved Roman theatre in the world, still hosting opera and ballet performances today.", "duration_hours": 2.0, "price": 300.0, "address": "Serik, Antalya", "categories": ["Historical", "Museum"], "tags": ["cultural"]},
        {"name": "Olympos Teleferik", "description": "Cable car ride to the summit of Tahtali mountain for breathtaking views of the Turquoise Coast.", "duration_hours": 3.0, "price": 900.0, "address": "Kumluca, Antalya", "categories": ["Adventure", "Nature"], "tags": ["adventure", "nature"]},
    ],
    "Bursa": [
        {"name": "Uludag Kayak Merkezi", "description": "Turkey's most famous ski resort on the slopes of Mount Uludag, accessible by cable car from the city.", "duration_hours": 6.0, "price": 1200.0, "address": "Uludag, Bursa", "categories": ["Adventure", "Nature"], "tags": ["adventure", "family-friendly"]},
        {"name": "Ulu Cami", "description": "Magnificent early Ottoman mosque with 20 domes and intricate calligraphic panels, a jewel of Bursa.", "duration_hours": 1.0, "price": 0.0, "address": "Orhan Gazi, Osmangazi", "categories": ["Historical", "Religious"], "tags": ["cultural"]},
        {"name": "Koza Hani", "description": "Ottoman caravanserai at the heart of the silk trade, still selling silk cocoons and textiles today.", "duration_hours": 1.5, "price": 0.0, "address": "Kapali Carsi, Osmangazi", "categories": ["Historical"], "tags": ["cultural", "budget"]},
    ],
    "Adana": [
        {"name": "Tas Kopru", "description": "Roman stone bridge over the Seyhan River, the longest surviving Roman bridge in the world.", "duration_hours": 1.0, "price": 0.0, "address": "Seyhan Nehri, Seyhan", "categories": ["Historical"], "tags": ["cultural", "budget"]},
        {"name": "Adana Kebab Turu", "description": "Taste the famous spicy Adana kebab at the legendary restaurant district along Ataturk Boulevard.", "duration_hours": 2.0, "price": 250.0, "address": "Ataturk Cad., Seyhan", "categories": ["Food & Drink"], "tags": ["foodie", "budget"]},
        {"name": "Sabanci Merkez Camii", "description": "One of the largest mosques in the Middle East with soaring minarets and marble courtyards.", "duration_hours": 1.0, "price": 0.0, "address": "Seyhan, Adana", "categories": ["Religious"], "tags": ["cultural"]},
    ],
    "Gaziantep": [
        {"name": "Zeugma Mozaik Muzesi", "description": "World's largest mosaic museum, housing extraordinary Roman mosaics including the legendary Gypsy Girl.", "duration_hours": 3.0, "price": 200.0, "address": "Mithatpasa Cad., Sahinbey", "categories": ["Museum"], "tags": ["cultural", "family-friendly"]},
        {"name": "Antep Baklava Turu", "description": "Visit master pastry makers and sample fresh pistachio baklava in Gaziantep's famed bakery district.", "duration_hours": 2.0, "price": 150.0, "address": "Uzun Carsi, Sahinbey", "categories": ["Food & Drink"], "tags": ["foodie"]},
        {"name": "Gaziantep Kalesi", "description": "Basalt fortress dating to the Roman era dominating the city centre, housing a panoramic museum.", "duration_hours": 1.5, "price": 100.0, "address": "Sahinbey, Gaziantep", "categories": ["Historical"], "tags": ["cultural"]},
    ],
    "Konya": [
        {"name": "Mevlana Muzesi", "description": "Shrine and museum of Rumi, the Sufi poet, in the iconic turquoise-tiled lodge — spiritually profound.", "duration_hours": 2.0, "price": 0.0, "address": "Mevlana Cad., Karatay", "categories": ["Museum", "Religious"], "tags": ["cultural", "family-friendly"]},
        {"name": "Sema Toreni", "description": "Witness the hypnotic whirling dervish ceremony performed by the Mevlevi Order in traditional costume.", "duration_hours": 1.5, "price": 0.0, "address": "Mevlana Kulturel Merkezi", "categories": ["Religious"], "tags": ["cultural", "romantic"]},
        {"name": "Catalhoyuk Neolitik Kenti", "description": "9000-year-old Neolithic settlement, one of the earliest known cities and a UNESCO World Heritage site.", "duration_hours": 3.0, "price": 150.0, "address": "Cumra, Konya", "categories": ["Museum", "Historical"], "tags": ["cultural"]},
    ],
    "Mersin": [
        {"name": "Kiz Kalesi", "description": "Romantic sea castle on a tiny island just offshore, legend-rich and beautifully set against the Taurus Mountains.", "duration_hours": 2.0, "price": 100.0, "address": "Kizkalesi, Erdemli", "categories": ["Historical"], "tags": ["romantic", "cultural"]},
        {"name": "Mersin Sahil Yuruyusu", "description": "Long palm-lined seafront promenade, perfect for a morning walk with views across to Cyprus on clear days.", "duration_hours": 1.5, "price": 0.0, "address": "Merkez, Mersin", "categories": ["Nature"], "tags": ["budget", "family-friendly"]},
    ],
    "Diyarbakir": [
        {"name": "Suru Surlari", "description": "UNESCO World Heritage basalt city walls encircling the old city — the longest Roman fortifications in the world.", "duration_hours": 2.5, "price": 0.0, "address": "Sur, Diyarbakir", "categories": ["Historical"], "tags": ["cultural"]},
        {"name": "Hasan Pasa Hani", "description": "16th-century caravanserai in the heart of the bazaar, now buzzing with tea houses, copper smiths, and carpet sellers.", "duration_hours": 1.5, "price": 0.0, "address": "Sur, Diyarbakir", "categories": ["Historical"], "tags": ["cultural", "budget"]},
    ],
    "Trabzon": [
        {"name": "Sumela Manastiri", "description": "Cliff-hanging 4th-century Greek Orthodox monastery carved into a sheer rock face in a misty mountain gorge.", "duration_hours": 3.0, "price": 200.0, "address": "Altindere, Macka", "categories": ["Historical", "Religious", "Nature"], "tags": ["cultural", "adventure"]},
        {"name": "Uzungol", "description": "Serene highland lake surrounded by forested mountains — one of Turkey's most photographed landscapes.", "duration_hours": 4.0, "price": 0.0, "address": "Uzungol, Caykara", "categories": ["Nature"], "tags": ["nature", "romantic", "family-friendly"]},
        {"name": "Aya Sofya Trabzon", "description": "13th-century Byzantine church with remarkable frescoes, later converted to a mosque, by the Black Sea.", "duration_hours": 1.0, "price": 0.0, "address": "Ortahisar, Trabzon", "categories": ["Museum", "Historical", "Religious"], "tags": ["cultural"]},
    ],
    "Kayseri": [
        {"name": "Erciyes Dag Kayagi", "description": "Skiing and snowboarding on the slopes of the 3916-metre volcanic Mount Erciyes, Turkey's top ski resort.", "duration_hours": 6.0, "price": 1500.0, "address": "Talas, Kayseri", "categories": ["Adventure", "Nature"], "tags": ["adventure", "family-friendly"]},
        {"name": "Kayseri Kapali Carsi", "description": "One of Anatolia's oldest covered bazaars, where pastirma and sucuk artisans have traded for centuries.", "duration_hours": 2.0, "price": 0.0, "address": "Cumhuriyet, Kocasinan", "categories": ["Historical"], "tags": ["cultural", "foodie", "budget"]},
    ],
    "Eskisehir": [
        {"name": "Porsuk Cayi Tekne Turu", "description": "Gondola ride along Porsuk Creek through the colourful historic quarter — Turkey's little Venice.", "duration_hours": 1.0, "price": 150.0, "address": "Odunpazari, Eskisehir", "categories": ["Nature"], "tags": ["romantic", "family-friendly"]},
        {"name": "Odunpazari Tarihi Mahalle", "description": "Restored Ottoman neighbourhood with brightly painted houses, local art galleries, and craft workshops.", "duration_hours": 2.0, "price": 0.0, "address": "Odunpazari, Eskisehir", "categories": ["Historical"], "tags": ["cultural", "romantic"]},
        {"name": "Lületasi Muzesi", "description": "Museum dedicated to meerschaum (lületası), the white mineral found only near Eskisehir, hand-carved into pipes.", "duration_hours": 1.0, "price": 50.0, "address": "Odunpazari, Eskisehir", "categories": ["Museum"], "tags": ["cultural"]},
    ],
    "Samsun": [
        {"name": "Ataturk Aniti", "description": "Monumental sculpture of Ataturk on horseback at the spot where he landed to begin the Turkish War of Independence.", "duration_hours": 0.5, "price": 0.0, "address": "Cumhuriyet Meydani, Ilkadim", "categories": ["Historical"], "tags": ["cultural", "budget"]},
        {"name": "19 Mayis Milli Parki", "description": "Large national park east of Samsun with lake, beaches, and forests ideal for picnics and cycling.", "duration_hours": 3.0, "price": 0.0, "address": "19 Mayis, Samsun", "categories": ["Nature"], "tags": ["nature", "family-friendly", "budget"]},
    ],
    "Denizli": [
        {"name": "Pamukkale Travertenleri", "description": "Walk barefoot on snowy-white calcium terraces formed by thermal springs cascading over millennia.", "duration_hours": 3.0, "price": 600.0, "address": "Pamukkale Koyu, Pamukkale", "categories": ["Nature"], "tags": ["family-friendly", "nature"]},
        {"name": "Hierapolis Antik Kenti", "description": "Roman spa city above Pamukkale with a theatre, necropolis, and the world's first known thermal pool.", "duration_hours": 3.0, "price": 600.0, "address": "Pamukkale, Denizli", "categories": ["Historical", "Museum"], "tags": ["cultural", "family-friendly"]},
    ],
    "Bodrum": [
        {"name": "Bodrum Kalesi ve Sualt Arkeoloji Muzesi", "description": "Crusader castle housing the world's finest museum of ancient maritime archaeology, including the Uluburun shipwreck.", "duration_hours": 3.0, "price": 300.0, "address": "Kaleiçi, Bodrum", "categories": ["Museum", "Historical"], "tags": ["cultural", "family-friendly"]},
        {"name": "Gundogdu Koyu Tekne Turu", "description": "Blue Voyage boat trip around Bodrum's crystal coves, with snorkelling, cliff jumping, and sunset views.", "duration_hours": 8.0, "price": 1200.0, "address": "Bodrum Limani", "categories": ["Beach", "Adventure"], "tags": ["adventure", "romantic"]},
    ],
    "Cappadocia": [
        {"name": "Sicak Hava Balonu Turu", "description": "Float over fairy chimneys and rose-coloured valleys at sunrise — an unforgettable bucket-list experience.", "duration_hours": 3.0, "price": 3500.0, "address": "Goreme, Nevsehir", "categories": ["Adventure", "Nature"], "tags": ["romantic", "adventure"]},
        {"name": "Goreme Acik Hava Muzesi", "description": "UNESCO World Heritage complex of rock-cut Byzantine churches with brilliant 10th-century frescoes.", "duration_hours": 2.0, "price": 360.0, "address": "Goreme, Nevsehir", "categories": ["Museum", "Historical", "Religious"], "tags": ["cultural", "family-friendly"]},
        {"name": "Derinkuyu Yeralti Sehri", "description": "Descend 85 metres into an ancient underground city carved by the Phrygians, large enough for 20,000 people.", "duration_hours": 2.5, "price": 300.0, "address": "Derinkuyu, Nevsehir", "categories": ["Historical", "Adventure"], "tags": ["adventure", "cultural"]},
        {"name": "At Turu Kizilcukur Vadisi", "description": "Horseback ride through Red Valley's rust-coloured rock formations at golden hour.", "duration_hours": 2.0, "price": 800.0, "address": "Cavusin, Avanos", "categories": ["Adventure", "Nature"], "tags": ["adventure", "romantic"]},
    ],
    "Safranbolu": [
        {"name": "Cinci Han", "description": "Imposing 17th-century Ottoman caravanserai with massive stone arches, now a charming hotel and cultural space.", "duration_hours": 1.0, "price": 0.0, "address": "Carsı Mahallesi, Safranbolu", "categories": ["Historical"], "tags": ["cultural", "romantic"]},
        {"name": "Safranbolu Tarihi Evleri Turu", "description": "Walk through perfectly preserved Ottoman mansions and buy handmade Turkish delight flavoured with local saffron.", "duration_hours": 2.0, "price": 0.0, "address": "Carsı Mahallesi, Safranbolu", "categories": ["Historical"], "tags": ["cultural", "budget"]},
    ],
    "Sanliurfa": [
        {"name": "Balikligol", "description": "Sacred pool of sacred carp fed by the spring where Abraham is believed to have been cast into Nimrod's fire.", "duration_hours": 1.5, "price": 0.0, "address": "Golbasi, Sanliurfa", "categories": ["Religious", "Historical"], "tags": ["cultural", "family-friendly", "budget"]},
        {"name": "Gobeklitepe", "description": "World's oldest known temple complex at 12,000 years old, rewriting the history of human civilisation.", "duration_hours": 3.0, "price": 200.0, "address": "Orencik Koyu, Sanliurfa", "categories": ["Historical", "Museum"], "tags": ["cultural", "adventure"]},
        {"name": "Sanliurfa Kapali Carsi", "description": "Labyrinthine bazaar of spice sellers, coppersmiths, and weavers producing the famous Sanliurfa kilims.", "duration_hours": 2.0, "price": 0.0, "address": "Golbasi, Sanliurfa", "categories": ["Historical"], "tags": ["cultural", "budget", "foodie"]},
    ],
    "Van": [
        {"name": "Van Golu Teknesi", "description": "Boat trip across the vast saline lake to the hauntingly beautiful Akdamar Island Armenian Church.", "duration_hours": 4.0, "price": 400.0, "address": "Iskele, Edremit", "categories": ["Historical", "Nature", "Religious"], "tags": ["cultural", "nature"]},
        {"name": "Akdamar Kilisesi", "description": "10th-century Armenian Holy Cross Church on a lake island, with vivid carved biblical scenes on its exterior.", "duration_hours": 2.0, "price": 100.0, "address": "Akdamar Adasi, Gevas", "categories": ["Historical", "Religious", "Museum"], "tags": ["cultural"]},
        {"name": "Van Kalesi", "description": "Urartian fortress towering over the lake on a sheer rock, with cuneiform inscriptions of King Sarduri.", "duration_hours": 2.0, "price": 100.0, "address": "Sarihorak Koyu, Edremit", "categories": ["Historical"], "tags": ["cultural", "adventure"]},
    ],
    "Erzurum": [
        {"name": "Cifte Minareli Medrese", "description": "Twin-minareted 13th-century Ilkhanid theological school with stunning stonework — an iconic symbol of Erzurum.", "duration_hours": 1.0, "price": 0.0, "address": "Cumhuriyet, Yakutiye", "categories": ["Historical", "Religious"], "tags": ["cultural"]},
        {"name": "Palandoken Kayak Merkezi", "description": "International-standard ski resort within minutes of the city centre, with 38 km of piste.", "duration_hours": 6.0, "price": 1000.0, "address": "Palandoken, Erzurum", "categories": ["Adventure", "Nature"], "tags": ["adventure"]},
    ],
    "Mardin": [
        {"name": "Zinciriye Medresesi", "description": "15th-century madrasa with remarkable honeycomb stonework and a rooftop terrace offering views across Mesopotamia.", "duration_hours": 1.5, "price": 50.0, "address": "Birinci Cadde, Artuklu", "categories": ["Historical", "Religious"], "tags": ["cultural", "romantic"]},
        {"name": "Deyrulzafaran Manastiri", "description": "4th-century Syriac Orthodox monastery, the seat of the Patriarchate — still an active religious community.", "duration_hours": 2.0, "price": 100.0, "address": "Mardin-Midyat yolu", "categories": ["Historical", "Religious"], "tags": ["cultural"]},
        {"name": "Mardin Tarihi Carsi", "description": "Cobblestone alleyways lined with silver jewellery, spice shops, and tandir bread bakeries in the old city.", "duration_hours": 2.0, "price": 0.0, "address": "Cumhuriyet Cad., Artuklu", "categories": ["Historical"], "tags": ["cultural", "budget", "foodie"]},
    ],
    "Afyonkarahisar": [
        {"name": "Afyon Kalesi", "description": "Volcanic rock fortress rising 226 metres above the city, with sweeping views of poppy-filled plains.", "duration_hours": 1.5, "price": 50.0, "address": "Zafer, Merkez", "categories": ["Historical"], "tags": ["cultural", "adventure"]},
        {"name": "Gazligol Termal Kaplicalari", "description": "Thermal spa resort in a beautiful valley — natural hot springs have healed travellers here since Roman times.", "duration_hours": 3.0, "price": 400.0, "address": "Gazligol, Afyon", "categories": ["Nature"], "tags": ["romantic", "family-friendly"]},
    ],
    "Canakkale": [
        {"name": "Truva Antik Kenti", "description": "Archaeological site of legendary Troy, with nine successive cities spanning 4000 years of human history.", "duration_hours": 3.0, "price": 300.0, "address": "Tevfikiye Koyu, Canakkale", "categories": ["Historical", "Museum"], "tags": ["cultural", "family-friendly"]},
        {"name": "Gelibolu Yarimadasi", "description": "Profoundly moving WWI battlefields and ANZAC memorials on the peninsula where Ataturk rose to fame.", "duration_hours": 4.0, "price": 0.0, "address": "Eceabat, Canakkale", "categories": ["Historical"], "tags": ["cultural"]},
        {"name": "Cumenlik Kalesi", "description": "Ottoman fortress controlling the narrows of the Dardanelles, housing a military museum.", "duration_hours": 1.5, "price": 100.0, "address": "Intepe Koyu, Canakkale", "categories": ["Historical", "Museum"], "tags": ["cultural"]},
    ],
    "Edirne": [
        {"name": "Selimiye Camii", "description": "Sinan's masterpiece and UNESCO World Heritage mosque, considered the peak of Ottoman architecture.", "duration_hours": 1.5, "price": 0.0, "address": "Mimar Sinan Cad., Merkez", "categories": ["Historical", "Religious"], "tags": ["cultural"]},
        {"name": "Kirkpinar Gures Alani", "description": "Stadium and grounds of the world's oldest sporting event — the Kırkpınar oil wrestling festival since 1362.", "duration_hours": 2.0, "price": 0.0, "address": "Sarayici Adasi, Edirne", "categories": ["Historical"], "tags": ["cultural"]},
    ],
    "Balikesir": [
        {"name": "Ayvalik Adalari", "description": "Boat tour through the Ayvalik archipelago of pine-covered islands with turquoise water and secluded beaches.", "duration_hours": 6.0, "price": 800.0, "address": "Ayvalik Limani", "categories": ["Beach", "Nature"], "tags": ["romantic", "nature", "adventure"]},
        {"name": "Seytan Sofrasi", "description": "Hilltop lookout on Lesbos-facing peninsula — a legendary viewpoint above Ayvalik's olive-clad islands.", "duration_hours": 1.0, "price": 0.0, "address": "Seytan Sofrasi, Ayvalik", "categories": ["Nature"], "tags": ["romantic", "budget"]},
    ],
    "Malatya": [
        {"name": "Aslantepe Hoyugu", "description": "One of Turkey's most important Neolithic and Iron Age mound sites, dating back 5000 years.", "duration_hours": 2.0, "price": 100.0, "address": "Orduzu, Battalgazi", "categories": ["Historical", "Museum"], "tags": ["cultural"]},
        {"name": "Malatya Kaysisi Bahceleri", "description": "Walk through vast golden apricot orchards during harvest season and taste sun-dried apricots straight from the tree.", "duration_hours": 2.0, "price": 0.0, "address": "Arguvan, Malatya", "categories": ["Nature", "Food & Drink"], "tags": ["foodie", "nature", "family-friendly"]},
    ],
    "Kahramanmaras": [
        {"name": "Maras Dondurmasi Deneyimi", "description": "Watch the theatrical mastic ice cream stretching performance and sample the world-famous chewy Maras dondurma.", "duration_hours": 1.0, "price": 50.0, "address": "Trabzon Cad., Dulkadiroglular", "categories": ["Food & Drink"], "tags": ["foodie", "family-friendly", "budget"]},
        {"name": "Kahramanmaras Kalesi", "description": "Hilltop citadel with sweeping views of the Taurus foothills, incorporating Roman, Byzantine, and Mamluk stonework.", "duration_hours": 1.5, "price": 50.0, "address": "Karacay, Dulkadiroglular", "categories": ["Historical"], "tags": ["cultural"]},
    ],
    "Alanya": [
        {"name": "Alanya Kalesi ve Kizil Kule", "description": "Seljuk hilltop fortress with stunning sea views and the iconic Red Tower harbour fortification below.", "duration_hours": 3.0, "price": 200.0, "address": "Iskele, Alanya", "categories": ["Historical"], "tags": ["cultural", "family-friendly"]},
        {"name": "Damlatas Magarasi", "description": "Stalactite cave at sea level, noted for its therapeutic microclimate recommended for respiratory ailments.", "duration_hours": 1.0, "price": 120.0, "address": "Alaaddin, Alanya", "categories": ["Nature"], "tags": ["family-friendly", "nature"]},
        {"name": "Kleopatra Plaji", "description": "Legendary beach of golden sand and clear water where Cleopatra is said to have bathed with Mark Antony.", "duration_hours": 4.0, "price": 0.0, "address": "Oba, Alanya", "categories": ["Beach"], "tags": ["romantic", "family-friendly", "budget"]},
    ],
    "Pamukkale": [
        {"name": "Antik Havuz", "description": "Swim among sunken Roman columns in the original Cleopatra's Pool — a warm thermal spring at Hierapolis.", "duration_hours": 2.0, "price": 750.0, "address": "Pamukkale Koyu, Denizli", "categories": ["Historical", "Nature"], "tags": ["romantic", "adventure"]},
        {"name": "Hierapolis Nekropolu", "description": "One of the largest and best-preserved ancient necropolises in the world, with thousands of sarcophagi.", "duration_hours": 1.5, "price": 0.0, "address": "Pamukkale, Denizli", "categories": ["Historical"], "tags": ["cultural"]},
    ],
}

# ── Restaurants ───────────────────────────────────────────────────────────────

_RESTAURANTS: dict[str, list[dict]] = {
    "Istanbul": [
        {"name": "Mikla", "cuisine_type": "Modern Turkish", "price_range": "luxury", "address": "Mesrutiyet Cad. 15, Beyoglu", "rating": 4.8},
        {"name": "Karakoy Lokantasi", "cuisine_type": "Traditional Turkish", "price_range": "mid", "address": "Kemankescad. 37, Karakoy", "rating": 4.5},
        {"name": "Develi Balik", "cuisine_type": "Ottoman Seafood", "price_range": "luxury", "address": "Kumkapi, Fatih", "rating": 4.6},
    ],
    "Ankara": [
        {"name": "Trilye Ankara", "cuisine_type": "Turkish Seafood", "price_range": "luxury", "address": "Kucukesat, Cankaya", "rating": 4.6},
        {"name": "Namlı Lokanta", "cuisine_type": "Anatolian", "price_range": "mid", "address": "Ulus, Altindag", "rating": 4.3},
    ],
    "Izmir": [
        {"name": "Deniz Restaurant", "cuisine_type": "Aegean Seafood", "price_range": "luxury", "address": "Ataturk Cad. 188, Alsancak", "rating": 4.7},
        {"name": "Sakiz Balikhane", "cuisine_type": "Aegean Meyhane", "price_range": "mid", "address": "Kemeralti, Konak", "rating": 4.4},
    ],
    "Antalya": [
        {"name": "Seven", "cuisine_type": "Mediterranean Fine Dining", "price_range": "luxury", "address": "Kaleici, Muratpasa", "rating": 4.7},
        {"name": "Afrodit Restaurant", "cuisine_type": "Turkish & Seafood", "price_range": "mid", "address": "Konyaalti Plaji", "rating": 4.4},
    ],
    "Bursa": [
        {"name": "Kebapci Iskender", "cuisine_type": "Iskender Kebab", "price_range": "mid", "address": "Unlu Cad. 7, Osmangazi", "rating": 4.7},
        {"name": "Tarihi Cekirge Hamamı Restoran", "cuisine_type": "Traditional Turkish", "price_range": "mid", "address": "Cekirge, Osmangazi", "rating": 4.3},
    ],
    "Adana": [
        {"name": "Kebapci Mesut", "cuisine_type": "Adana Kebab", "price_range": "budget", "address": "Ataturk Cad., Seyhan", "rating": 4.6},
        {"name": "Yüregir Restaurant", "cuisine_type": "Southern Turkish", "price_range": "mid", "address": "Yuregiryolu, Seyhan", "rating": 4.4},
    ],
    "Gaziantep": [
        {"name": "Imam Cagdas", "cuisine_type": "Antep Kebab & Baklava", "price_range": "mid", "address": "Uzun Carsi 49, Sahinbey", "rating": 4.8},
        {"name": "Metanet Lokantasi", "cuisine_type": "Gaziantep Traditional", "price_range": "budget", "address": "Kagit Pazari, Sahinbey", "rating": 4.5},
    ],
    "Konya": [
        {"name": "Sifa Restaurant", "cuisine_type": "Konya Cuisine", "price_range": "mid", "address": "Mevlana Cad., Karatay", "rating": 4.5},
        {"name": "Gulbahce Konak", "cuisine_type": "Ottoman Anatolian", "price_range": "mid", "address": "Sille Koyu, Selcuklu", "rating": 4.4},
    ],
    "Mersin": [
        {"name": "Toros Balık", "cuisine_type": "Mediterranean Seafood", "price_range": "mid", "address": "Sahil Cad., Akdeniz", "rating": 4.5},
        {"name": "Tantuni Merkezi", "cuisine_type": "Mersin Tantuni", "price_range": "budget", "address": "Cumhuriyet Meydani", "rating": 4.6},
    ],
    "Diyarbakir": [
        {"name": "Selim Amca'nın Sofrası", "cuisine_type": "Kurdish & Turkish", "price_range": "mid", "address": "Gazi Cad., Sur", "rating": 4.5},
        {"name": "Cigerci Memo", "cuisine_type": "Diyarbakir Liver", "price_range": "budget", "address": "Hasanpasa Hani, Sur", "rating": 4.4},
    ],
    "Trabzon": [
        {"name": "Cemil Usta", "cuisine_type": "Black Sea Fish", "price_range": "mid", "address": "Uzun Sokak, Ortahisar", "rating": 4.6},
        {"name": "Nihat'in Yeri", "cuisine_type": "Karadeniz Cuisine", "price_range": "budget", "address": "Kahramanmaras Cad.", "rating": 4.4},
    ],
    "Kayseri": [
        {"name": "Develi Kayseri", "cuisine_type": "Kayseri Testi Kebabi", "price_range": "mid", "address": "Sivas Cad., Kocasinan", "rating": 4.5},
        {"name": "Baylan Pastane", "cuisine_type": "Kayseri Pastry", "price_range": "budget", "address": "Kocasinan, Kayseri", "rating": 4.6},
    ],
    "Eskisehir": [
        {"name": "Cikolata Kapilar", "cuisine_type": "Eclectic European", "price_range": "mid", "address": "Odunpazari, Eskisehir", "rating": 4.4},
        {"name": "Cinful Tavern", "cuisine_type": "Modern Turkish", "price_range": "mid", "address": "Porsuk Kordon, Odunpazari", "rating": 4.5},
    ],
    "Samsun": [
        {"name": "Bafra Pidecisi Mehmet Usta", "cuisine_type": "Black Sea Pide", "price_range": "budget", "address": "Cumhuriyet Cad., Ilkadim", "rating": 4.6},
        {"name": "Sinop Balik Evi", "cuisine_type": "Black Sea Seafood", "price_range": "mid", "address": "Sahil, Atakum", "rating": 4.4},
    ],
    "Denizli": [
        {"name": "Korhan Restaurant", "cuisine_type": "Aegean Turkish", "price_range": "mid", "address": "Pamukkale, Denizli", "rating": 4.4},
        {"name": "Karahayit Lokantasi", "cuisine_type": "Turkish Home Cooking", "price_range": "budget", "address": "Karahayit, Pamukkale", "rating": 4.3},
    ],
    "Bodrum": [
        {"name": "Balikcilar Dernegi", "cuisine_type": "Aegean Fish", "price_range": "luxury", "address": "Kumbahce, Bodrum", "rating": 4.7},
        {"name": "Limon Cafe", "cuisine_type": "Meyhane & Meze", "price_range": "mid", "address": "Neyzen Tevfik Cad.", "rating": 4.5},
    ],
    "Cappadocia": [
        {"name": "Seki Restaurant", "cuisine_type": "Cappadocian Testi", "price_range": "mid", "address": "Goreme, Nevsehir", "rating": 4.6},
        {"name": "Dimrit Cave Restaurant", "cuisine_type": "Anatolian Cave Dining", "price_range": "mid", "address": "Urgup, Nevsehir", "rating": 4.5},
    ],
    "Safranbolu": [
        {"name": "Kadıoğlu Sehzade Sofrasi", "cuisine_type": "Ottoman Safranbolu", "price_range": "mid", "address": "Carsı Mah., Safranbolu", "rating": 4.6},
        {"name": "Mesale Cafe", "cuisine_type": "Turkish Breakfast", "price_range": "budget", "address": "Cinci Han Carsı, Safranbolu", "rating": 4.4},
    ],
    "Sanliurfa": [
        {"name": "Hamdibey Sofrasi", "cuisine_type": "Urfa Kebab & Cigkofte", "price_range": "budget", "address": "Golbasi, Sanliurfa", "rating": 4.6},
        {"name": "Dergah Restaurant", "cuisine_type": "Southeastern Anatolian", "price_range": "mid", "address": "Ataturk Cad., Merkez", "rating": 4.4},
    ],
    "Van": [
        {"name": "Van Kahvalti Evi", "cuisine_type": "Van Breakfast (Otlu Peynir)", "price_range": "budget", "address": "Ipekyolu, Van", "rating": 4.7},
        {"name": "Sütçü Fevzi", "cuisine_type": "Van Dairy Cuisine", "price_range": "budget", "address": "Cumhuriyet Cad., Van", "rating": 4.5},
    ],
    "Erzurum": [
        {"name": "Güzelyurt Cag Kebabi", "cuisine_type": "Erzurum Cag Kebabi", "price_range": "budget", "address": "Kazimkarabekir Cad.", "rating": 4.7},
        {"name": "Askerlik Subesi Arkadaslık Lokali", "cuisine_type": "Erzurum Home Cooking", "price_range": "budget", "address": "Yakutiye, Erzurum", "rating": 4.4},
    ],
    "Mardin": [
        {"name": "Cercis Murat Konagi", "cuisine_type": "Mardin Syriac Cuisine", "price_range": "mid", "address": "1. Cadde, Artuklu", "rating": 4.7},
        {"name": "Artuklu Mutfagi", "cuisine_type": "Kurdish & Arabic Fusion", "price_range": "mid", "address": "Cumhuriyet Cad., Artuklu", "rating": 4.5},
    ],
    "Afyonkarahisar": [
        {"name": "Ikbal Lokantası", "cuisine_type": "Afyon Kaymak & Sucuk", "price_range": "budget", "address": "Bankalar Cad., Merkez", "rating": 4.6},
        {"name": "Gaziantep Kebap Salonu", "cuisine_type": "Central Anatolian Kebab", "price_range": "budget", "address": "Zafer, Afyon", "rating": 4.3},
    ],
    "Canakkale": [
        {"name": "Yalova Restaurant", "cuisine_type": "Dardanelles Seafood", "price_range": "mid", "address": "Yali Cad. 7, Canakkale", "rating": 4.5},
        {"name": "Doyum Pide ve Kebab", "cuisine_type": "Turkish Pide", "price_range": "budget", "address": "Cumhuriyet Myd., Canakkale", "rating": 4.4},
    ],
    "Edirne": [
        {"name": "Ciğer Tava Niyazi Usta", "cuisine_type": "Edirne Tava Cigeri", "price_range": "budget", "address": "Saraclar Cad., Merkez", "rating": 4.6},
        {"name": "Balkan Sofrasi", "cuisine_type": "Thracian Cuisine", "price_range": "mid", "address": "Ali Pasa Carsisi, Merkez", "rating": 4.4},
    ],
    "Balikesir": [
        {"name": "Mevsim Balikevi", "cuisine_type": "Aegean Seafood", "price_range": "mid", "address": "Sahil Cad., Ayvalik", "rating": 4.5},
        {"name": "Zeytinlibahce", "cuisine_type": "Olive Oil & Aegean", "price_range": "mid", "address": "Namli Koyu, Ayvalik", "rating": 4.4},
    ],
    "Malatya": [
        {"name": "Özler Lokantası", "cuisine_type": "Malatya Apricot Cuisine", "price_range": "budget", "address": "Ismetpasa Cad., Battalgazi", "rating": 4.5},
        {"name": "Sehir Kebapçısı", "cuisine_type": "Eastern Anatolian Kebab", "price_range": "budget", "address": "Ataturk Cad., Merkez", "rating": 4.3},
    ],
    "Kahramanmaras": [
        {"name": "Yasar Pastanesi", "cuisine_type": "Maras Dondurma", "price_range": "budget", "address": "Trabzon Cad., Dulkadiroglular", "rating": 4.7},
        {"name": "Kervan Kebap", "cuisine_type": "Southern Anatolian Kebab", "price_range": "budget", "address": "Ataturk Blv., Merkez", "rating": 4.4},
    ],
    "Alanya": [
        {"name": "Ottoman House", "cuisine_type": "Turkish Mediterranean", "price_range": "mid", "address": "Damlatas Cad., Alaaddin", "rating": 4.5},
        {"name": "Red Tower Brewery", "cuisine_type": "Craft Beer & Meze", "price_range": "mid", "address": "Iskele Cad., Alanya", "rating": 4.4},
    ],
    "Pamukkale": [
        {"name": "Mehmet's Heaven Restaurant", "cuisine_type": "Turkish Homestyle", "price_range": "budget", "address": "Pamukkale Koyu", "rating": 4.5},
        {"name": "Kayas Restaurant", "cuisine_type": "Turkish & International", "price_range": "mid", "address": "Pamukkale, Denizli", "rating": 4.3},
    ],
}

# ── Accommodations ────────────────────────────────────────────────────────────

_ACCOMMODATIONS: dict[str, list[dict]] = {
    "Istanbul": [
        {"name": "Four Seasons Sultanahmet", "type": "hotel", "star_rating": 5, "price_per_night": 8500.0, "address": "Tevkifhane Sok. 1, Sultanahmet"},
        {"name": "Witt Istanbul Suites", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 3200.0, "address": "Defterdar Yokusu 26, Cihangir"},
        {"name": "Istanbul Hostel Beyoglu", "type": "hostel", "star_rating": 2, "price_per_night": 350.0, "address": "Istiklal Cad., Beyoglu"},
    ],
    "Ankara": [
        {"name": "JW Marriott Ankara", "type": "hotel", "star_rating": 5, "price_per_night": 4500.0, "address": "Sogutozu Cad. 2, Cankaya"},
        {"name": "Hotel Angora", "type": "hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Ataturk Blv. 183, Kavaklidere"},
    ],
    "Izmir": [
        {"name": "Swissotel Grand Efes Izmir", "type": "hotel", "star_rating": 5, "price_per_night": 5500.0, "address": "Gaziosmanpasa Blv. 1, Alsancak"},
        {"name": "Manzara Izmir", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2200.0, "address": "Kemeralti, Konak"},
        {"name": "Izmir Backpackers", "type": "hostel", "star_rating": 2, "price_per_night": 400.0, "address": "Alsancak, Izmir"},
    ],
    "Antalya": [
        {"name": "Akra Hotel Antalya", "type": "hotel", "star_rating": 5, "price_per_night": 6000.0, "address": "Konyaalti, Antalya"},
        {"name": "Alp Pasa Boutique Hotel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2800.0, "address": "Kaleici, Muratpasa"},
        {"name": "White Garden Hostel", "type": "hostel", "star_rating": 2, "price_per_night": 500.0, "address": "Barbaros Mah., Kaleici"},
    ],
    "Bursa": [
        {"name": "Marmara Ciftlik", "type": "resort", "star_rating": 4, "price_per_night": 3500.0, "address": "Uludag Yolu, Bursa"},
        {"name": "Termal Grand Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 2000.0, "address": "Cekirge Mey., Osmangazi"},
    ],
    "Adana": [
        {"name": "Hilton Adana", "type": "hotel", "star_rating": 5, "price_per_night": 3000.0, "address": "Sinanpasa Mah., Seyhan"},
        {"name": "Seyhan Hotel", "type": "hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Turhan Cemal, Seyhan"},
    ],
    "Gaziantep": [
        {"name": "Tugcan Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 2000.0, "address": "Istasyon Cad. 4, Sahinbey"},
        {"name": "Anadolu Evleri", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2500.0, "address": "Tekkemescit Mah., Sahinbey"},
    ],
    "Konya": [
        {"name": "Rixos Konya", "type": "hotel", "star_rating": 5, "price_per_night": 3500.0, "address": "Nalcaci Cad. 20, Meram"},
        {"name": "Dervish Cave Hotel", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1500.0, "address": "Beyhekim, Karatay"},
    ],
    "Mersin": [
        {"name": "Hilton Mersin", "type": "hotel", "star_rating": 5, "price_per_night": 3200.0, "address": "Adnan Menderes Blv., Akdeniz"},
        {"name": "Hotel Mersin", "type": "hotel", "star_rating": 3, "price_per_night": 1000.0, "address": "Istasyon Cad., Akdeniz"},
    ],
    "Diyarbakir": [
        {"name": "Hotel Ceylan Diyarbakir", "type": "hotel", "star_rating": 4, "price_per_night": 1800.0, "address": "Kibris Cad. 4, Baglar"},
        {"name": "Diyarbakir Butik Otel", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Sur, Diyarbakir"},
    ],
    "Trabzon": [
        {"name": "Zorlu Grand Hotel", "type": "hotel", "star_rating": 5, "price_per_night": 3000.0, "address": "Maras Cad. 9, Ortahisar"},
        {"name": "Uzungol Dogal Ahsap Evler", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1400.0, "address": "Uzungol, Caykara"},
    ],
    "Kayseri": [
        {"name": "Ramada Kayseri", "type": "hotel", "star_rating": 4, "price_per_night": 2200.0, "address": "Hastane Cad. 2, Kocasinan"},
        {"name": "Erciyes Ski Lodge", "type": "resort", "star_rating": 3, "price_per_night": 1800.0, "address": "Talas, Kayseri"},
    ],
    "Eskisehir": [
        {"name": "DoubleTree by Hilton Eskisehir", "type": "hotel", "star_rating": 5, "price_per_night": 2800.0, "address": "Arifiye Mah., Tepebaşı"},
        {"name": "Odunpazari Konagi", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1500.0, "address": "Odunpazari, Eskisehir"},
    ],
    "Samsun": [
        {"name": "Samsun Buyuk Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 1800.0, "address": "Ataturk Blv. 629, Ilkadim"},
        {"name": "Liva Otel Samsun", "type": "hotel", "star_rating": 3, "price_per_night": 900.0, "address": "Kale, Ilkadim"},
    ],
    "Denizli": [
        {"name": "Doğa Thermal & Spa", "type": "resort", "star_rating": 4, "price_per_night": 2500.0, "address": "Karahayit, Pamukkale"},
        {"name": "Artemis Yoruk Hotel", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1400.0, "address": "Pamukkale Koyu"},
    ],
    "Bodrum": [
        {"name": "Kempinski Hotel Barbaros Bay", "type": "resort", "star_rating": 5, "price_per_night": 10000.0, "address": "Gerenkuyu Mevkii, Bodrum"},
        {"name": "Manastır Hotel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 3500.0, "address": "Barlar Sok. 18, Bodrum"},
        {"name": "Nick's Boutique Hostel", "type": "hostel", "star_rating": 2, "price_per_night": 600.0, "address": "Bodrum Merkez"},
    ],
    "Cappadocia": [
        {"name": "Museum Hotel Cappadocia", "type": "boutique_hotel", "star_rating": 5, "price_per_night": 9000.0, "address": "Tekelli Mah. 1, Urgup"},
        {"name": "Kelebek Cave Hotel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2800.0, "address": "Aydinli Mah., Goreme"},
        {"name": "Goreme Backpacker", "type": "hostel", "star_rating": 2, "price_per_night": 450.0, "address": "Goreme, Nevsehir"},
    ],
    "Safranbolu": [
        {"name": "Cinci Han Boutique", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2200.0, "address": "Cinci Han, Safranbolu"},
        {"name": "Efe Guesthouse", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Carsı Mah., Safranbolu"},
    ],
    "Sanliurfa": [
        {"name": "HiltonGarden Sanliurfa", "type": "hotel", "star_rating": 4, "price_per_night": 2000.0, "address": "Ataturk Blv., Merkez"},
        {"name": "Kasım Padişah Konagi", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1600.0, "address": "Golbasi, Sanliurfa"},
    ],
    "Van": [
        {"name": "Buyuk Urartu Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 1800.0, "address": "Cumhuriyet Cad. 60, Ipekyolu"},
        {"name": "Akdamar Ada Hotel", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Edremit, Van"},
    ],
    "Erzurum": [
        {"name": "Polat Renaissance Erzurum", "type": "resort", "star_rating": 5, "price_per_night": 4000.0, "address": "Palandoken Kayak Merkezi"},
        {"name": "Grand Erzurum Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 1800.0, "address": "Kazimkarabekir Cad., Yakutiye"},
    ],
    "Mardin": [
        {"name": "Erdoba Elegance Hotel", "type": "boutique_hotel", "star_rating": 5, "price_per_night": 5000.0, "address": "1. Cad., Artuklu"},
        {"name": "Dara Butik Otel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2500.0, "address": "Cumhuriyet Cad., Artuklu"},
    ],
    "Afyonkarahisar": [
        {"name": "Ikbal Thermal Hotel", "type": "resort", "star_rating": 5, "price_per_night": 4000.0, "address": "Gazligol, Afyon"},
        {"name": "Afyon Kaymakci Otel", "type": "hotel", "star_rating": 3, "price_per_night": 1000.0, "address": "Zafer, Merkez"},
    ],
    "Canakkale": [
        {"name": "Kolin Hotel Canakkale", "type": "hotel", "star_rating": 5, "price_per_night": 3500.0, "address": "Kepez, Canakkale"},
        {"name": "Anzac Hotel Canakkale", "type": "hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Saat Kulesi Mey., Canakkale"},
        {"name": "Yellow Rose Pension", "type": "hostel", "star_rating": 2, "price_per_night": 500.0, "address": "Yali Cad. 5, Canakkale"},
    ],
    "Edirne": [
        {"name": "Edirne Palace Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 2000.0, "address": "Mimar Sinan Cad., Merkez"},
        {"name": "Trakya Hotel", "type": "hotel", "star_rating": 3, "price_per_night": 900.0, "address": "Saraclar Cad., Merkez"},
    ],
    "Balikesir": [
        {"name": "Ayvalik Ceylan Hotel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2000.0, "address": "Sahil Cad., Ayvalik"},
        {"name": "Taksiarkis Hotel", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1400.0, "address": "Cunda Adasi, Ayvalik"},
    ],
    "Malatya": [
        {"name": "Malatya Buyuk Hotel", "type": "hotel", "star_rating": 4, "price_per_night": 1500.0, "address": "Ismetpasa Cad., Battalgazi"},
        {"name": "Hotel Buyuk Malatya", "type": "hotel", "star_rating": 3, "price_per_night": 800.0, "address": "PTT Karsisi, Merkez"},
    ],
    "Kahramanmaras": [
        {"name": "Ramada Kahramanmaras", "type": "hotel", "star_rating": 4, "price_per_night": 1600.0, "address": "Trabzon Cad., Dulkadiroglular"},
        {"name": "Grand Otel Maras", "type": "hotel", "star_rating": 3, "price_per_night": 900.0, "address": "Ataturk Blv., Merkez"},
    ],
    "Alanya": [
        {"name": "Granada Luxury Alanya", "type": "resort", "star_rating": 5, "price_per_night": 7000.0, "address": "Oba, Alanya"},
        {"name": "Alanya Boutique Hotel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2500.0, "address": "Kaleici, Alanya"},
        {"name": "Backpacker Cave Hostel", "type": "hostel", "star_rating": 2, "price_per_night": 500.0, "address": "Alaaddin, Alanya"},
    ],
    "Pamukkale": [
        {"name": "Venus Suite Hotel", "type": "boutique_hotel", "star_rating": 4, "price_per_night": 2000.0, "address": "Pamukkale Koyu"},
        {"name": "Melrose House", "type": "boutique_hotel", "star_rating": 3, "price_per_night": 1200.0, "address": "Pamukkale, Denizli"},
    ],
}

# ── Festivals ─────────────────────────────────────────────────────────────────

_FESTIVALS: dict[str, list[dict]] = {
    "Istanbul": [
        {"name": "Istanbul Film Festivali", "description": "International film festival showcasing global and Turkish cinema at historic venues across the city.", "start_date": "2025-04-04", "end_date": "2025-04-17", "is_recurring": True, "ticket_price": 120.0},
        {"name": "Istanbul Caz Festivali", "description": "World-class jazz festival bringing international artists to outdoor stages along the Bosphorus.", "start_date": "2025-07-01", "end_date": "2025-07-20", "is_recurring": True, "ticket_price": 250.0},
        {"name": "Lale Festivali", "description": "Tulip festival celebrating millions of blooms in city parks, a breathtaking spring tradition since Ottoman times.", "start_date": "2025-04-01", "end_date": "2025-04-30", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Edirne": [
        {"name": "Kırkpınar Yagli Gures Festivali", "description": "World's oldest sporting event — the legendary Kırkpınar oil wrestling championship held since 1362.", "start_date": "2025-07-04", "end_date": "2025-07-06", "is_recurring": True, "ticket_price": 100.0},
    ],
    "Antalya": [
        {"name": "Altın Portakal Film Festivali", "description": "Turkey's most prestigious film festival screening Turkish cinema under the Mediterranean sun.", "start_date": "2025-10-10", "end_date": "2025-10-17", "is_recurring": True, "ticket_price": 80.0},
        {"name": "Antalya Piyasa Festivali", "description": "Lively summer street festival with live music, crafts, and food along the seafront promenade.", "start_date": "2025-07-15", "end_date": "2025-07-20", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Izmir": [
        {"name": "Izmir Enternasyonal Fuari", "description": "Turkey's oldest international trade fair, combining commerce, culture, and concerts for ten days every September.", "start_date": "2025-09-07", "end_date": "2025-09-17", "is_recurring": True, "ticket_price": 50.0},
        {"name": "Izmir Avrupa Caz Festivali", "description": "European jazz acts and Turkish musicians perform free open-air concerts along Alsancak's seafront.", "start_date": "2025-05-01", "end_date": "2025-05-10", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Eskisehir": [
        {"name": "Uluslararasi Eskisehir Festivali", "description": "Multi-disciplinary arts and culture festival transforming canal streets into open-air stages and galleries.", "start_date": "2025-05-20", "end_date": "2025-05-25", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Trabzon": [
        {"name": "Trabzon Kultur Sanat Festivali", "description": "Black Sea culture festival with traditional Horon dance performances, folk music, and local crafts.", "start_date": "2025-08-10", "end_date": "2025-08-20", "is_recurring": True, "ticket_price": 0.0},
        {"name": "Uzungol Dag Festivali", "description": "Mountain festival at the scenic Uzungol lake with trekking competitions, folk music, and local food stalls.", "start_date": "2025-07-20", "end_date": "2025-07-22", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Cappadocia": [
        {"name": "Kapadokya Balon Festivali", "description": "International hot-air balloon festival filling the sky above fairy chimneys with hundreds of colourful balloons.", "start_date": "2025-07-14", "end_date": "2025-07-20", "is_recurring": True, "ticket_price": 0.0},
        {"name": "Nevsehir Muzik Festivali", "description": "Classical and folk music concerts in cave venues carved from volcanic rock across the Goreme valley.", "start_date": "2025-09-05", "end_date": "2025-09-10", "is_recurring": True, "ticket_price": 150.0},
    ],
    "Sanliurfa": [
        {"name": "Uluslararasi Sanliurfa Kultur Sanat Festivali", "description": "Festival celebrating the mystical city's rich multicultural heritage with whirling dervishes, concerts, and bazaars.", "start_date": "2025-09-20", "end_date": "2025-09-25", "is_recurring": True, "ticket_price": 0.0},
        {"name": "Gobeklitepe Kultur Yolu Festivali", "description": "Cultural trail festival linking Gobeklitepe and Balikligol with guided tours, talks, and traditional performances.", "start_date": "2025-05-15", "end_date": "2025-05-20", "is_recurring": True, "ticket_price": 50.0},
    ],
    "Gaziantep": [
        {"name": "Gastronomi Festivali", "description": "Massive food festival showcasing Gaziantep's UNESCO-recognised culinary heritage — baklava, kebab, and mezze masters.", "start_date": "2025-10-01", "end_date": "2025-10-05", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Van": [
        {"name": "Van Golu Festivali", "description": "Lake festival with boat races, traditional Van breakfast competitions, and Akdamar Island concerts.", "start_date": "2025-08-15", "end_date": "2025-08-20", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Bursa": [
        {"name": "Bursa Ipek Yolu Festivali", "description": "Silk Road festival honouring Bursa's Ottoman silk heritage with textile exhibitions, caravans, and concerts.", "start_date": "2025-06-01", "end_date": "2025-06-07", "is_recurring": True, "ticket_price": 50.0},
    ],
    "Konya": [
        {"name": "Seb-i Arus (Mevlana Anma)", "description": "Annual commemoration of Rumi's death with sema ceremonies, music, and spiritual gatherings drawing visitors worldwide.", "start_date": "2025-12-07", "end_date": "2025-12-17", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Canakkale": [
        {"name": "Canakkale Zaferi Etkinlikleri", "description": "Commemoration of the Gallipoli victory with ceremonies, exhibitions, and international delegations at ANZAC Cove.", "start_date": "2025-04-24", "end_date": "2025-04-25", "is_recurring": True, "ticket_price": 0.0},
        {"name": "Troya Festivali", "description": "Heritage festival at the ancient site of Troy featuring theatrical performances of the Iliad and archaeological tours.", "start_date": "2025-08-01", "end_date": "2025-08-07", "is_recurring": True, "ticket_price": 100.0},
    ],
    "Safranbolu": [
        {"name": "Safranbolu Kultur Festivali", "description": "Ottoman heritage festival with traditional crafts, period costumes, and mansion tours through cobbled historic streets.", "start_date": "2025-09-15", "end_date": "2025-09-18", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Bodrum": [
        {"name": "Bodrum Baski Muzik Festivali", "description": "Beach music festival on the shores of the Aegean with international DJs and live acts under the stars.", "start_date": "2025-08-01", "end_date": "2025-08-10", "is_recurring": True, "ticket_price": 500.0},
    ],
    "Mardin": [
        {"name": "Mardin Kirik Bahar Festivali", "description": "Spring festival celebrating Mardin's multicultural Syriac, Kurdish, and Arab heritage with open-air concerts.", "start_date": "2025-04-20", "end_date": "2025-04-23", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Alanya": [
        {"name": "Alanya Uluslararasi Kultur ve Sanat Festivali", "description": "International arts festival with exhibitions, concerts, and theatrical performances around the Alanya citadel.", "start_date": "2025-09-20", "end_date": "2025-09-28", "is_recurring": True, "ticket_price": 0.0},
    ],
    "Afyonkarahisar": [
        {"name": "Afyon Haşhaş Festivali", "description": "Unique poppy festival celebrating the blooming of Afyon's famous opium poppy fields with cultural events.", "start_date": "2025-06-01", "end_date": "2025-06-05", "is_recurring": True, "ticket_price": 0.0},
    ],
}

# ── Users ─────────────────────────────────────────────────────────────────────

_USERS: list[dict] = [
    {"name": "Ayse Yilmaz",   "email": "ayse@example.com"},
    {"name": "Mehmet Demir",  "email": "mehmet@example.com"},
    {"name": "Zeynep Kaya",   "email": "zeynep@example.com"},
    {"name": "Can Celik",     "email": "can@example.com"},
    {"name": "Buse Sahin",    "email": "buse@example.com"},
]

# ── Transport ─────────────────────────────────────────────────────────────────

_TRANSPORTS: list[dict] = [
    {"dep": "Istanbul",   "arr": "Ankara",     "type": "flight", "provider": "Turkish Airlines",  "dur": 1.5, "price": 800.0},
    {"dep": "Istanbul",   "arr": "Izmir",      "type": "flight", "provider": "Pegasus Airlines",  "dur": 1.2, "price": 700.0},
    {"dep": "Istanbul",   "arr": "Antalya",    "type": "flight", "provider": "SunExpress",        "dur": 1.5, "price": 900.0},
    {"dep": "Istanbul",   "arr": "Trabzon",    "type": "flight", "provider": "Turkish Airlines",  "dur": 1.8, "price": 1000.0},
    {"dep": "Istanbul",   "arr": "Cappadocia", "type": "flight", "provider": "Pegasus Airlines",  "dur": 1.4, "price": 950.0},
    {"dep": "Istanbul",   "arr": "Mardin",     "type": "flight", "provider": "AnadoluJet",        "dur": 2.2, "price": 1100.0},
    {"dep": "Istanbul",   "arr": "Van",        "type": "flight", "provider": "Turkish Airlines",  "dur": 2.5, "price": 1400.0},
    {"dep": "Ankara",     "arr": "Izmir",      "type": "flight", "provider": "AnadoluJet",        "dur": 1.3, "price": 750.0},
    {"dep": "Ankara",     "arr": "Cappadocia", "type": "bus",    "provider": "Metro Turizm",      "dur": 3.5, "price": 300.0},
    {"dep": "Ankara",     "arr": "Sanliurfa",  "type": "flight", "provider": "Turkish Airlines",  "dur": 1.8, "price": 1000.0},
    {"dep": "Izmir",      "arr": "Bodrum",     "type": "bus",    "provider": "Kamil Koc",         "dur": 3.5, "price": 250.0},
    {"dep": "Izmir",      "arr": "Antalya",    "type": "flight", "provider": "Pegasus Airlines",  "dur": 1.2, "price": 600.0},
    {"dep": "Izmir",      "arr": "Pamukkale",  "type": "bus",    "provider": "Pamukkale Turizm",  "dur": 4.0, "price": 200.0},
    {"dep": "Antalya",    "arr": "Alanya",     "type": "bus",    "provider": "Antalya Belko",     "dur": 2.5, "price": 150.0},
    {"dep": "Antalya",    "arr": "Konya",      "type": "bus",    "provider": "Metro Turizm",      "dur": 4.5, "price": 280.0},
    {"dep": "Cappadocia", "arr": "Kayseri",    "type": "bus",    "provider": "Goreme Seyahat",    "dur": 1.0, "price": 100.0},
    {"dep": "Istanbul",   "arr": "Edirne",     "type": "bus",    "provider": "Ulusoy",            "dur": 2.5, "price": 200.0},
    {"dep": "Istanbul",   "arr": "Canakkale",  "type": "bus",    "provider": "Truva Turizm",      "dur": 5.0, "price": 350.0},
    {"dep": "Bursa",      "arr": "Istanbul",   "type": "ferry",  "provider": "IDO",               "dur": 2.0, "price": 180.0},
    {"dep": "Diyarbakir", "arr": "Mardin",     "type": "bus",    "provider": "Diyarbakir Ekspres", "dur": 1.5, "price": 80.0},
]

# ── Visited edges ─────────────────────────────────────────────────────────────

_VISITED: dict[str, list[str]] = {
    "ayse@example.com":   ["Istanbul", "Izmir", "Antalya", "Bodrum"],
    "mehmet@example.com": ["Cappadocia", "Ankara", "Gaziantep", "Konya", "Sanliurfa"],
    "zeynep@example.com": ["Trabzon", "Van", "Erzurum", "Mardin", "Diyarbakir"],
    "can@example.com":    ["Istanbul", "Eskisehir", "Bursa", "Safranbolu", "Canakkale"],
    "buse@example.com":   ["Alanya", "Antalya", "Pamukkale", "Bodrum", "Izmir"],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _run(db: Any, cypher: str, params: dict | None = None) -> Any:
    return db.query(cypher, params or {})


# ── Step functions ────────────────────────────────────────────────────────────

def _clean(db: Any) -> None:
    _run(db, "MATCH (n) DETACH DELETE n")
    print("✓ Veritabani temizlendi")


def _create_categories(db: Any) -> None:
    for cat in _CATEGORIES:
        _run(db, "CREATE (:Category {id: $id, name: $name, icon: $icon})", cat)
    print(f"✓ {len(_CATEGORIES)} Category olusturuldu")


def _create_seasons(db: Any) -> None:
    for s in _SEASONS:
        _run(db, "CREATE (:Season {id: $id, name: $name, months: $months, avg_temp_c: $avg_temp_c, weather_description: $weather_description})", s)
    print(f"✓ {len(_SEASONS)} Season olusturuldu")


def _create_tags(db: Any) -> None:
    for tag in _TAGS:
        _run(db, "CREATE (:Tag {id: $id, name: $name, color: $color})", tag)
    print(f"✓ {len(_TAGS)} Tag olusturuldu")


def _create_destinations(db: Any) -> dict[str, str]:
    dest_ids: dict[str, str] = {}
    for dest in _DESTINATIONS:
        dest_id = str(uuid4())
        dest_ids[dest["name"]] = dest_id
        _run(
            db,
            "CREATE (:Destination {id: $id, name: $name, country: $country, description: $description, lat: $lat, lng: $lng, created_at: $ca})",
            {"id": dest_id, "name": dest["name"], "country": dest["country"], "description": dest["description"], "lat": dest["lat"], "lng": dest["lng"], "ca": _now()},
        )
        for season_name in dest["best_seasons"]:
            _run(db, "MATCH (d:Destination {id: $did}), (s:Season {name: $sn}) CREATE (d)-[:BEST_IN]->(s)", {"did": dest_id, "sn": season_name})
    print(f"✓ {len(_DESTINATIONS)} Destination olusturuldu")
    return dest_ids


def _create_activities(db: Any, dest_ids: dict[str, str]) -> dict[str, str]:
    act_ids: dict[str, str] = {}
    total = 0
    for dest_name, activities in _ACTIVITIES.items():
        if dest_name not in dest_ids:
            continue
        dest_id = dest_ids[dest_name]
        for act in activities:
            act_id = str(uuid4())
            act_ids[act["name"]] = act_id
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (a:Activity {id: $id, name: $name, description: $description, duration_hours: $dh, price: $price, address: $address, destination_id: $dest_id, categories: [], tags: [], created_at: $ca}) "
                "CREATE (d)-[:HAS_ACTIVITY]->(a) "
                "CREATE (a)-[:LOCATED_IN]->(d)",
                {"dest_id": dest_id, "id": act_id, "name": act["name"], "description": act["description"], "dh": act["duration_hours"], "price": act["price"], "address": act["address"], "ca": _now()},
            )
            for cat_name in act["categories"]:
                _run(db, "MATCH (a:Activity {id: $aid}), (c:Category {name: $cn}) CREATE (a)-[:IN_CATEGORY]->(c)", {"aid": act_id, "cn": cat_name})
            for tag_name in act["tags"]:
                _run(db, "MATCH (a:Activity {id: $aid}), (t:Tag {name: $tn}) CREATE (a)-[:HAS_TAG]->(t)", {"aid": act_id, "tn": tag_name})
            total += 1
    print(f"✓ {total} Activity olusturuldu")
    return act_ids


def _create_restaurants(db: Any, dest_ids: dict[str, str]) -> None:
    total = 0
    for dest_name, restaurants in _RESTAURANTS.items():
        if dest_name not in dest_ids:
            continue
        dest_id = dest_ids[dest_name]
        for rest in restaurants:
            rest_id = str(uuid4())
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (r:Restaurant {id: $id, name: $name, cuisine_type: $cuisine_type, price_range: $price_range, address: $address, rating: $rating, destination_id: $dest_id, created_at: $ca}) "
                "CREATE (d)-[:HAS_RESTAURANT]->(r)",
                {"dest_id": dest_id, "id": rest_id, "name": rest["name"], "cuisine_type": rest["cuisine_type"], "price_range": rest["price_range"], "address": rest["address"], "rating": rest.get("rating"), "ca": _now()},
            )
            total += 1
    print(f"✓ {total} Restaurant olusturuldu")


def _create_accommodations(db: Any, dest_ids: dict[str, str]) -> dict[str, str]:
    acc_ids: dict[str, str] = {}
    total = 0
    for dest_name, accommodations in _ACCOMMODATIONS.items():
        if dest_name not in dest_ids:
            continue
        dest_id = dest_ids[dest_name]
        for acc in accommodations:
            acc_id = str(uuid4())
            acc_ids[acc["name"]] = acc_id
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (a:Accommodation {id: $id, name: $name, type: $type, star_rating: $sr, price_per_night: $ppn, address: $address, destination_id: $dest_id, created_at: $ca}) "
                "CREATE (d)-[:HAS_ACCOMMODATION]->(a) "
                "CREATE (a)-[:LOCATED_IN]->(d)",
                {"dest_id": dest_id, "id": acc_id, "name": acc["name"], "type": acc["type"], "sr": acc["star_rating"], "ppn": acc["price_per_night"], "address": acc["address"], "ca": _now()},
            )
            total += 1
    print(f"✓ {total} Accommodation olusturuldu")
    return acc_ids


def _create_festivals(db: Any, dest_ids: dict[str, str]) -> None:
    total = 0
    for dest_name, fest_list in _FESTIVALS.items():
        if dest_name not in dest_ids:
            continue
        dest_id = dest_ids[dest_name]
        fests = fest_list if isinstance(fest_list, list) else [fest_list]
        for fest in fests:
            fest_id = str(uuid4())
            _run(
                db,
                "MATCH (d:Destination {id: $dest_id}) "
                "CREATE (f:Festival {id: $id, name: $name, description: $description, start_date: $sd, end_date: $ed, is_recurring: $ir, ticket_price: $tp, destination_id: $dest_id, created_at: $ca}) "
                "CREATE (d)-[:HAS_FESTIVAL]->(f)",
                {"dest_id": dest_id, "id": fest_id, "name": fest["name"], "description": fest["description"], "sd": fest["start_date"], "ed": fest["end_date"], "ir": fest["is_recurring"], "tp": fest.get("ticket_price"), "ca": _now()},
            )
            total += 1
    print(f"✓ {total} Festival olusturuldu")


def _create_users(db: Any) -> dict[str, str]:
    user_ids: dict[str, str] = {}
    pw_hash = hash_password("Test1234!")
    for user in _USERS:
        user_id = str(uuid4())
        user_ids[user["email"]] = user_id
        _run(
            db,
            "CREATE (:User {id: $id, name: $name, email: $email, password_hash: $ph, created_at: $ca})",
            {"id": user_id, "name": user["name"], "email": user["email"], "ph": pw_hash, "ca": _now()},
        )
    print(f"✓ {len(_USERS)} User olusturuldu (sifre: Test1234!)")
    return user_ids


def _create_visited_edges(db: Any, user_ids: dict[str, str], dest_ids: dict[str, str]) -> None:
    total = 0
    for email, dest_names in _VISITED.items():
        user_id = user_ids[email]
        for dest_name in dest_names:
            if dest_name not in dest_ids:
                continue
            _run(db, "MATCH (u:User {id: $uid}), (d:Destination {id: $did}) CREATE (u)-[:VISITED {visited_at: $va}]->(d)", {"uid": user_id, "did": dest_ids[dest_name], "va": _now()})
            total += 1
    print(f"✓ {total} VISITED kenari olusturuldu")


def _create_reviews(db: Any, user_ids: dict[str, str], act_ids: dict[str, str], acc_ids: dict[str, str]) -> None:
    reviews = [
        {"user": "ayse@example.com",   "target_name": "Bogaz Turu",            "target_type": "activity",      "rating": 5, "comment": "Aksam gunesinde Bogazda yuzmeyi izlemek tarifsiz guzeldi."},
        {"user": "ayse@example.com",   "target_name": "Ayasofya",              "target_type": "activity",      "rating": 5, "comment": "Binlerce yillik tarihin icinde durmak insani kupucuk hissettiriyor."},
        {"user": "mehmet@example.com", "target_name": "Sicak Hava Balonu Turu","target_type": "activity",      "rating": 5, "comment": "Hayatimin en iyi deneyimi. Peri bacalari uzerinden gunes dogusunu seyrettik."},
        {"user": "mehmet@example.com", "target_name": "Gobeklitepe",           "target_type": "activity",      "rating": 5, "comment": "12.000 yillik tarihin uzerinde durmak akil almaz. Mutlaka gorun."},
        {"user": "zeynep@example.com", "target_name": "Sumela Manastiri",      "target_type": "activity",      "rating": 5, "comment": "Virajli dag yolunun ardinda karsilasacaginiz manzara nefes kesici."},
        {"user": "zeynep@example.com", "target_name": "Akdamar Kilisesi",      "target_type": "activity",      "rating": 4, "comment": "Van Golunde tekneyle adaya ulasmak basli basina bir deneyim."},
        {"user": "can@example.com",    "target_name": "Safranbolu Tarihi Evleri Turu", "target_type": "activity", "rating": 5, "comment": "Sanki zamanda geriye gittim. Her kose bir fotograf."},
        {"user": "can@example.com",    "target_name": "Porsuk Cayi Tekne Turu","target_type": "activity",      "rating": 4, "comment": "Romantik ve rahatlatici. Kanallar boyunca kahve icmek harikaydı."},
        {"user": "buse@example.com",   "target_name": "Kleopatra Plaji",       "target_type": "activity",      "rating": 5, "comment": "Turkiyenin en guzel plajlarindan biri. Suyu kristal berrakligi."},
        {"user": "buse@example.com",   "target_name": "Pamukkale Travertenleri","target_type": "activity",     "rating": 5, "comment": "Fotograflarda gordugunuzden cok daha guzel. Beyaz termallar masalsi."},
        {"user": "ayse@example.com",   "target_name": "Four Seasons Sultanahmet", "target_type": "accommodation", "rating": 5, "comment": "Harika konum ve servis. Pencereden Ayasofya goruntuleniyor."},
        {"user": "mehmet@example.com", "target_name": "Kelebek Cave Hotel",    "target_type": "accommodation", "rating": 5, "comment": "Kapadokya macera baslamasın demek lazim, kaya odalarda uyumak cok efsane."},
        {"user": "zeynep@example.com", "target_name": "Erdoba Elegance Hotel", "target_type": "accommodation", "rating": 5, "comment": "Mardin manzarali tarih icinde konaklama. Muhtesem."},
        {"user": "can@example.com",    "target_name": "Cinci Han Boutique",    "target_type": "accommodation", "rating": 4, "comment": "Tarihi hanin icinde kalmak cok keyifliydi. Sabah kaymagi ve bal muhtesem."},
        {"user": "buse@example.com",   "target_name": "Alanya Boutique Hotel", "target_type": "accommodation", "rating": 4, "comment": "Kaleye yakin, temiz, hos bir butik otel. Personel cok ilgiliydi."},
    ]
    all_ids = {**act_ids, **acc_ids}
    total = 0
    for rev in reviews:
        if rev["target_name"] not in all_ids:
            continue
        review_id = str(uuid4())
        user_id = user_ids[rev["user"]]
        target_id = all_ids[rev["target_name"]]
        _run(
            db,
            "MATCH (u:User {id: $uid}) "
            "CREATE (r:Review {id: $id, target_id: $tid, target_type: $tt, rating: $rating, comment: $comment, created_at: $ca}) "
            "CREATE (u)-[:WROTE]->(r)",
            {"uid": user_id, "id": review_id, "tid": target_id, "tt": rev["target_type"], "rating": rev["rating"], "comment": rev["comment"], "ca": _now()},
        )
        total += 1
    print(f"✓ {total} Review olusturuldu")


def _create_transports(db: Any, dest_ids: dict[str, str]) -> None:
    total = 0
    for route in _TRANSPORTS:
        if route["dep"] not in dest_ids or route["arr"] not in dest_ids:
            print(f"  ! '{route['dep']}' veya '{route['arr']}' bulunamadi — atlandi")
            continue
        tid = str(uuid4())
        _run(db, "CREATE (:Transport {id: $id, type: $type, provider: $provider, duration_hours: $dur, price: $price, departure_city: $dep, arrival_city: $arr})", {"id": tid, "type": route["type"], "provider": route["provider"], "dur": route["dur"], "price": route["price"], "dep": route["dep"], "arr": route["arr"]})
        _run(db, "MATCH (a:Destination {name: $dep}), (b:Destination {name: $arr}), (t:Transport {id: $tid}) CREATE (a)-[:CONNECTED_BY]->(t)-[:CONNECTED_BY]->(b)", {"dep": route["dep"], "arr": route["arr"], "tid": tid})
        _run(db, "MATCH (a:Destination {name: $dep}), (b:Destination {name: $arr}), (t:Transport {id: $tid}) CREATE (b)-[:CONNECTED_BY]->(t)-[:CONNECTED_BY]->(a)", {"dep": route["dep"], "arr": route["arr"], "tid": tid})
        total += 1
    print(f"✓ {total} Transport olusturuldu")


# ── Entry point ───────────────────────────────────────────────────────────────

def seed() -> None:
    print("FalkorDB'ye baglaniliyor...")
    db = _connect_with_retry()
    print("✓ Baglanti kuruldu\n")

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
    _create_transports(db, dest_ids)

    print("\n✓ Seed tamamlandi.")
    print(f"  {len(_DESTINATIONS)} sehir, {sum(len(v) for v in _ACTIVITIES.values())} aktivite,")
    print(f"  {sum(len(v) for v in _FESTIVALS.values())} festival,")
    print(f"  {len(_USERS)} kullanici (sifre: Test1234!)")


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:
        print(f"\n✗ Seed basarisiz: {exc}", file=sys.stderr)
        sys.exit(1)
