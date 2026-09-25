"""
config.py — FoodMetric USA Taxonomy & Filter Rules (Revised for 2026 Trends)
"""

CATEGORIES = {
    "savory-snack-plates": {
        "name": "Savory Snack Plates, Pickle Plates & Briny Snacks",
        "keywords": [
            "snack plate", "pickle plate", "charcuterie for one",
            "girl dinner", "savory snack", "savory toppings",
            "pickle everything", "goat cheese snack", "briny snack",
            "pickle dip", "pickle ranch", "pickle chips",
            "spicy pickle", "pickle fries", "pickle pizza",
            "pickle salad", "pickle bowl", "pickle cotton candy",
            "cottage cheese dip", "cottage cheese snack",
            "savory yogurt", "savory cottage cheese"
        ],
        "base_volume": 45000, # High-volume snack and pickle trend cluster
    },
    "swicy-flavor-systems": {
        "name": "Swicy, Sweet Heat & Global Flavor Mashups",
        "keywords": [
            "swicy", "sweet spicy", "sweet heat", "honey chipotle",
            "hot honey", "hot honey pizza", "hot honey chicken",
            "hot honey fries", "chili crisp", "chili crisp plus",
            "chili oil", "briny sweet", "spicy pickles",
            "spicy honey", "miso", "miso snack", "miso caramel",
            "tom yum", "tom yum flavored", "gochujang",
            "gochujang honey", "tajin", "tajin fruit",
            "sweet heat", "spicy ranch", "spicy mayo",
            "global flavors", "flavor mashup"
        ],
        "base_volume": 38000, # High-velocity flavor and fusion trend cluster
    },
    "dubai-pistachio-universe": {
        "name": "Dubai Chocolate, Pistachio, Kunafa & Premium Filled Desserts",
        "keywords": [
            "dubai chocolate", "dubai chocolate bar", "dubai chocolate strawberry",
            "dubai chocolate dessert", "dubai chocolate ice cream",
            "dubai chewy cookie", "dubai cookie", "dubai dessert",
            "pistachio cream", "pistachio butter", "pistachio dessert",
            "pistachio latte", "pistachio croissant", "pistachio cookie",
            "pistachio chocolate", "pistachio ice cream",
            "pistachio kunafa", "kunafa", "knafeh", "kataifi",
            "chocolate kataifi", "filled chocolate", "stuffed chocolate"
        ],
        "base_volume": 36000, # Persistent viral dessert and pistachio ecosystem
    },
    "matcha-culture": {
        "name": "Matcha, Green Tea & Viral Matcha Desserts",
        "keywords": [
            "matcha", "matcha latte", "iced matcha",
            "strawberry matcha", "banana matcha", "blueberry matcha",
            "matcha einspanner", "matcha tiramisu", "matcha cheesecake",
            "matcha cookies", "matcha chocolate", "matcha dessert",
            "matcha soft serve", "matcha ice cream", "matcha pudding",
            "matcha croissant", "matcha cream", "matcha foam",
            "dirty matcha", "matcha lemonade", "matcha mocktail"
        ],
        "base_volume": 34000, # Strong beverage, dessert and creator-content cluster
    },
    "protein-foods": {
        "name": "High-Protein Foods, Cottage Cheese & Protein Desserts",
        "keywords": [
            "high protein", "protein snack", "protein dessert",
            "protein pudding", "protein ice cream", "protein cereal",
            "protein coffee", "protein latte", "protein smoothie",
            "protein shake", "protein yogurt", "protein greek yogurt",
            "greek yogurt", "cottage cheese", "cottage cheese bowl",
            "cottage cheese ice cream", "cottage cheese flatbread",
            "cottage cheese pasta", "cottage cheese cheesecake",
            "cottage cheese cookie dough", "protein jell-o",
            "protein fluff", "protein bark", "protein bites",
            "high protein breakfast", "high protein dessert"
        ],
        "base_volume": 32000, # Major protein-focused recipe and snack ecosystem
    },
    "viral-texture-treats": {
        "name": "Gooey, Chewy, Crunchy, Filled & Interactive Treats",
        "keywords": [
            "gooey", "chewy", "crunchy", "crispy", "crack open",
            "pull apart", "cheese pull", "cheese stretch",
            "lava cake", "lava cookie", "stuffed cookie",
            "filled cookie", "filled croissant", "stuffed croissant",
            "oozing", "melty", "smashable treat", "smash cake",
            "smash dessert", "crackable chocolate", "crack dessert",
            "frozen fruit cluster", "yogurt bark", "grape yogurt bark",
            "yogurt tiramisu", "japanese yogurt cheesecake",
            "candy salad", "musubi snack", "mochi",
            "chewy mochi", "viral dessert"
        ],
        "base_volume": 30000, # High visual shareability and texture-driven content
    },
    "viral-recipe-hacks": {
        "name": "Viral Recipes, Food Hacks & Creator Recipes",
        "keywords": [
            "viral recipe", "viral food", "food hack", "food hacks",
            "tiktok recipe", "tiktok food", "viral tiktok recipe",
            "easy viral recipe", "5 minute recipe", "3 ingredient recipe",
            "one pan recipe", "air fryer recipe", "air fryer hack",
            "air fryer snack", "air fryer dessert", "sheet pan recipe",
            "lazy recipe", "lazy girl recipe", "meal hack",
            "breakfast hack", "lunch hack", "dinner hack",
            "snack hack", "dessert hack", "copycat recipe",
            "restaurant hack", "fast food hack"
        ],
        "base_volume": 29000, # Discovery engine for emerging creator-led recipes
    },
    "functional-beverages": {
        "name": "Functional Beverages, Hydration & Better-for-You Drinks",
        "keywords": [
            "banana latte", "banana matcha", "matcha einspanner",
            "electrolyte powder", "electrolytes", "hydration powder",
            "hydration drink", "hydration mix", "coconut water",
            "coconut water drink", "protein coffee", "protein latte",
            "protein water", "prebiotic soda", "probiotic soda",
            "functional beverage", "functional drink",
            "gut health drink", "gut health soda", "fiber drink",
            "fiber soda", "adaptogen drink", "mushroom drink",
            "energy drink", "energy powder", "mocktail",
            "viral mocktail", "wellness drink"
        ],
        "base_volume": 28000, # High-growth beverage and hydration ecosystem
    },
    "viral-candy-freeze-dried": {
        "name": "Freeze-Dried Candy, Sour Candy & Viral Candy",
        "keywords": [
            "freeze dried candy", "freeze dried candy tiktok",
            "freeze dried skittles", "freeze dried gummy",
            "freeze dried gummies", "freeze dried nerds",
            "freeze dried starburst", "freeze dried marshmallow",
            "freeze dried fruit", "freeze dried snacks",
            "sour candy", "sour gummies", "gummy candy",
            "gummy clusters", "nerd clusters", "candy grapes",
            "candy salad", "candy mix", "viral candy",
            "tiktok candy", "viral gummies", "giant gummy"
        ],
        "base_volume": 25000, # Highly visual snack and TikTok Shop category
    },
    "cpg-test-lab-innovations": {
        "name": "CPG Viral Products, Limited Editions & Creator Collabs",
        "keywords": [
            "creator collab snack", "creator collaboration food",
            "creator collab food", "flavor swap", "flavor collab",
            "limited edition flavor", "limited edition snack",
            "limited time flavor", "tiktok shop food",
            "tiktok shop snack", "tiktok shop exclusive",
            "viral snack brand", "viral food brand",
            "internet famous snack", "viral grocery product",
            "new snack drop", "snack drop", "food drop",
            "skittles pop'd", "olipop", "poppi",
            "athletic brewing", "premium dark chocolate",
            "new flavor", "new food product"
        ],
        "base_volume": 24000, # Trend-testing and creator-driven CPG innovation
    },
    "global-comfort-food": {
        "name": "Global Comfort Foods, Fusion & Cross-Cultural Recipes",
        "keywords": [
            "korean food", "korean corn dog", "korean fried chicken",
            "korean marinated eggs", "gochujang", "kimbap",
            "musubi", "onigiri", "japanese cheesecake",
            "japanese yogurt cheesecake", "ramen hack",
            "ramen recipe", "chinese street food", "chinese dessert",
            "indian street food", "indian dessert", "mexican street food",
            "birria", "birria ramen", "birria tacos",
            "elote", "esquites", "filipino food",
            "ube", "ube dessert", "ube latte",
            "middle eastern dessert", "kunafa", "knafeh",
            "global comfort food", "fusion food"
        ],
        "base_volume": 22000, # Cross-cultural discovery and fusion content
    },
    "high-protein-comfort": {
        "name": "High-Protein Versions of American Comfort Food",
        "keywords": [
            "protein pizza", "high protein pizza",
            "protein burger", "high protein burger",
            "protein pancakes", "protein waffles",
            "protein french toast", "protein mac and cheese",
            "protein pasta", "protein ramen", "protein tacos",
            "protein quesadilla", "protein burrito",
            "protein chicken", "protein fries",
            "high protein comfort food", "macro friendly",
            "macro friendly recipe", "low calorie high protein",
            "high protein meal", "high protein dinner",
            "high protein lunch", "high protein breakfast"
        ],
        "base_volume": 20000, # Creator-driven transformation of familiar comfort foods
    },
    "viral-fruit-snacks": {
        "name": "Viral Fruit, Frozen Fruit & Fruit-Based Snacks",
        "keywords": [
            "frozen fruit", "frozen fruit snack", "frozen fruit cluster",
            "frozen grapes", "candy grapes", "chocolate grapes",
            "yogurt covered fruit", "chocolate covered fruit",
            "fruit bark", "yogurt bark", "fruit roll up",
            "fruit roll up hack", "fruit leather",
            "watermelon hack", "watermelon pizza",
            "pineapple snack", "mango snack", "tajin fruit",
            "fruit bowl", "fruit snack", "viral fruit",
            "frozen strawberry", "frozen banana"
        ],
        "base_volume": 19000, # Highly visual fruit and frozen-snack formats
    }
}

# Exclusion list to filter out packaging, plastics, apparel, electronics,
# kitchen accessories, and non-food dropshipping junk that can falsely
# trigger food-related TikTok Shop searches.
BLACKLIST_KEYWORDS = [
    "tumbler", "water bottle", "stanley cup", "plastic jar",
    "ziplock bag", "food storage bag", "storage bag",
    "t-shirt", "shirt", "apparel", "clothing",
    "sticker", "label", "glass jar", "storage container",
    "kitchen gadget", "kitchen tool", "kitchen accessory",
    "apron", "mug", "coffee mug", "keychain",
    "phone case", "car accessory", "phone holder",
    "cutting board", "food container", "lunch box",
    "meal prep container", "silicone mold", "bento box",
    "straw", "straw set", "utensil", "spoon", "fork",
    "plate", "bowl", "cup", "glassware", "napkin",
    "tablecloth", "kitchen towel", "oven mitt",
    "recipe book", "cookbook", "digital download",
    "ebook", "pdf", "course", "template"
]

# Currency & Pricing Logic in USD
PRICE_FLOOR_USD = 2.00       # Filter out samples, digital items, or junk
PRICE_CEILING_USD = 150.00   # Filter out bulk wholesale or high-end non-food products
