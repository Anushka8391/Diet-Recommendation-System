import requests
from functools import lru_cache

# Curated static fallback images (Unsplash, permanent URLs) keyed by food keyword.
_FALLBACKS = {
    "chicken":   "https://images.unsplash.com/photo-1598103442097-8b74394b95c7?w=400&h=300&fit=crop",
    "beef":      "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop",
    "pork":      "https://images.unsplash.com/photo-1432139509613-5c4255815697?w=400&h=300&fit=crop",
    "fish":      "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&h=300&fit=crop",
    "salmon":    "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400&h=300&fit=crop",
    "pasta":     "https://images.unsplash.com/photo-1551183053-bf91798d047b?w=400&h=300&fit=crop",
    "pizza":     "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop",
    "soup":      "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=300&fit=crop",
    "salad":     "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop",
    "cake":      "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=400&h=300&fit=crop",
    "cookie":    "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400&h=300&fit=crop",
    "bread":     "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=400&h=300&fit=crop",
    "rice":      "https://images.unsplash.com/photo-1536304993881-ff86e0c9b98f?w=400&h=300&fit=crop",
    "egg":       "https://images.unsplash.com/photo-1510693206972-df098062cb71?w=400&h=300&fit=crop",
    "sandwich":  "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=400&h=300&fit=crop",
    "burger":    "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&h=300&fit=crop",
    "steak":     "https://images.unsplash.com/photo-1558030006-450675393462?w=400&h=300&fit=crop",
    "vegetable": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
    "fruit":     "https://images.unsplash.com/photo-1490474418585-ba9bad8fd0ea?w=400&h=300&fit=crop",
    "smoothie":  "https://images.unsplash.com/photo-1502741126161-b048400d085d?w=400&h=300&fit=crop",
    "breakfast": "https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=400&h=300&fit=crop",
    "pancake":   "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop",
    "muffin":    "https://images.unsplash.com/photo-1607958996333-41ade62d6f26?w=400&h=300&fit=crop",
    "stew":      "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a?w=400&h=300&fit=crop",
}
_DEFAULT_IMAGE = "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop"


def _keyword_fallback(name: str) -> str:
    lower = name.lower()
    for keyword, url in _FALLBACKS.items():
        if keyword in lower:
            return url
    return _DEFAULT_IMAGE


@lru_cache(maxsize=512)
def get_image_url(recipe_name: str) -> str:
    """Return a food image URL for the given recipe name.

    Queries TheMealDB (free, no API key) first for a matching dish image.
    Falls back to a keyword-matched static Unsplash photo on miss or error.
    """
    try:
        resp = requests.get(
            "https://www.themealdb.com/api/json/v1/1/search.php",
            params={"s": recipe_name},
            timeout=5,
        )
        if resp.ok:
            data = resp.json()
            if data.get("meals"):
                return data["meals"][0]["strMealThumb"]
    except Exception:
        pass
    return _keyword_fallback(recipe_name)
