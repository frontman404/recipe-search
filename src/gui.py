"""
GUI components for the Recipe Search application.
"""

import tkinter as tk
from tkinter import font, messagebox
from PIL import ImageTk
from typing import List, Callable, Optional
import re

from api_client import SpoonacularAPI
from models import Recipe, RecipeDetails, SubstituteResult
import config


class RecipeSearchGUI:
    """Main GUI class for the Recipe Search application."""

    def __init__(self):
        self.api_client: Optional[SpoonacularAPI] = None
        self.recipes: List[Recipe] = []
        self.current_recipe_index = 0
        self.current_ingredient_index = 0

        self._setup_main_window()
        self._create_frames()
        self._setup_fonts()
        self._create_search_frame()
        self._create_api_frame()
        self._create_substitute_frame()
        self._create_results_frame()

    def _setup_main_window(self):
        """Initialize the main window."""
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(config.WINDOW_GEOMETRY)

    def _create_frames(self):
        """Create the main frames."""
        self.first_frame = tk.LabelFrame(
            self.root, text="Recipe search", padx=3, pady=3
        )
        self.first_frame.grid(row=0, column=0, padx=3, pady=3, rowspan=3)

        self.second_frame = tk.LabelFrame(
            self.root, text="API setup", padx=3, pady=3
        )
        self.second_frame.grid(row=0, column=1, padx=3, pady=3)

        self.third_frame = tk.LabelFrame(
            self.root, text="Substitute search", padx=3, pady=3
        )
        self.third_frame.grid(row=1, column=1, padx=3, pady=3)

        self.forth_frame = tk.LabelFrame(
            self.root, text="Recipes list", padx=3, pady=3
        )
        self.forth_frame.grid(row=2, column=1, padx=3, pady=3)

    def _setup_fonts(self):
        """Setup font objects."""
        self.bolded = font.Font(size=config.BOLD_FONT_SIZE, weight="bold")
        self.small = font.Font(size=config.SMALL_FONT_SIZE)

    def _create_search_frame(self):
        """Create the recipe search frame."""
        row_number = 0

        # Query input
        query_label = tk.Label(self.first_frame, text="What are you looking for?")
        query_label["font"] = self.bolded
        query_label.grid(row=row_number, column=0, columnspan=4)
        self.query_entry = tk.Entry(self.first_frame, width=30, justify="center")
        self.query_entry.grid(row=row_number + 1, column=0, columnspan=4, pady=3)
        self.query_entry.insert(0, config.DEFAULT_QUERY)
        row_number += 2

        # Dish type selection
        type_label = tk.Label(self.first_frame, text="What type of dish you want?")
        type_label["font"] = self.bolded
        type_label.grid(row=row_number, column=0, columnspan=4)
        self.type_choice = tk.StringVar()
        self.type_choice.set("any")
        row_number += 1
        for i, dish_type in enumerate(config.DISH_TYPES):
            type_radiobutton = tk.Radiobutton(
                self.first_frame, text=dish_type, variable=self.type_choice, value=dish_type
            )
            type_radiobutton.grid(row=row_number, column=i % config.RADIOBUTTON_COLUMNS, sticky=tk.W)
            if i in [3, 7, 11]:
                row_number += 1

        # Diet selection
        diet_label = tk.Label(self.first_frame, text="What diet are you following?")
        diet_label["font"] = self.bolded
        diet_label.grid(row=row_number, column=0, columnspan=4)
        self.diet_choice = tk.StringVar()
        self.diet_choice.set("none")
        row_number += 1
        for i, diet in enumerate(config.DIETS):
            diet_radiobutton = tk.Radiobutton(
                self.first_frame, text=diet, variable=self.diet_choice, value=diet
            )
            diet_radiobutton.grid(row=row_number, column=i % config.RADIOBUTTON_COLUMNS, sticky=tk.W)
            if i in [3, 7, 11]:
                row_number += 1

        # Cuisine selection
        cuisine_label = tk.Label(self.first_frame, text="What cuisine shall the recipe belong to?")
        cuisine_label["font"] = self.bolded
        cuisine_label.grid(row=row_number, column=0, columnspan=4)
        self.cuisine_choice = tk.StringVar()
        self.cuisine_choice.set("any")
        row_number += 1
        for i, cuisine in enumerate(config.CUISINES):
            cuisine_radiobutton = tk.Radiobutton(
                self.first_frame, text=cuisine, variable=self.cuisine_choice, value=cuisine
            )
            cuisine_radiobutton.grid(row=row_number, column=i % config.RADIOBUTTON_COLUMNS, sticky=tk.W)
            if i in [3, 7, 11, 15, 19, 23, 26]:
                row_number += 1

        # Exclude cuisine
        nocuisine_label = tk.Label(
            self.first_frame,
            text="What cuisine shall the recipe not belong to? Choose from the list above.*",
        )
        nocuisine_label["font"] = self.bolded
        nocuisine_label.grid(row=row_number, column=0, columnspan=4)
        self.nocuisine_entry = tk.Entry(self.first_frame, width=50, justify="center")
        self.nocuisine_entry.grid(row=row_number + 1, column=0, columnspan=4, pady=3)
        self.nocuisine_entry.insert(0, config.DEFAULT_EXCLUDE_CUISINE)
        row_number += 2

        # Include ingredients
        include_label = tk.Label(
            self.first_frame,
            text="Any specific ingredients you want in your recipes?*",
        )
        include_label["font"] = self.bolded
        include_label.grid(row=row_number, column=0, columnspan=4)
        self.include_entry = tk.Entry(self.first_frame, width=50, justify="center")
        self.include_entry.grid(row=row_number + 1, column=0, columnspan=4, pady=3)
        self.include_entry.insert(0, config.DEFAULT_INCLUDE_INGREDIENTS)
        row_number += 2

        # Exclude ingredients
        exclude_label = tk.Label(
            self.first_frame,
            text="Any specific ingredients you don't want in your recipes?*",
        )
        exclude_label["font"] = self.bolded
        exclude_label.grid(row=row_number, column=0, columnspan=4)
        self.exclude_entry = tk.Entry(self.first_frame, width=50, justify="center")
        self.exclude_entry.grid(row=row_number + 1, column=0, columnspan=4, pady=3)
        self.exclude_entry.insert(0, config.DEFAULT_EXCLUDE_INGREDIENTS)
        row_number += 2

        # Equipment
        equipment_label = tk.Label(
            self.first_frame,
            text="Any kitchen equipment you want to use in particular?**",
        )
        equipment_label["font"] = self.bolded
        equipment_label.grid(row=row_number, column=0, columnspan=4)
        self.equipment_entry = tk.Entry(self.first_frame, width=50, justify="center")
        self.equipment_entry.grid(row=row_number + 1, column=0, columnspan=4, pady=3)
        self.equipment_entry.insert(0, config.DEFAULT_EQUIPMENT)
        row_number += 2

        # Number of results
        number_label = tk.Label(
            self.first_frame, text="How many results you want to recieve?"
        )
        number_label["font"] = self.bolded
        number_label.grid(row=row_number, column=0, columnspan=2)
        extra_number_label = tk.Label(
            self.first_frame, text="A number from 1 to 10"
        )
        extra_number_label["font"] = self.small
        extra_number_label.grid(row=row_number + 1, column=0, columnspan=2)
        self.number_entry = tk.Entry(self.first_frame, width=10, justify="center")
        self.number_entry.insert(0, str(config.DEFAULT_NUMBER))
        self.number_entry.grid(row=row_number + 2, column=0, columnspan=2)

        # Offset
        offset_label = tk.Label(
            self.first_frame, text="How many results you want to skip?"
        )
        offset_label["font"] = self.bolded
        offset_label.grid(row=row_number, column=2, columnspan=2)
        extra_offset_label = tk.Label(
            self.first_frame, text="A number from 0 to 900"
        )
        extra_offset_label["font"] = self.small
        extra_offset_label.grid(row=row_number + 1, column=2, columnspan=2)
        self.offset_entry = tk.Entry(self.first_frame, width=10, justify="center")
        self.offset_entry.insert(0, str(config.DEFAULT_OFFSET))
        self.offset_entry.grid(row=row_number + 2, column=2, columnspan=2)
        row_number += 3

        # Search button
        search_button = tk.Button(
            self.first_frame, text="Search recipes", command=self._search_recipes
        )
        search_button.grid(row=row_number, column=0, columnspan=4, pady=2)

        # Help text
        extra_label1 = tk.Label(
            self.first_frame,
            text="*Separate them with a comma. Leave blank if none.",
        )
        extra_label1['font'] = self.small
        extra_label1.grid(row=row_number + 1, column=0, columnspan=4, sticky=tk.W)
        extra_label2 = tk.Label(
            self.first_frame,
            text="**Multiple options will be interpreted as 'or'. Separate them with a comma. Leave blank if none.",
        )
        extra_label2['font'] = self.small
        extra_label2.grid(row=row_number + 2, column=0, columnspan=4, sticky=tk.W)

    def _create_api_frame(self):
        """Create the API setup frame."""
        api_info = tk.Label(self.second_frame, text="Set up your API connection")
        api_info["font"] = self.bolded
        api_info.grid(row=0, column=0, columnspan=2)

        api_key_label = tk.Label(self.second_frame, text="Key")
        api_key_label.grid(row=1, column=0)
        self.api_key_entry = tk.Entry(self.second_frame, width=60, justify='center')
        self.api_key_entry.grid(row=1, column=1, pady=3)
        self.api_key_entry.insert(0, config.DEFAULT_API_KEY)

        api_host_label = tk.Label(self.second_frame, text="Host")
        api_host_label.grid(row=2, column=0, pady=3)
        self.api_host_entry = tk.Entry(self.second_frame, width=60, justify='center')
        self.api_host_entry.grid(row=2, column=1)
        self.api_host_entry.insert(0, config.DEFAULT_API_HOST)

        api_button = tk.Button(self.second_frame, text="Submit", command=self._setup_api)
        api_button.grid(row=3, column=0, columnspan=2, pady=3)

        info = tk.Label(
            self.second_frame,
            text="Powered by Spoonacular API on rapidapi.com",
        )
        info.grid(row=5, column=0, columnspan=2)

    def _create_substitute_frame(self):
        """Create the substitute search frame."""
        substitute_label = tk.Label(
            self.third_frame, text="Type an ingredient and find out a substitute for it."
        )
        substitute_label["font"] = self.bolded
        substitute_label.grid(row=0, column=0)

        self.ingredient_entry = tk.Entry(self.third_frame, width=30, justify='center')
        self.ingredient_entry.grid(row=1, column=0, pady=3)
        self.ingredient_entry.insert(0, config.DEFAULT_SUBSTITUTE_INGREDIENT)

        substitute_button = tk.Button(
            self.third_frame, text="Find substitute", command=self._find_substitute
        )
        substitute_button.grid(row=2, column=0, columnspan=2, pady=3)

    def _create_results_frame(self):
        """Create the results frame (initially empty)."""
        pass

    def _setup_api(self):
        """Setup the API client with provided credentials."""
        api_key = self.api_key_entry.get()
        api_host = self.api_host_entry.get()
        self.api_client = SpoonacularAPI(api_key, api_host)

        success_label = tk.Label(self.second_frame, text="Success")
        success_label.grid(row=4, column=0, columnspan=2)
        self.second_frame.after(5000, success_label.destroy)

    def _search_recipes(self):
        """Perform recipe search."""
        if not self.api_client:
            messagebox.showerror("API Error", "Please set up your API connection first.")
            return

        # Clear previous results
        for widget in self.forth_frame.winfo_children():
            widget.destroy()

        # Get search parameters
        search_params = {
            "instructionsRequired": True,
            "query": self.query_entry.get().lower(),
            "type": "" if self.type_choice.get() == "any" else self.type_choice.get(),
            "diet": "" if self.diet_choice.get() == "none" else self.diet_choice.get(),
            "cuisine": "" if self.cuisine_choice.get() == "any" else self.cuisine_choice.get(),
            "excludeCuisine": self.nocuisine_entry.get().replace(" ", "").lower(),
            "includeIngredients": self.include_entry.get().replace(" ", "").lower(),
            "excludeIngredients": self.exclude_entry.get().replace(" ", "").lower(),
            "equipment": self.equipment_entry.get().replace(" ", "").lower(),
            "number": int(self.number_entry.get()),
            "offset": int(self.offset_entry.get()),
        }

        try:
            recipes_data = self.api_client.search_recipes(search_params)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to search recipes: {str(e)}")
            return

        if "results" not in recipes_data:
            messagebox.showerror("API Error", "Check your API host and/or key information")
            return

        self.recipes = [Recipe.from_dict(r) for r in recipes_data["results"]]

        if not self.recipes:
            error_label = tk.Label(
                self.forth_frame,
                text="No recipes found!\nCheck your search filters and try again.",
            )
            error_label.grid(row=0, column=0)
            return

        # Display recipes
        row_number = 0
        choice_label = tk.Label(
            self.forth_frame, text="Select the recipe you would like to prepare"
        )
        choice_label["font"] = self.bolded
        choice_label.grid(row=row_number, column=0)
        row_number += 1

        self.recipe_choice = tk.IntVar()
        for recipe in self.recipes:
            recipe_radiobutton = tk.Radiobutton(
                self.forth_frame, text=recipe.title, variable=self.recipe_choice, value=recipe.id
            )
            recipe_radiobutton.grid(row=row_number, column=0, sticky=tk.W)
            row_number += 1

        choose_button = tk.Button(
            self.forth_frame, text="Choose recipe", command=self._choose_recipe
        )
        choose_button.grid(row=row_number, column=0, pady=5)

        # Show image viewer
        self._show_image_viewer()

    def _show_image_viewer(self):
        """Show the image viewer for recipes."""
        self.image_viewer = tk.Toplevel()
        self.recipes_viewer = tk.LabelFrame(
            self.image_viewer, text="Pictures of recipes found", padx=3, pady=3
        )
        self.recipes_viewer.grid(row=0, column=0, padx=3, pady=3)

        self.ingredients_viewer = tk.LabelFrame(
            self.image_viewer, text="Pictures of ingredients required", padx=3, pady=3
        )
        self.ingredients_viewer.grid(row=0, column=1, padx=3, pady=3)

        self._update_recipe_image()

    def _update_recipe_image(self):
        """Update the recipe image display."""
        # Clear previous content
        for label in self.recipes_viewer.grid_slaves():
            if int(label.grid_info()["row"]) != 2:
                label.grid_forget()

        recipe = self.recipes[self.current_recipe_index]

        try:
            raw_image = self.api_client.download_image(recipe.image)
            image = ImageTk.PhotoImage(data=raw_image)
            picture_label = tk.Label(self.recipes_viewer, image=image)
            picture_label.image = image
            picture_label.grid(row=0, column=0, columnspan=2)
        except Exception:
            # Fallback if image fails to load
            picture_label = tk.Label(self.recipes_viewer, text="[Image not available]")
            picture_label.grid(row=0, column=0, columnspan=2)

        title_label = tk.Label(self.recipes_viewer, text=recipe.title)
        title_label.grid(row=1, column=0, columnspan=2)

        status_label = tk.Label(
            self.recipes_viewer,
            text=f"Recipe {self.current_recipe_index + 1} of {len(self.recipes)}",
            relief=tk.SUNKEN,
        )
        status_label.grid(row=3, column=0, columnspan=2)

        # Navigation buttons
        button_back = tk.Button(
            self.recipes_viewer, text="<<", command=self._previous_recipe
        )
        button_back.grid(row=2, column=0, pady=5)
        button_forward = tk.Button(
            self.recipes_viewer, text=">>", command=self._next_recipe
        )
        button_forward.grid(row=2, column=1, pady=5)

    def _previous_recipe(self):
        """Navigate to previous recipe."""
        if self.current_recipe_index > 0:
            self.current_recipe_index -= 1
            self._update_recipe_image()

    def _next_recipe(self):
        """Navigate to next recipe."""
        if self.current_recipe_index < len(self.recipes) - 1:
            self.current_recipe_index += 1
            self._update_recipe_image()

    def _choose_recipe(self):
        """Handle recipe selection."""
        recipe_id = self.recipe_choice.get()
        if not recipe_id:
            return

        try:
            recipe_data = self.api_client.get_recipe_information(recipe_id)
            recipe_details = RecipeDetails.from_dict(recipe_data)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to get recipe details: {str(e)}")
            return

        self._show_recipe_details(recipe_details)

    def _show_recipe_details(self, recipe: RecipeDetails):
        """Show detailed recipe information."""
        # Update ingredients viewer
        self.current_ingredient_index = 0
        self._update_ingredient_image(recipe.ingredients)

        # Show recipe window
        recipe_window = tk.Toplevel()
        title_label = tk.Label(
            recipe_window,
            text=f"{recipe.title} by {recipe.source_name}",
        )
        title_label.grid(row=0, column=0, columnspan=2)

        ingredients_frame = tk.LabelFrame(
            recipe_window, text="Details", padx=5, pady=5
        )
        ingredients_frame.grid(row=1, column=0, padx=5, pady=5)
        steps_frame = tk.LabelFrame(
            recipe_window, text="Steps to follow", padx=5, pady=5
        )
        steps_frame.grid(row=1, column=1, padx=5, pady=5)

        # Recipe details
        row_number = 0
        prep_time_label = tk.Label(
            ingredients_frame,
            text=f"Preparation time: {recipe.preparation_minutes} mins",
        )
        prep_time_label.grid(row=row_number, column=0)
        row_number += 1

        cook_time_label = tk.Label(
            ingredients_frame,
            text=f"Cooking time: {recipe.cooking_minutes} mins",
        )
        cook_time_label.grid(row=row_number, column=0)
        row_number += 1

        servings_label = tk.Label(
            ingredients_frame,
            text=f"Number of servings: {recipe.servings}",
        )
        servings_label.grid(row=row_number, column=0)
        row_number += 1

        ingredients_string = "\n".join(
            f"* {ing.original.strip('*')}" for ing in recipe.ingredients
        )
        ingredients_label = tk.Label(
            ingredients_frame, text=f"Ingredients are:\n{ingredients_string}"
        )
        ingredients_label.grid(row=row_number, column=0, sticky=tk.W)

        # Instructions
        title_label = tk.Label(
            steps_frame, text="In order to prepare the dish do the following:\n"
        )
        title_label.grid(row=0, column=0)
        clean_instructions = re.sub(" +", " ", recipe.instructions)
        steps_label = tk.Label(
            steps_frame, text=clean_instructions, wraplength=config.IMAGE_WRAP_LENGTH
        )
        steps_label.grid(row=1, column=0)

    def _update_ingredient_image(self, ingredients: List):
        """Update the ingredient image display."""
        if not ingredients:
            return

        # Clear previous content
        for label in self.ingredients_viewer.grid_slaves():
            if int(label.grid_info()["row"]) != 2:
                label.grid_forget()

        ingredient = ingredients[self.current_ingredient_index]

        try:
            image_url = config.INGREDIENT_IMAGE_URL.format(ingredient.image)
            raw_image = self.api_client.download_image(image_url)
            image = ImageTk.PhotoImage(data=raw_image)
            picture_label = tk.Label(self.ingredients_viewer, image=image)
            picture_label.image = image
            picture_label.grid(row=0, column=0, columnspan=2)
        except Exception:
            picture_label = tk.Label(self.ingredients_viewer, text="[Image not available]")
            picture_label.grid(row=0, column=0, columnspan=2)

        title_label = tk.Label(
            self.ingredients_viewer, text=ingredient.name_clean
        )
        title_label.grid(row=1, column=0, columnspan=2)

        status_label = tk.Label(
            self.ingredients_viewer,
            text=f"Ingredient {self.current_ingredient_index + 1} of {len(ingredients)}",
            relief=tk.SUNKEN,
        )
        status_label.grid(row=3, column=0, columnspan=2)

        # Navigation buttons
        button_back = tk.Button(
            self.ingredients_viewer, text="<<", command=lambda: self._previous_ingredient(ingredients)
        )
        button_back.grid(row=2, column=0, pady=5)
        button_forward = tk.Button(
            self.ingredients_viewer, text=">>", command=lambda: self._next_ingredient(ingredients)
        )
        button_forward.grid(row=2, column=1, pady=5)

    def _previous_ingredient(self, ingredients):
        """Navigate to previous ingredient."""
        if self.current_ingredient_index > 0:
            self.current_ingredient_index -= 1
            self._update_ingredient_image(ingredients)

    def _next_ingredient(self, ingredients):
        """Navigate to next ingredient."""
        if self.current_ingredient_index < len(ingredients) - 1:
            self.current_ingredient_index += 1
            self._update_ingredient_image(ingredients)

    def _find_substitute(self):
        """Find ingredient substitutes."""
        if not self.api_client:
            messagebox.showerror("API Error", "Please set up your API connection first.")
            return

        # Clear previous results
        for label in self.third_frame.grid_slaves():
            if int(label.grid_info()["row"]) > 2:
                label.grid_forget()

        ingredient = self.ingredient_entry.get()

        try:
            result_data = self.api_client.find_substitutes(ingredient)
            result = SubstituteResult.from_dict(result_data)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to find substitutes: {str(e)}")
            return

        if "status" not in result_data:
            messagebox.showerror("API Error", "Check your API host and/or key information")
            return

        if result.status == "success" and result.substitutes:
            label = tk.Label(self.third_frame, text="The ingredient can be substituted with:")
            label.grid(row=3, column=0)
            row_number = 4
            for substitute in result.substitutes:
                result_label = tk.Label(self.third_frame, text=f"* {substitute}")
                result_label.grid(row=row_number, column=0)
                row_number += 1
        else:
            result_label = tk.Label(self.third_frame, text="No results")
            result_label.grid(row=3, column=0)
            self.third_frame.after(5000, result_label.destroy)

    def run(self):
        """Start the GUI main loop."""
        self.root.mainloop()