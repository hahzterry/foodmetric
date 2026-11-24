"""US TikTok Shop product pipeline. Prices and GMV are integer USD cents."""

import json
import datetime
import argparse
import logging
import math
from pathlib import Path
from urllib.parse import urlparse

try:
    from .config import CATEGORIES, BLACKLIST_KEYWORDS
except ImportError:
    from config import CATEGORIES, BLACKLIST_KEYWORDS


ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data/us_products.json"
OUTPUT = ROOT / "web/public/data/leaderboard_latest.json"

MARKET = "US"
LANGUAGE = "en"
CURRENCY = "USD"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("foodmetric.pipeline")


def valid_https_url(value):
    if not isinstance(value, str):
        return False

    parsed = urlparse(value)

    return (
        parsed.scheme == "https"
        and bool(parsed.hostname)
    )


def valid_tiktok_url(value):
    if not valid_https_url(value):
        return False

    hostname = urlparse(value).hostname or ""

    return (
        hostname == "tiktok.com"
        or hostname.endswith(".tiktok.com")
    )


def is_blacklisted(product_name):
    name = str(product_name).lower()

    return any(
        keyword.lower() in name
        for keyword in BLACKLIST_KEYWORDS
    )


def validate_product(row):

    if not isinstance(row, dict):
        raise ValueError("Product must be a dictionary")

    if row.get("market") != MARKET:
        raise ValueError("Non-US product")

    if row.get("language") != LANGUAGE:
        raise ValueError("Non-English product")

    if row.get("currency") != CURRENCY:
        raise ValueError("Non-USD product")

    p = dict(row)

    product_id = str(
        p.get("product_id") or ""
    ).strip()

    product_name = str(
        p.get("product_name") or ""
    ).strip()

    if not product_id:
        raise ValueError("Missing product ID")

    if not product_name:
        raise ValueError("Missing product name")

    if is_blacklisted(product_name):
        raise ValueError("Blacklisted product")

    if p.get("category_slug") not in CATEGORIES:
        raise ValueError("Unknown category")

    p["product_id"] = product_id
    p["product_name"] = product_name

    for key in (
        "current_price",
        "historical_sold",
        "estimated_daily_units",
        "review_count"
    ):

        value = p.get(key, 0)

        if type(value) is not int or value < 0:
            raise ValueError("Invalid " + key)

        p[key] = value

    if p["current_price"] <= 0:
        raise ValueError("Invalid product price")

    for key in (
        "affiliate_url",
        "video_url",
        "image_url"
    ):

        value = p.get(key, "")

        if value and not valid_https_url(value):
            raise ValueError(
                "HTTPS URL required: " + key
            )

        p[key] = value or ""

    if not p["affiliate_url"]:
        raise ValueError("Missing product URL")

    if not valid_tiktok_url(p["affiliate_url"]):
        raise ValueError("Invalid TikTok Shop URL")

    p["shop_id"] = str(
        p.get("shop_id") or ""
    )

    p["shop_name"] = str(
        p.get("shop_name") or "Unknown Shop"
    )

    rating = float(
        p.get("product_rating") or 0
    )

    if not math.isfinite(rating) or not 0 <= rating <= 5:
        raise ValueError("Invalid product rating")

    p["product_rating"] = rating

    p["is_shop_official"] = (
        p.get("is_shop_official") is True
    )

    p["anomaly_flag"] = (
        p.get("anomaly_flag") is True
    )

    p["estimated_daily_gmv"] = (
        p["current_price"]
        * p["estimated_daily_units"]
    )

    return p


