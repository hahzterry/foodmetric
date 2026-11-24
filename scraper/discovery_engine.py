"""Automated US TikTok Shop food product discovery."""

import os
import json
import logging
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

try:
    from .config import CATEGORIES
    from .pipeline import build
except ImportError:
    from config import CATEGORIES
    from pipeline import build

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env")

INPUT = ROOT / "data/us_products.json"
OUTPUT = ROOT / "web/public/data/leaderboard_latest.json"

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")
APIFY_ACTOR_ID = os.getenv("APIFY_ACTOR_ID", "")

MAX_PRODUCTS = int(os.getenv("MAX_PRODUCTS", "100"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("foodmetric")


US_KEYWORDS = {
    "chips-crackers": [
        "viral chips",
        "spicy chips",
        "potato chips",
        "pretzels",
        "popcorn",
        "crackers"
    ],
    "jerky-protein": [
        "beef jerky",
        "protein bars",
        "protein snacks",
        "meat sticks"
    ],
    "candy-sweets": [
        "freeze dried candy",
        "Dubai chocolate",
        "gummy candy",
        "sour candy",
        "chamoy candy",
        "cookies"
    ],
    "beverages": [
        "energy drinks",
        "iced coffee",
        "sparkling water",
        "protein drinks"
    ],
    "other-snacks": [
        "viral snacks",
        "trail mix",
        "fruit snacks",
        "pickle kits",
        "mixed nuts"
    ]
}


def pick(item, *keys, default=None):
    for key in keys:
        value = item.get(key)
        if value is not None and value != "":
            return value
    return default


def number(value):
    if value is None:
        return 0

    text = str(value).replace(",", "").strip().upper()

    multiplier = 1

    if text.endswith("K"):
        multiplier = 1000
        text = text[:-1]
    elif text.endswith("M"):
        multiplier = 1000000
        text = text[:-1]

    return max(0, int(Decimal(text) * multiplier))


def price_to_cents(value):
    text = str(value).replace("$", "").replace(",", "").strip()

    amount = Decimal(text)

    if amount < 0:
        raise ValueError("Negative price")

    return int(
        (amount * 100).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    )


def https_url(value):
    if not isinstance(value, str):
        return ""

    parsed = urlparse(value)

    if parsed.scheme == "https" and parsed.hostname:
        return value

    return ""


def is_us_product(item):
    market = str(
        pick(item, "market", "country", "region", default="")
    ).upper()

    currency = str(
        pick(item, "currency", "currencyCode", default="")
    ).upper()

    language = str(
        pick(item, "language", "locale", default="")
    ).lower()

    return (
        market in ("US", "USA", "UNITED STATES")
        and currency == "USD"
        and language in ("en", "en-us", "en_us", "english")
    )


def normalize_product(item, category):
    if not is_us_product(item):
        return None

    product_id = pick(
        item,
        "productId",
        "product_id",
        "id"
    )

    product_name = pick(
        item,
        "productName",
        "product_name",
        "title",
        "name"
    )

    product_url = https_url(
        pick(
            item,
            "productUrl",
            "product_url",
            "affiliate_url",
            "url"
        )
    )

    price = pick(
        item,
        "price",
        "salePrice",
        "currentPrice"
    )

    if not product_id or not product_name or not product_url:
        return None

    if price is None:
        return None

    host = urlparse(product_url).hostname or ""

    if not (
        host == "tiktok.com"
        or host.endswith(".tiktok.com")
    ):
        return None

    return {
        "market": "US",
        "language": "en",
        "currency": "USD",

        "product_id": str(product_id),
        "product_name": str(product_name),
        "category_slug": category,

        "shop_id": str(
            pick(item, "shopId", "shop_id", default="")
        ),

        "shop_name": str(
            pick(
                item,
                "shopName",
                "shop_name",
                "sellerName",
                default="Unknown shop"
            )
        ),

        "current_price": price_to_cents(price),

        "historical_sold": number(
            pick(
                item,
                "soldCount",
                "totalSold",
                "historical_sold",
                default=0
            )
        ),

        "estimated_daily_units": number(
            pick(
                item,
                "dailySales",
                "estimated_daily_units",
                default=0
            )
        ),

        "review_count": number(
            pick(
                item,
                "reviewCount",
                "review_count",
                default=0
            )
        ),

        "product_rating": float(
            pick(
                item,
                "rating",
                "product_rating",
                default=0
            )
        ),

        "is_shop_official": (
            item.get("isOfficialShop") is True
        ),

        "anomaly_flag": False,

        "affiliate_url": product_url,

        "image_url": https_url(
            pick(
                item,
                "imageUrl",
                "image_url",
                "image",
                default=""
            )
        ),

        "video_url": https_url(
            pick(
                item,
                "videoUrl",
                "video_url",
                default=""
            )
        )
    }


def discover_products(keyword):
    actor = APIFY_ACTOR_ID.replace("/", "~")

    url = (
        f"https://api.apify.com/v2/acts/{actor}"
        "/run-sync-get-dataset-items"
    )

    headers = {
        "Authorization": f"Bearer {APIFY_TOKEN}",
        "Content-Type": "application/json"
    }

    # Configure these input fields to match
    # your selected Apify actor's input schema.

    payload = {
        "searchQueries": [keyword],
        "country": "US",
        "language": "en",
        "maxItems": MAX_PRODUCTS
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    items = response.json()

    if not isinstance(items, list):
        raise ValueError("Expected a product list from Apify")

    return items


def save_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(".tmp")

    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    temporary.replace(path)


def main():
    if not APIFY_TOKEN:
        raise RuntimeError("Missing APIFY_TOKEN")

    if not APIFY_ACTOR_ID:
        raise RuntimeError("Missing APIFY_ACTOR_ID")

    logger.info("Starting US TikTok Shop discovery")

    products = {}

    for category, keywords in US_KEYWORDS.items():

        if category not in CATEGORIES:
            continue

        for keyword in keywords:

            logger.info("Searching: %s", keyword)

            try:
                results = discover_products(keyword)

                logger.info(
                    "Received %s results",
                    len(results)
                )

            except (requests.RequestException, ValueError) as exc:
                logger.warning(
                    "Search failed for %s: %s",
                    keyword,
                    type(exc).__name__
                )
                continue

            for item in results:
                try:
                    product = normalize_product(
                        item,
                        category
                    )

                    if product:
                        products.setdefault(
                            product["product_id"],
                            product
                        )

                except (ValueError, TypeError, ArithmeticError):
                    logger.warning(
                        "Skipping invalid product record"
                    )

    rows = list(products.values())

    if not rows:
        raise RuntimeError(
            "No valid US English USD products found. "
            "Check actor input and output fields. "
            "Existing data has been preserved."
        )

    payload = build(rows)

    save_json(INPUT, rows)
    save_json(OUTPUT, payload)

    logger.info("Products indexed: %s", len(rows))
    logger.info("Database: %s", INPUT)
    logger.info("Leaderboard: %s", OUTPUT)
    logger.info("Discovery completed successfully")


if __name__ == "__main__":
    main()