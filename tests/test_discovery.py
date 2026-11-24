import unittest
from scraper.pipeline import build
class FeedTests(unittest.TestCase):
    def test_empty(self): self.assertEqual(build([])["leaderboard"], [])
    def test_non_us(self): self.assertEqual(build([{"market":"VN","language":"en","currency":"USD"}])["leaderboard"], [])
    def test_non_english(self): self.assertEqual(build([{"market":"US","language":"vi","currency":"USD"}])["leaderboard"], [])
    def test_cents(self):
        p=dict(market="US",language="en",currency="USD",category_slug="other-snacks",product_id="test",current_price=599,historical_sold=20,estimated_daily_units=3,review_count=0,affiliate_url="https://example.com/product")
        self.assertEqual(build([p])["leaderboard"][0]["estimated_daily_gmv"],1797)
