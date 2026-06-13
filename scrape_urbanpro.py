"""
UrbanPro Profile Scraper for Shilpa Deol
=========================================
Run this script once a month to update your data.json with
fresh ratings, review counts, and reviews from UrbanPro.

Usage:
    python scrape_urbanpro.py

Requirements:
    pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

# ── Your UrbanPro profile URL ──────────────────────────────────────────────
PROFILE_URL  = "https://www.urbanpro.com/delhi/shilpa-c"
REVIEWS_URL  = "https://www.urbanpro.com/kharar/french-language-classes"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

DATA_FILE = "data.json"


def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  ⚠ Could not fetch {url}: {e}")
        return None


def scrape_profile(soup):
    """Extract rating, review count, students, hours from profile page."""
    data = {}

    if not soup:
        return data

    text = soup.get_text(" ", strip=True)

    # Rating  e.g. "4.7"
    m = re.search(r'\b(4|5)\.\d\b', text)
    if m:
        data["rating"] = m.group(0)

    # Review count  e.g. "40 reviews" or "39 reviews"
    m = re.search(r'(\d+)\s+reviews?', text, re.IGNORECASE)
    if m:
        data["review_count"] = int(m.group(1))

    # Students taught
    m = re.search(r'(\d+)\s+students?\s+taught', text, re.IGNORECASE)
    if m:
        data["students"] = int(m.group(1))

    # Hours of classes
    m = re.search(r'(\d+)\s+hours?\s+of\s+classes', text, re.IGNORECASE)
    if m:
        data["hours"] = int(m.group(1))

    return data


def scrape_reviews(soup):
    """Extract individual reviews."""
    reviews = []

    if not soup:
        return reviews

    # UrbanPro review blocks vary — try multiple selectors
    blocks = (
        soup.find_all("div", class_=re.compile(r'review', re.I)) or
        soup.find_all("div", class_=re.compile(r'testimonial', re.I)) or
        soup.find_all("li",  class_=re.compile(r'review', re.I))
    )

    for block in blocks[:20]:
        text_el = (
            block.find(class_=re.compile(r'comment|text|content|body', re.I)) or
            block.find("p")
        )
        name_el = (
            block.find(class_=re.compile(r'name|author|reviewer', re.I)) or
            block.find("strong")
        )
        stars_el = block.find(class_=re.compile(r'star|rating', re.I))
        date_el  = block.find(class_=re.compile(r'date|time', re.I))

        text  = text_el.get_text(strip=True)  if text_el  else ""
        name  = name_el.get_text(strip=True)  if name_el  else "Student"
        stars = 5
        date  = date_el.get_text(strip=True)  if date_el  else ""

        if stars_el:
            filled = len(stars_el.find_all(class_=re.compile(r'fill|active|yellow', re.I)))
            if filled:
                stars = filled

        if text and len(text) > 20:
            reviews.append({
                "name":  name,
                "text":  text,
                "stars": stars,
                "date":  date,
            })

    return reviews


def load_existing():
    """Load existing data.json so we don't lose manually added data."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}


def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Saved to {DATA_FILE}")


def main():
    print("🔍 Scraping UrbanPro profile...")
    profile_soup = fetch(PROFILE_URL)
    profile_data = scrape_profile(profile_soup)

    print("🔍 Scraping reviews...")
    reviews_soup = fetch(REVIEWS_URL)
    reviews      = scrape_reviews(reviews_soup)

    # Load existing and merge
    existing = load_existing()

    updated = {
        **existing,
        "last_updated": datetime.now().strftime("%B %Y"),
        "rating":       profile_data.get("rating",       existing.get("rating",       "4.7")),
        "review_count": profile_data.get("review_count", existing.get("review_count", 40)),
        "students":     profile_data.get("students",     existing.get("students",     86)),
        "hours":        profile_data.get("hours",        existing.get("hours",        566)),
        "reviews":      reviews if reviews else existing.get("reviews", []),
    }

    print(f"\n📊 Results:")
    print(f"   Rating       : {updated['rating']}")
    print(f"   Reviews      : {updated['review_count']}")
    print(f"   Students     : {updated['students']}")
    print(f"   Hours        : {updated['hours']}")
    print(f"   Reviews found: {len(updated['reviews'])}")

    if not reviews:
        print("\n⚠  Live review scraping returned nothing (UrbanPro may have changed layout).")
        print("   Existing reviews in data.json are preserved.")
        print("   You can manually paste new reviews into data.json anytime.")

    save(updated)


if __name__ == "__main__":
    main()
