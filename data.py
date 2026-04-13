"""
ABFRL Customer Profiles and Product Catalog
Synthetic data for Aditya Birla Fashion and Retail Limited demo.
"""

from typing import List
import os
import json

# ---- Customers -----------------------------------------------------
CUSTOMERS = {
    "ABFRL-C001": {
        "id": "ABFRL-C001",
        "name": "Rajesh Sharma",
        "email": "rajesh.sharma@gmail.com",
        "phone": "+91-98765-43210",
        "demographics": {
            "age": 35, "gender": "Male",
            "location": {"city": "Mumbai", "state": "Maharashtra", "pincode": "400001"},
            "income_bracket": "15L-25L", "occupation": "IT Manager",
        },
        "loyalty_tier": "Gold",
        "loyalty_points": 4500,
        "member_since": "2021-06-15",
        "device_preferences": ["mobile_app", "web"],
        "preferred_channel": "online",
        "preferred_brands": ["Louis Philippe", "Van Heusen"],
        "size_profile": {"shirt": "42", "trouser": "34", "shoe": "9"},
        "purchase_history": [
            {"order_id": "ABFRL-2024-001", "date": "2024-01-15", "items": ["LP-SHIRT-001", "LP-TROUSER-002"], "total": 5999.00, "status": "delivered", "brand": "Louis Philippe"},
            {"order_id": "ABFRL-2024-045", "date": "2024-03-22", "items": ["VH-BLAZER-003"],                  "total": 8999.00, "status": "delivered", "brand": "Van Heusen"},
            {"order_id": "ABFRL-2024-112", "date": "2024-06-10", "items": ["LP-POLO-005", "LP-CHINO-002"],    "total": 4499.00, "status": "delivered", "brand": "Louis Philippe"},
        ],
        "browsing_history": ["formal shirts", "blazers", "leather belts", "formal shoes"],
        "saved_payment_methods": [
            {"type": "card", "last4": "4242", "brand": "HDFC Visa"},
            {"type": "upi",  "id":    "rajesh@okicici"},
        ],
        "addresses": [
            {"type": "home", "address": "A-42, Hiranandani Gardens, Powai", "city": "Mumbai", "state": "Maharashtra", "pincode": "400076"},
            {"type": "work", "address": "WeWork, BKC",                      "city": "Mumbai", "state": "Maharashtra", "pincode": "400051"},
        ],
    },
    "ABFRL-C002": {
        "id": "ABFRL-C002",
        "name": "Priya Menon",
        "email": "priya.menon@outlook.com",
        "phone": "+91-87654-32109",
        "demographics": {
            "age": 28, "gender": "Female",
            "location": {"city": "Bangalore", "state": "Karnataka", "pincode": "560001"},
            "income_bracket": "10L-15L", "occupation": "Product Manager",
        },
        "loyalty_tier": "Platinum",
        "loyalty_points": 12800,
        "member_since": "2019-08-20",
        "device_preferences": ["mobile_app"],
        "preferred_channel": "online",
        "preferred_brands": ["Allen Solly", "Pantaloons"],
        "size_profile": {"top": "M", "bottom": "30", "shoe": "6"},
        "purchase_history": [
            {"order_id": "ABFRL-2024-023", "date": "2024-02-08", "items": ["AS-DRESS-002", "AS-TOP-015"],   "total": 3999.00, "status": "delivered", "brand": "Allen Solly"},
            {"order_id": "ABFRL-2024-078", "date": "2024-04-15", "items": ["PL-KURTI-001", "PL-PALAZZO-003"],"total": 2499.00, "status": "delivered", "brand": "Pantaloons"},
            {"order_id": "ABFRL-2024-156", "date": "2024-08-30", "items": ["AS-BLAZER-001", "AS-TROUSER-008"],"total": 6999.00,"status": "delivered", "brand": "Allen Solly"},
        ],
        "browsing_history": ["work dresses", "kurtis", "palazzos", "handbags", "formal tops"],
        "saved_payment_methods": [
            {"type": "card", "last4": "1234", "brand": "ICICI Mastercard"},
            {"type": "upi",  "id":    "priya@ybl"},
        ],
        "addresses": [
            {"type": "home", "address": "Flat 302, Prestige Shantiniketan", "city": "Bangalore", "state": "Karnataka", "pincode": "560048"},
        ],
    },
    "ABFRL-C003": {
        "id": "ABFRL-C003",
        "name": "Amit Patel",
        "email": "amit.patel@gmail.com",
        "phone": "+91-99887-76655",
        "demographics": {
            "age": 42, "gender": "Male",
            "location": {"city": "Ahmedabad", "state": "Gujarat", "pincode": "380001"},
            "income_bracket": "25L+", "occupation": "Business Owner",
        },
        "loyalty_tier": "Platinum",
        "loyalty_points": 18500,
        "member_since": "2018-11-10",
        "device_preferences": ["web", "in_store"],
        "preferred_channel": "omnichannel",
        "preferred_brands": ["Louis Philippe", "Van Heusen"],
        "size_profile": {"shirt": "44", "trouser": "36", "shoe": "10"},
        "purchase_history": [
            {"order_id": "ABFRL-2024-034", "date": "2024-02-20", "items": ["LP-SUIT-001", "LP-SHIRT-010", "VH-TIE-005"], "total": 24999.00, "status": "delivered", "brand": "Louis Philippe"},
            {"order_id": "ABFRL-2024-089", "date": "2024-05-05", "items": ["VH-JACKET-002", "VH-TROUSER-004"],            "total": 12999.00, "status": "delivered", "brand": "Van Heusen"},
            {"order_id": "ABFRL-2024-167", "date": "2024-09-12", "items": ["LP-COAT-001"],                                "total": 18999.00, "status": "processing", "brand": "Louis Philippe"},
        ],
        "browsing_history": ["suits", "premium blazers", "wedding collection", "formal accessories"],
        "saved_payment_methods": [
            {"type": "card", "last4": "5678", "brand": "Amex Platinum"},
        ],
        "addresses": [
            {"type": "home", "address": "Bungalow 15, Satellite Road",  "city": "Ahmedabad", "state": "Gujarat", "pincode": "380015"},
            {"type": "work", "address": "Patel Industries, GIDC Vatva", "city": "Ahmedabad", "state": "Gujarat", "pincode": "382445"},
        ],
    },
}

