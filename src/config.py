"""
Configuration and constants for the Recipe Search application.
"""

# API Configuration
DEFAULT_API_HOST = "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
DEFAULT_API_KEY = "Enter your private key"

# UI Constants
WINDOW_TITLE = "Recipe Search"
# WINDOW_ICON = "food.ico"  # Icon file not available
WINDOW_GEOMETRY = "+300+3"

# Font settings
BOLD_FONT_SIZE = 9
SMALL_FONT_SIZE = 8

# Search options
DISH_TYPES = [
    "main course",
    "side dish",
    "dessert",
    "appetizer",
    "salad",
    "bread",
    "breakfast",
    "soup",
    "beverage",
    "sauce",
    "drink",
    "any",
]

DIETS = [
    "gluten free",
    "ketogenic",
    "vegetarian",
    "lacto vegetarian",
    "ovo vegetarian",
    "vegan",
    "pescetarian",
    "paleo",
    "primal",
    "low FODMAP",
    "whole30",
    "none",
]

CUISINES = [
    "african",
    "british",
    "cajun",
    "caribbean",
    "chinese",
    "eastern european",
    "european",
    "french",
    "german",
    "greek",
    "indian",
    "irish",
    "italian",
    "japanese",
    "korean",
    "latin american",
    "mediterranean",
    "mexican",
    "middle eastern",
    "nordic",
    "southern",
    "spanish",
    "vietnamese",
    "thai",
    "any",
]

# Default search values
DEFAULT_QUERY = "burger"
DEFAULT_EXCLUDE_CUISINE = "eastern european"
DEFAULT_INCLUDE_INGREDIENTS = "eggs"
DEFAULT_EXCLUDE_INGREDIENTS = "potatoes"
DEFAULT_EQUIPMENT = "pan"
DEFAULT_NUMBER = 5
DEFAULT_OFFSET = 0
DEFAULT_SUBSTITUTE_INGREDIENT = "butter"

# API URLs
COMPLEX_SEARCH_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
RECIPE_INFO_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information"
SUBSTITUTE_URL = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/substitutes"

# Image URLs
INGREDIENT_IMAGE_URL = "https://spoonacular.com/cdn/ingredients_250x250/{}"

# UI Layout
RADIOBUTTON_COLUMNS = 4
IMAGE_WRAP_LENGTH = 700