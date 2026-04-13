#!/usr/bin/env python3
"""
Recipe Search Application

A GUI application for searching recipes using the Spoonacular API.
"""

from gui import RecipeSearchGUI


def main():
    """Main entry point for the application."""
    app = RecipeSearchGUI()
    app.run()


if __name__ == "__main__":
    main()