# ---- Brands --------------------------------------------------------
BRANDS = {
    "LP": {"id": "LP", "name": "Louis Philippe", "segment": "Premium",       "tagline": "The Upper Crest"},
    "VH": {"id": "VH", "name": "Van Heusen",     "segment": "Premium",       "tagline": "Power Dressing"},
    "AS": {"id": "AS", "name": "Allen Solly",     "segment": "Mid-Premium",   "tagline": "My World. My Way."},
    "PE": {"id": "PE", "name": "Peter England",   "segment": "Value",         "tagline": "Honestly Impressive"},
    "PL": {"id": "PL", "name": "Pantaloons",      "segment": "Value Fashion", "tagline": "Fresh Fashion"},
}

# ---- Products: load from scraped JSON if present, else built-in ----
_products_path = os.path.join(os.path.dirname(__file__), "data", "products.json")

if os.path.exists(_products_path):
    try:
        with open(_products_path, "r", encoding="utf-8") as fh:
            PRODUCTS = json.load(fh)
        print(f"[data] Loaded {len(PRODUCTS)} products from {_products_path}")
    except Exception as e:
        print(f"[data] Failed to load products.json ({e}), using built-in sample.")
        PRODUCTS = {}
else:
    PRODUCTS = {
        "LP-SHIRT-001": {
            "sku": "LP-SHIRT-001", "name": "Premium Cotton Formal Shirt – White",
            "brand": "Louis Philippe", "brand_code": "LP",
            "category": "Shirts", "subcategory": "Formal Shirts", "gender": "Men",
            "price": 2999.00, "sale_price": None,
            "attributes": {"fabric": "100% Premium Cotton", "fit": "Slim Fit", "collar": "Cutaway", "sleeve": "Full Sleeve", "pattern": "Solid", "color": "White", "occasion": "Formal/Office", "care": "Machine Wash"},
            "sizes": ["38", "40", "42", "44", "46"],
            "description": "Classic white formal shirt crafted from premium cotton with superior finish",
            "image_url": "/images/lp/shirt-001.jpg", "rating": 4.6, "reviews_count": 342,
            "tags": ["formal", "office wear", "premium", "classic"],
        },
        "LP-TROUSER-002": {
            "sku": "LP-TROUSER-002", "name": "Wool Blend Formal Trouser – Charcoal",
            "brand": "Louis Philippe", "brand_code": "LP",
            "category": "Trousers", "subcategory": "Formal Trousers", "gender": "Men",
            "price": 3299.00, "sale_price": None,
            "attributes": {"fabric": "Wool Blend (70% Wool, 30% Polyester)", "fit": "Slim Fit", "type": "Flat Front", "color": "Charcoal Grey", "occasion": "Formal/Office", "care": "Dry Clean Only"},
            "sizes": ["30", "32", "34", "36", "38"],
            "description": "Premium wool blend trouser with impeccable tailoring",
            "image_url": "/images/lp/trouser-002.jpg", "rating": 4.7, "reviews_count": 234,
            "tags": ["formal", "wool", "office", "tailored"],
        },
        "LP-POLO-005": {
            "sku": "LP-POLO-005", "name": "Classic Polo T-Shirt – Navy",
            "brand": "Louis Philippe", "brand_code": "LP",
            "category": "T-Shirts", "subcategory": "Polo", "gender": "Men",
            "price": 1999.00, "sale_price": None,
            "attributes": {"fabric": "100% Cotton Pique", "fit": "Regular Fit", "collar": "Polo Collar", "sleeve": "Half Sleeve", "pattern": "Solid", "color": "Navy Blue", "occasion": "Smart Casual", "care": "Machine Wash"},
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "description": "Timeless polo t-shirt in classic navy with signature LP branding",
            "image_url": "/images/lp/polo-005.jpg", "rating": 4.5, "reviews_count": 456,
            "tags": ["polo", "casual", "weekend", "classic"],
        },
        "LP-CHINO-002": {
            "sku": "LP-CHINO-002", "name": "Stretch Cotton Chinos – Khaki",
            "brand": "Louis Philippe", "brand_code": "LP",
            "category": "Trousers", "subcategory": "Chinos", "gender": "Men",
            "price": 2499.00, "sale_price": None,
            "attributes": {"fabric": "98% Cotton, 2% Elastane", "fit": "Slim Fit", "type": "Flat Front", "color": "Khaki", "occasion": "Smart Casual", "care": "Machine Wash"},
            "sizes": ["30", "32", "34", "36"],
            "description": "Comfortable stretch chinos perfect for the modern gentleman",
            "image_url": "/images/lp/chino-002.jpg", "rating": 4.6, "reviews_count": 312,
            "tags": ["chinos", "casual", "stretch", "comfortable"],
        },
        "LP-SUIT-001": {
            "sku": "LP-SUIT-001", "name": "Premium Wool Suit – Navy",
            "brand": "Louis Philippe", "brand_code": "LP",
            "category": "Suits", "subcategory": "2-Piece Suits", "gender": "Men",
            "price": 19999.00, "sale_price": None,
            "attributes": {"fabric": "Super 120s Wool", "fit": "Slim Fit", "style": "Single Breasted, 2 Button", "color": "Navy Blue", "lining": "Full Canvas", "occasion": "Formal/Business/Wedding", "care": "Dry Clean Only"},
            "sizes": ["38", "40", "42", "44", "46"],
            "description": "Impeccably tailored suit in Super 120s wool for the distinguished gentleman",
            "image_url": "/images/lp/suit-001.jpg", "rating": 4.9, "reviews_count": 87,
            "tags": ["suit", "premium", "wedding", "formal", "wool"],
        },
        "LP-BLAZER-003": {
            "sku": "LP-BLAZER-003", "name": "Classic Blazer – Black",
            "brand": "Louis Philippe", "brand_code": "LP",
            "category": "Blazers", "subcategory": "Formal Blazers", "gender": "Men",
            "price": 9999.00, "sale_price": 8499.00,
            "attributes": {"fabric": "Wool Blend", "fit": "Regular Fit", "style": "Single Breasted, 2 Button", "color": "Black", "occasion": "Formal/Business", "care": "Dry Clean Only"},
            "sizes": ["38", "40", "42", "44"],
            "description": "Versatile black blazer for every formal occasion",
            "image_url": "/images/lp/blazer-003.jpg", "rating": 4.7, "reviews_count": 156,
            "tags": ["blazer", "formal", "classic", "versatile"],
        },
        "VH-SHIRT-001": {
            "sku": "VH-SHIRT-001", "name": "Tech Smart Formal Shirt – White",
            "brand": "Van Heusen", "brand_code": "VH",
            "category": "Shirts", "subcategory": "Formal Shirts", "gender": "Men",
            "price": 2299.00, "sale_price": None,
            "attributes": {"fabric": "Cotton Rich with Tech Finish", "fit": "Slim Fit", "collar": "Semi-Spread", "sleeve": "Full Sleeve", "pattern": "Solid", "color": "White", "features": ["Wrinkle Free", "Stain Resistant"], "occasion": "Formal/Office", "care": "Machine Wash"},
            "sizes": ["38", "40", "42", "44", "46"],
            "description": "Smart formal shirt with wrinkle-free and stain-resistant technology",
            "image_url": "/images/vh/shirt-001.jpg", "rating": 4.5, "reviews_count": 523,
            "tags": ["formal", "wrinkle-free", "tech", "office"],
        },
        "VH-BLAZER-003": {
            "sku": "VH-BLAZER-003", "name": "Power Suit Blazer – Grey",
            "brand": "Van Heusen", "brand_code": "VH",
            "category": "Blazers", "subcategory": "Business Blazers", "gender": "Men",
            "price": 8999.00, "sale_price": None,
            "attributes": {"fabric": "Poly Viscose", "fit": "Slim Fit", "style": "Single Breasted, 2 Button", "color": "Steel Grey", "features": ["Stretch", "Easy Care"], "occasion": "Business/Formal", "care": "Dry Clean"},
            "sizes": ["38", "40", "42", "44", "46"],
            "description": "Contemporary blazer designed for the power professional",
            "image_url": "/images/vh/blazer-003.jpg", "rating": 4.6, "reviews_count": 198,
            "tags": ["blazer", "business", "power dressing", "professional"],
        },
        "AS-DRESS-002": {
            "sku": "AS-DRESS-002", "name": "Fit & Flare Work Dress – Navy",
            "brand": "Allen Solly", "brand_code": "AS",
            "category": "Dresses", "subcategory": "Work Dresses", "gender": "Women",
            "price": 2999.00, "sale_price": None,
            "attributes": {"fabric": "Polyester Crepe", "fit": "Fit & Flare", "length": "Knee Length", "sleeve": "Short Sleeve", "neckline": "Round Neck", "color": "Navy Blue", "occasion": "Office/Work", "care": "Machine Wash"},
            "sizes": ["XS", "S", "M", "L", "XL"],
            "description": "Chic fit and flare dress perfect for the office",
            "image_url": "/images/as/dress-002.jpg", "rating": 4.5, "reviews_count": 312,
            "tags": ["dress", "work", "office", "elegant"],
        },
        "PL-KURTI-001": {
            "sku": "PL-KURTI-001", "name": "Printed Cotton Kurti – Multicolor",
            "brand": "Pantaloons", "brand_code": "PL",
            "category": "Kurtis", "subcategory": "Casual Kurtis", "gender": "Women",
            "price": 999.00, "sale_price": 799.00,
            "attributes": {"fabric": "100% Cotton", "fit": "Regular Fit", "length": "Knee Length", "sleeve": "3/4 Sleeve", "pattern": "Floral Print", "occasion": "Casual/Ethnic", "care": "Machine Wash"},
            "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
            "description": "Vibrant printed cotton kurti for everyday casual and ethnic wear",
            "image_url": "/images/pl/kurti-001.jpg", "rating": 4.3, "reviews_count": 678,
            "tags": ["ethnic", "kurti", "casual", "comfortable", "printed"],
        },
        "PE-SHIRT-001": {
            "sku": "PE-SHIRT-001", "name": "Classic Formal Shirt – Blue Checks",
            "brand": "Peter England", "brand_code": "PE",
            "category": "Shirts", "subcategory": "Formal Shirts", "gender": "Men",
            "price": 1299.00, "sale_price": None,
            "attributes": {"fabric": "Cotton Blend", "fit": "Regular Fit", "collar": "Spread", "sleeve": "Full Sleeve", "pattern": "Checks", "color": "Blue/White", "occasion": "Formal/Office", "care": "Machine Wash"},
            "sizes": ["38", "40", "42", "44", "46"],
            "description": "Smart check shirt ideal for office and semi-formal occasions",
            "image_url": "/images/pe/shirt-001.jpg", "rating": 4.4, "reviews_count": 891,
            "tags": ["formal", "checks", "office", "value"],
        },
    }