def build(rows):

    if not isinstance(rows, list):
        raise ValueError(
            "Product feed must contain a JSON array"
        )

    items = []
    seen = set()

    rejected = 0
    duplicates = 0

    logger.info(
        "Processing %s product records",
        len(rows)
    )

    for row in rows:

        try:

            p = validate_product(row)

            if p["product_id"] in seen:
                duplicates += 1
                continue

            seen.add(p["product_id"])

            items.append(p)

        except (ValueError, TypeError, KeyError, OverflowError) as exc:

            rejected += 1

            logger.warning(
                "Product skipped: %s",
                str(exc)
            )

    items.sort(
        key=lambda p: (
            p["estimated_daily_gmv"],
            p["estimated_daily_units"],
            p["historical_sold"],
            p["review_count"]
        ),
        reverse=True
    )

    counts = {}
    totals = {}

    for i, p in enumerate(items, 1):

        category = p["category_slug"]

        counts[category] = (
            counts.get(category, 0) + 1
        )

        totals[category] = (
            totals.get(category, 0)
            + p["estimated_daily_gmv"]
        )

        p.update(
            rank_overall=i,
            rank_in_category=counts[category]
        )

    top_category = (
        max(totals, key=totals.get)
        if totals
        else "other-snacks"
    )

    total_gmv = sum(
        p["estimated_daily_gmv"]
        for p in items
    )

    total_units = sum(
        p["estimated_daily_units"]
        for p in items
    )

    total_historical_sold = sum(
        p["historical_sold"]
        for p in items
    )

    total_reviews = sum(
        p["review_count"]
        for p in items
    )

    now = datetime.datetime.now(
        datetime.timezone.utc
    )

    top_gmv_product = (
        items[0]
        if items and total_gmv > 0
        else None
    )

    growth_candidates = [
        p for p in items
        if p["estimated_daily_units"] > 0
        and p["historical_sold"] > 0
    ]

    fastest_growth_product = (
        max(
            growth_candidates,
            key=lambda p: (
                p["estimated_daily_units"]
                / p["historical_sold"]
            )
        )
        if growth_candidates
        else None
    )

    payload = {

        "metadata": {

            "market": MARKET,

            "currency": CURRENCY,

            "language": LANGUAGE,

            "last_updated": now.isoformat(),

            "snapshot_date": now.date().isoformat(),

            "data_source_mode": (
                "US product feed; sales estimates "
                "supplied by source"
            ),

            "total_products_indexed": len(items),

            "total_estimated_daily_gmv": total_gmv,

            "total_estimated_daily_units": total_units,

            "total_historical_sold": total_historical_sold,

            "total_reviews": total_reviews,

            "total_categories": len(CATEGORIES),

            "total_rejected_products": rejected,

            "total_duplicate_products": duplicates

        },

        "categories": CATEGORIES,

        "bento_kpis": {

            "top_gmv_product": top_gmv_product,

            "fastest_growth_product": fastest_growth_product,

            "top_category": {

                "slug": top_category,

                "name": CATEGORIES[top_category]["name"],

                "gmv": totals.get(
                    top_category,
                    0
                )

            },

            "top_viral_hook": {

                "hook_text": "",

                "recommended_sound": "",

                "views_benchmark": ""

            }

        },

        "leaderboard": items

    }

    logger.info(
        "Products accepted: %s",
        len(items)
    )

    logger.info(
        "Products rejected: %s",
        rejected
    )

    logger.info(
        "Duplicates removed: %s",
        duplicates
    )

    logger.info(
        "Estimated daily units: %s",
        total_units
    )

    logger.info(
        "Estimated daily GMV: $%s",
        f"{total_gmv / 100:,.2f}"
    )

    return payload


def save_json(path, payload):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temporary = path.with_suffix(".tmp")

    temporary.write_text(

        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            allow_nan=False
        ) + "\n",

        encoding="utf-8"

    )

    temporary.replace(path)


def main():

    parser = argparse.ArgumentParser(
        description="US TikTok Shop product pipeline"
    )

    parser.add_argument(
        "--input",
        type=Path,
        default=INPUT,
        help="US product JSON feed"
    )

    parser.add_argument(
        "--discover",
        action="store_true",
        help="Discover US TikTok Shop products first"
    )

    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow an empty leaderboard to be published"
    )

    args = parser.parse_args()

    logger.info(
        "Starting US TikTok Shop pipeline"
    )

    if args.discover:

        logger.info(
            "Starting automated product discovery"
        )

        if __package__:
           from .discovery_engine import main as discover
        else:
           from discovery_engine import main as discover

        discover()

        logger.info(
            "Automated discovery completed"
        )

        return

    if not args.input.exists():

        raise FileNotFoundError(
            f"Product feed not found: {args.input}"
        )

    logger.info(
        "Reading product feed: %s",
        args.input
    )

    rows = json.loads(
        args.input.read_text(
            encoding="utf-8"
        )
    )

    payload = build(rows)

    product_count = payload["metadata"][
        "total_products_indexed"
    ]

    if product_count == 0 and not args.allow_empty:

        raise RuntimeError(
            "No valid US products found. "
            "Existing leaderboard has been preserved."
        )

    save_json(
        OUTPUT,
        payload
    )

    logger.info(
        "Leaderboard generated: %s",
        OUTPUT
    )

    logger.info(
        "Total products indexed: %s",
        product_count
    )

    logger.info(
        "Pipeline completed successfully"
    )


if __name__ == "__main__":
    main()