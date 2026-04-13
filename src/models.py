"""
Data models for the Recipe Search application.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SearchParameters:
    """Parameters for recipe search."""
    query: str
    dish_type: str = ""
    diet: str = ""
    cuisine: str = ""
    exclude_cuisine: str = ""
    include_ingredients: str = ""
    exclude_ingredients: str = ""
    equipment: str = ""
    number: int = 5
    offset: int = 0
    instructions_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API call."""
        return {
            "query": self.query.lower(),
            "type": self.dish_type,
            "diet": self.diet,
            "cuisine": self.cuisine,
            "excludeCuisine": self.exclude_cuisine.replace(" ", "").lower(),
            "includeIngredients": self.include_ingredients.replace(" ", "").lower(),
            "excludeIngredients": self.exclude_ingredients.replace(" ", "").lower(),
            "equipment": self.equipment.replace(" ", "").lower(),
            "number": self.number,
            "offset": self.offset,
            "instructionsRequired": self.instructions_required,
        }


@dataclass
class Recipe:
    """Recipe data structure."""
    id: int
    title: str
    image: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Recipe':
        return cls(
            id=data['id'],
            title=data['title'],
            image=data['image']
        )


@dataclass
class Ingredient:
    """Ingredient data structure."""
    name_clean: str
    image: str
    original: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Ingredient':
        return cls(
            name_clean=data.get('nameClean', ''),
            image=data.get('image', ''),
            original=data.get('original', '')
        )


@dataclass
class RecipeDetails:
    """Detailed recipe information."""
    title: str
    source_name: str
    cooking_minutes: int
    preparation_minutes: int
    servings: int
    ingredients: List[Ingredient]
    instructions: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RecipeDetails':
        return cls(
            title=data['title'],
            source_name=data.get('sourceName', ''),
            cooking_minutes=data.get('cookingMinutes', 0),
            preparation_minutes=data.get('preparationMinutes', 0),
            servings=data.get('servings', 1),
            ingredients=[Ingredient.from_dict(ing) for ing in data.get('extendedIngredients', [])],
            instructions=data.get('instructions', '')
        )


@dataclass
class SubstituteResult:
    """Substitute search result."""
    status: str
    substitutes: List[str]
    message: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubstituteResult':
        return cls(
            status=data.get('status', 'failure'),
            substitutes=data.get('substitutes', []),
            message=data.get('message', '')
        )