# ---- Helpers -------------------------------------------------------
def get_customer(customer_id: str):
    return CUSTOMERS.get(customer_id)


def get_product(sku: str):
    return PRODUCTS.get(sku)


def search_products(query: str, gender: str = None, brand: str = None, max_results: int = 10):
    """Search products by name, description, category, or tags."""
    query_lower = query.lower()
    results = []
    for product in PRODUCTS.values():
        if gender and product.get("gender", "").lower() != gender.lower():
            continue
        if brand and product.get("brand_code", "").lower() != brand.lower():
            continue
        score = 0
        if query_lower in product["name"].lower():        score += 10
        if query_lower in product.get("description", "").lower(): score += 5
        if query_lower in product.get("category", "").lower():    score += 4
        if any(query_lower in tag for tag in product.get("tags", [])): score += 3
        if score > 0:
            results.append((score, product))
    results.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in results[:max_results]]


def refresh_products_from_site(seeds: List[str], out_path: str = None, limit: int = 100, delay: float = 1.0):
    """Dev helper: crawl ABFRL and save products.json."""
    try:
        from fetch_abfrl import bootstrap
    except Exception as e:
        raise RuntimeError("Scraper dependencies not available. Install requirements first.") from e

    out_path = out_path or os.path.join(os.path.dirname(__file__), "data", "products.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    count, saved = bootstrap(seeds, out_path=out_path, limit=limit, delay=delay)

    try:
        with open(saved, "r", encoding="utf-8") as fh:
            global PRODUCTS
            PRODUCTS = json.load(fh)
    except Exception as e:
        raise RuntimeError("Failed to reload scraped products JSON") from e

    return count, saved
