#!/usr/bin/env python3
"""
Simple test script for the Recipe Search application.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import SearchParameters, Recipe, Ingredient, RecipeDetails, SubstituteResult


def test_models():
    """Test the data models."""
    print("Testing data models...")

    # Test SearchParameters
    params = SearchParameters(
        query="chicken",
        dish_type="main course",
        diet="gluten free",
        cuisine="italian",
        exclude_cuisine="chinese",
        include_ingredients="garlic, onion",
        exclude_ingredients="nuts",
        equipment="oven",
        number=5,
        offset=0
    )

    params_dict = params.to_dict()
    assert params_dict["query"] == "chicken"
    assert params_dict["type"] == "main course"
    assert params_dict["diet"] == "gluten free"
    print("✓ SearchParameters model works")

    # Test Recipe
    recipe = Recipe.from_dict({
        "id": 123,
        "title": "Chicken Parmesan",
        "image": "https://example.com/image.jpg"
    })
    assert recipe.id == 123
    assert recipe.title == "Chicken Parmesan"
    print("✓ Recipe model works")

    # Test Ingredient
    ingredient = Ingredient.from_dict({
        "nameClean": "chicken breast",
        "image": "chicken.jpg",
        "original": "2 chicken breasts"
    })
    assert ingredient.name_clean == "chicken breast"
    assert ingredient.original == "2 chicken breasts"
    print("✓ Ingredient model works")

    print("All model tests passed!")


if __name__ == "__main__":
    test_models()