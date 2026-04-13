"""
API client for interacting with the Spoonacular API.
"""

import requests
from urllib.request import Request, urlopen
from typing import Dict, List, Optional, Any

import config


class SpoonacularAPI:
    """Client for Spoonacular Recipe API."""

    def __init__(self, api_key: str, api_host: str = config.DEFAULT_API_HOST):
        self.api_key = api_key
        self.api_host = api_host
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host,
        }

    def search_recipes(self, search_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for recipes based on given parameters.

        Args:
            search_params: Dictionary containing search parameters

        Returns:
            JSON response from the API
        """
        url = config.COMPLEX_SEARCH_URL
        response = requests.get(url, headers=self.headers, params=search_params)
        response.raise_for_status()
        return response.json()

    def get_recipe_information(self, recipe_id: int) -> Dict[str, Any]:
        """
        Get detailed information about a specific recipe.

        Args:
            recipe_id: The ID of the recipe

        Returns:
            JSON response with recipe details
        """
        url = config.RECIPE_INFO_URL.format(recipe_id)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def find_substitutes(self, ingredient: str) -> Dict[str, Any]:
        """
        Find substitutes for a given ingredient.

        Args:
            ingredient: Name of the ingredient

        Returns:
            JSON response with substitute information
        """
        url = config.SUBSTITUTE_URL
        params = {"ingredientName": ingredient}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def download_image(url: str) -> bytes:
        """
        Download image from URL.

        Args:
            url: Image URL

        Returns:
            Raw image bytes
        """
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return urlopen(req).read()