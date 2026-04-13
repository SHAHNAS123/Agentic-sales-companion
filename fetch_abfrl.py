"""
ABFRL Product Scraper – fetch_abfrl.py
Optional helper: crawls ABFRL/brand pages and saves a products.json.
Only required if you use the /admin/bootstrap endpoint.

Usage:
    from fetch_abfrl import bootstrap
    bootstrap(["https://www.louisphilippe.com/men/shirts"], out_path="data/products.json")
"""

import json
import os
import time
import re
from typing import List, Tuple
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
    from tqdm import tqdm
    _DEPS_OK = True
except ImportError:
    _DEPS_OK = False


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _extract_products_from_page(url: str, session: "requests.Session", brand_code: str = "LP") -> List[dict]:
    """Attempt to scrape product cards from a listing page."""
    if not _DEPS_OK:
        raise RuntimeError("Install requests, beautifulsoup4, lxml, tqdm to use the scraper.")

    products = []
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        # Generic product card selectors — adjust per site structure
        cards = (
            soup.select(".product-card")
            or soup.select(".product-item")
            or soup.select("[data-product-id]")
            or soup.select(".plp-card")
            or []
        )

        for card in cards:
            try:
                name_el  = card.select_one(".product-name, .product-title, h3, h2")
                price_el = card.select_one(".price, .product-price, [data-price]")
                img_el   = card.select_one("img")
                link_el  = card.select_one("a[href]")

                name  = name_el.get_text(strip=True)  if name_el  else "Unknown Product"
                price_text = price_el.get_text(strip=True) if price_el else "0"
                price_val  = float(re.sub(r"[^\d.]", "", price_text) or "0")
                image_url  = img_el.get("src") or img_el.get("data-src") or "" if img_el else ""
                product_url = urljoin(url, link_el["href"]) if link_el else url

                sku = f"{brand_code}-SCRAPED-{_slugify(name)[:20].upper()}"

                products.append({
                    "sku": sku,
                    "name": name,
                    "brand_code": brand_code,
                    "category": "Uncategorised",
                    "gender": "Unisex",
                    "price": price_val,
                    "sale_price": None,
                    "image_url": image_url,
                    "product_url": product_url,
                    "tags": [],
                    "scraped": True,
                })
            except Exception:
                continue
    except Exception as e:
        print(f"[scraper] Error fetching {url}: {e}")

    return products


def bootstrap(
    seeds: List[str],
    out_path: str = "data/products.json",
    limit: int = 100,
    delay: float = 1.0,
) -> Tuple[int, str]:
    """
    Crawl seed URLs, collect products, and save to out_path.
    Returns (count_found, saved_path).
    """
    if not _DEPS_OK:
        raise RuntimeError("Install requests, beautifulsoup4, lxml, tqdm first.")

    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; ABFRL-demo-scraper/1.0)"})

    all_products: dict = {}

    for seed_url in tqdm(seeds, desc="Crawling seeds"):
        parsed = urlparse(seed_url)
        # Guess brand from domain
        domain = parsed.netloc.lower()
        brand_code = "LP"
        if "vanheusen" in domain or "vh" in domain:   brand_code = "VH"
        elif "allensolly" in domain:                   brand_code = "AS"
        elif "peterengland" in domain:                 brand_code = "PE"
        elif "pantaloons" in domain:                   brand_code = "PL"

        products = _extract_products_from_page(seed_url, session, brand_code)
        for p in products:
            if len(all_products) >= limit:
                break
            all_products[p["sku"]] = p

        if len(all_products) >= limit:
            break

        time.sleep(delay)

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(all_products, fh, ensure_ascii=False, indent=2)

    print(f"[scraper] Saved {len(all_products)} products → {out_path}")
    return len(all_products), out_path
