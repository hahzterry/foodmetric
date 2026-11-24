# FoodMetric USA
English-only US dashboard. No live products are bundled. The old Vietnam benchmark and media were removed. The original CDP/TikWM discovery is replaced by a reviewed feed import; automatic live TikTok sourcing is not connected. Random snack selection and product/video links are retained; tarot, voucher promotions, snack battle and creator promotion are removed.

## Deploy
Vercel root directory: `web`; framework: Next.js. No environment keys needed for the static dashboard. Locally: `cd web && npm ci && npm run dev`.

## Import
Populate `data/us_products.json` with reviewed records, then run `python scraper/pipeline.py` from the repository root. Market, language and currency are required source attestations, not automatically verified. Prices and GMV use integer USD cents. Do not import old VND records. Example schema (illustrative only, not live):

```json
[
  {
    "market": "US",
    "language": "en",
    "currency": "USD",
    "product_id": "example",
    "product_name": "Example snack",
    "category_slug": "other-snacks",
    "shop_id": "example-shop",
    "shop_name": "Example shop",
    "current_price": 599,
    "historical_sold": 0,
    "estimated_daily_units": 0,
    "review_count": 0,
    "product_rating": 0,
    "is_shop_official": false,
    "anomaly_flag": false,
    "affiliate_url": "https://example.com/product",
    "image_url": "",
    "video_url": ""
  }
]
```
The daily workflow republishes the reviewed input, not fresh external data. Existing SQL migration and Supabase storage utility are legacy optional infrastructure, not used by the new dashboard. Use a new database if extending the US importer to avoid mixing currencies.
