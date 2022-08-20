import requests
from urllib.request import Request, urlopen
import tkinter as tk
from tkinter import font
from tkinter import messagebox
import re
from PIL import ImageTk


root = tk.Tk()
root.title("Recipe Search")
root.iconbitmap("food.ico")
root.geometry("+300+3")

bolded = font.Font(size=9, weight="bold")
small = font.Font(size=8)

# Creating frames
first_frame = tk.LabelFrame(root, text="Recipe search", padx=3, pady=3)
first_frame.grid(row=0, column=0, padx=3, pady=3, rowspan=3)

second_frame = tk.LabelFrame(root, text="API setup", padx=3, pady=3)
second_frame.grid(row=0, column=1, padx=3, pady=3)

third_frame = tk.LabelFrame(root, text="Substitute search", padx=3, pady=3)
third_frame.grid(row=1, column=1, padx=3, pady=3)

forth_frame = tk.LabelFrame(root, text="Recipes list", padx=3, pady=3)
forth_frame.grid(row=2, column=1, padx=3, pady=3)

# Display the search filters on first frame
row_number_1st = 0
query_label = tk.Label(first_frame, text="What are you looking for?")
query_label["font"] = bolded
query_label.grid(row=row_number_1st, column=0, columnspan=4)
query_entry = tk.Entry(first_frame, width=30, justify="center")
query_entry.grid(row=row_number_1st + 1, column=0, columnspan=4, pady=3)
query_entry.insert(0, "burger")
row_number_1st += 2

type_label = tk.Label(first_frame, text="What type of dish you want?")
type_label["font"] = bolded
type_label.grid(row=row_number_1st, column=0, columnspan=4)
types = [
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
type_choice = tk.StringVar()
type_choice.set("any")
row_number_1st += 1
for i in range(len(types)):
    type_radiobutton = tk.Radiobutton(
        first_frame, text=types[i], variable=type_choice, value=types[i]
    )
    type_radiobutton.grid(row=row_number_1st, column=i % 4, sticky=tk.W)
    if i in [3, 7, 11]:
        row_number_1st += 1

diet_label = tk.Label(first_frame, text="What diet are you following?")
diet_label["font"] = bolded
diet_label.grid(row=row_number_1st, column=0, columnspan=4)
diets = [
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
diet_choice = tk.StringVar()
diet_choice.set("none")
row_number_1st += 1
for i in range(len(diets)):
    diet_radiobutton = tk.Radiobutton(
        first_frame, text=diets[i], variable=diet_choice, value=diets[i]
    )
    diet_radiobutton.grid(row=row_number_1st, column=i % 4, sticky=tk.W)
    if i in [3, 7, 11]:
        row_number_1st += 1

cuisine_label = tk.Label(first_frame, text="What cuisine shall the recipe belong to?")
cuisine_label["font"] = bolded
cuisine_label.grid(row=row_number_1st, column=0, columnspan=4)
cuisines = [
    "african",
    "american",
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
    "jewish",
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
cuisine_choice = tk.StringVar()
cuisine_choice.set("any")
row_number_1st += 1
for i in range(len(cuisines)):
    cuisine_radiobutton = tk.Radiobutton(
        first_frame, text=cuisines[i], variable=cuisine_choice, value=cuisines[i]
    )
    cuisine_radiobutton.grid(row=row_number_1st, column=i % 4, sticky=tk.W)
    if i in [3, 7, 11, 15, 19, 23, 26]:
        row_number_1st += 1

nocuisine_label = tk.Label(
    first_frame,
    text="What cuisine shall the recipe not belong to? Choose from the list above.*",
)
nocuisine_label["font"] = bolded
nocuisine_label.grid(row=row_number_1st, column=0, columnspan=4)
nocuisine_entry = tk.Entry(first_frame, width=50, justify="center")
nocuisine_entry.grid(row=row_number_1st + 1, column=0, columnspan=4, pady=3)
nocuisine_entry.insert(0, "eastern european")
row_number_1st += 2

include_label = tk.Label(
    first_frame,
    text="Any specific ingredients you want in your recipes?*",
)
include_label["font"] = bolded
include_label.grid(row=row_number_1st, column=0, columnspan=4)
include_entry = tk.Entry(first_frame, width=50, justify="center")
include_entry.grid(row=row_number_1st + 1, column=0, columnspan=4, pady=3)
include_entry.insert(0, "eggs")
row_number_1st += 2

exclude_label = tk.Label(
    first_frame,
    text="Any specific ingredients you don't want in your recipes?*",
)
exclude_label["font"] = bolded
exclude_label.grid(row=row_number_1st, column=0, columnspan=4)
exclude_entry = tk.Entry(first_frame, width=50, justify="center")
exclude_entry.grid(row=row_number_1st + 1, column=0, columnspan=4, pady=3)
exclude_entry.insert(0, "potatoes")
row_number_1st += 2

equipment_label = tk.Label(
    first_frame,
    text="Any kitchen equipment you want to use in particular?**",
)
equipment_label["font"] = bolded
equipment_label.grid(row=row_number_1st, column=0, columnspan=4)
equipment_entry = tk.Entry(first_frame, width=50, justify="center")
equipment_entry.grid(row=row_number_1st + 1, column=0, columnspan=4, pady=3)
equipment_entry.insert(0, "pan")
row_number_1st += 2

number_label = tk.Label(
    first_frame, text="How many results you want to recieve?"
)
number_label["font"] = bolded
number_label.grid(row=row_number_1st, column=0, columnspan=2)
extra_number_label = tk.Label(
    first_frame, text="A number from 1 to 10"
)
extra_number_label["font"] = small
extra_number_label.grid(row=row_number_1st + 1, column=0, columnspan=2)
number_entry = tk.Entry(first_frame, width=10, justify="center")
number_entry.insert(0, "5")
number_entry.grid(row=row_number_1st + 2, column=0, columnspan=2)

offset_label = tk.Label(
    first_frame, text="How many results you want to skip?"
)
offset_label["font"] = bolded
offset_label.grid(row=row_number_1st, column=2, columnspan=2)
extra_offset_label = tk.Label(
    first_frame, text="A number from 0 to 900"
)
extra_offset_label["font"] = small
extra_offset_label.grid(row=row_number_1st + 1, column=2, columnspan=2)
offset_entry = tk.Entry(first_frame, width=10, justify="center")
offset_entry.insert(0, "0")
offset_entry.grid(row=row_number_1st + 2, column=2, columnspan=2)
row_number_1st += 3


def create_search_string():
    search_string = {}
    search_string["instructionsRequired"] = True
    search_string["query"] = query_entry.get().lower()
    search_string["type"] = "" if type_choice.get() == "any" else type_choice.get()
    search_string["diet"] = "" if diet_choice.get() == "none" else diet_choice.get()
    search_string["cuisine"] = (
        "" if cuisine_choice.get() == "any" else cuisine_choice.get()
    )
    search_string["excludeCuisine"] = nocuisine_entry.get().replace(" ", "").lower()
    search_string["includeIngredients"] = include_entry.get().replace(" ", "").lower()
    search_string["excludeIngredients"] = exclude_entry.get().replace(" ", "").lower()
    search_string["equipment"] = equipment_entry.get().replace(" ", "").lower()
    search_string["number"] = int(number_entry.get())
    search_string["offset"] = int(offset_entry.get())
    url1 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"
    recipes_raw = requests.request("GET", url1, headers=headers, params=search_string)
    recipes = recipes_raw.json()
    # recipes = {
    #     "results": [
    #         {
    #             "title": "chicken",
    #             "id": 1,
    #             "image": "https://spoonacular.com/recipeImages/1680541-312x231.jpg",
    #         },
    #         {
    #             "title": "beef",
    #             "id": 2,
    #             "image": "https://spoonacular.com/recipeImages/1680541-312x231.jpg",
    #         },
    #         {
    #             "title": "fish",
    #             "id": 3,
    #             "image": "https://spoonacular.com/recipeImages/1680541-312x231.jpg",
    #         },
    #     ]
    # }

    for widget in forth_frame.winfo_children():
        widget.destroy()

    if "results" not in recipes.keys():
        messagebox.showerror(
            "API connection problem!", "Check your API host and/or key information"
        )
    elif len(recipes["results"]) == 0:
        messagebox.showinfo("No recipes found!", "No recipes found!")
        error_label = tk.Label(
            forth_frame,
            text="No recipes found!\nCheck your search filters and try again.",
        )
        error_label.grid(row=0, column=0)
    else:
        # Display the list of recipes on forth frame
        row_number_4th = 0
        recipes_found = recipes["results"]
        choice_label = tk.Label(
            forth_frame, text="Select the recipe you would like to prepare"
        )
        choice_label["font"] = bolded
        choice_label.grid(row=row_number_4th, column=0)
        row_number_4th += 1
        recipe_choice = tk.IntVar()
        recipe_choice.set("none")
        for i in range(len(recipes_found)):
            title = recipes_found[i]["title"]
            id = recipes_found[i]["id"]
            recipe_radiobutton = tk.Radiobutton(
                forth_frame, text=title, variable=recipe_choice, value=id
            )
            recipe_radiobutton.grid(row=row_number_4th, column=0, sticky=tk.W)
            row_number_4th += 1

        # Making an image viewer for pictures provided by API
        image_viewer = tk.Toplevel()

        recipes_viewer = tk.LabelFrame(
            image_viewer, text="Pictures of recipes found", padx=3, pady=3
        )
        recipes_viewer.grid(row=0, column=0, padx=3, pady=3)
        ingredients_viewer = tk.LabelFrame(
            image_viewer, text="Pictures of ingredients required", padx=3, pady=3
        )
        ingredients_viewer.grid(row=0, column=1, padx=3, pady=3)

        # Pictures for recipes found
        global recipes_index
        recipes_index = 0
        req1 = Request(
            recipes_found[recipes_index]["image"], headers={"User-Agent": "Mozilla/5.0"}
        )
        raw_image = urlopen(req1).read()
        image = ImageTk.PhotoImage(data=raw_image)
        picture_label = tk.Label(recipes_viewer, image=image)
        picture_label.image = image
        picture_label.grid(row=0, column=0, columnspan=2)

        title_label = tk.Label(recipes_viewer, text=recipes_found[recipes_index]["title"])
        title_label.grid(row=1, column=0, columnspan=2)

        recipes_status = tk.Label(
            recipes_viewer,
            text="Recipe " + str(recipes_index + 1) + " of " + str(len(recipes_found)),
            relief=tk.SUNKEN,
        )
        recipes_status.grid(row=3, column=0, columnspan=2)

        def previous_recipe():
            global recipes_index

            if recipes_index > 0:
                for label in recipes_viewer.grid_slaves():
                    if int(label.grid_info()["row"]) != 2:
                        label.grid_forget()

                recipes_index -= 1
                req1 = Request(
                    recipes["results"][recipes_index]["image"],
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                raw_image = urlopen(req1).read()
                image = ImageTk.PhotoImage(data=raw_image)
                picture_label = tk.Label(recipes_viewer, image=image)
                picture_label.image = image
                picture_label.grid(row=0, column=0, columnspan=2)

                title_label = tk.Label(
                    recipes_viewer, text=recipes_found[recipes_index]["title"]
                )
                title_label.grid(row=1, column=0, columnspan=2)

                recipes_status = tk.Label(
                    recipes_viewer,
                    text="Recipe "
                    + str(recipes_index + 1)
                    + " of "
                    + str(len(recipes_found)),
                    relief=tk.SUNKEN,
                )
                recipes_status.grid(row=3, column=0, columnspan=2)

        def next_recipe():
            global recipes_index

            if recipes_index < len(recipes_found) - 1:
                for label in recipes_viewer.grid_slaves():
                    if int(label.grid_info()["row"]) != 2:
                        label.grid_forget()

                recipes_index += 1
                req1 = Request(
                    recipes["results"][recipes_index]["image"],
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                raw_image = urlopen(req1).read()
                image = ImageTk.PhotoImage(data=raw_image)
                picture_label = tk.Label(recipes_viewer, image=image)
                picture_label.image = image
                picture_label.grid(row=0, column=0, columnspan=2)

                title_label = tk.Label(
                    recipes_viewer, text=recipes_found[recipes_index]["title"]
                )
                title_label.grid(row=1, column=0, columnspan=2)

                recipes_status = tk.Label(
                    recipes_viewer,
                    text="Recipe "
                    + str(recipes_index + 1)
                    + " of "
                    + str(len(recipes_found)),
                    relief=tk.SUNKEN,
                )
                recipes_status.grid(row=3, column=0, columnspan=2)

        button_back = tk.Button(recipes_viewer, text="<<", command=previous_recipe)
        button_back.grid(row=2, column=0, pady=5)
        button_forward = tk.Button(recipes_viewer, text=">>", command=next_recipe)
        button_forward.grid(row=2, column=1, pady=5)

        def choose_recipe():
            url2 = (
                "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/"
                + str(recipe_choice.get())
                + "/information"
            )
            recipe_information_raw = requests.request("GET", url2, headers=headers)
            recipe_information = recipe_information_raw.json()
            # recipe_information = {
            #     "title": "recipe",
            #     "sourceName": "me",
            #     "cookingMinutes": 5,
            #     "preparationMinutes": 5,
            #     "servings": "1",
            #     "extendedIngredients": [
            #         {"nameClean": "egg", "image": "egg.jpg", "original": "2 eggs"},
            #         {
            #             "nameClean": "salt",
            #             "image": "salt.jpg",
            #             "original": "1 tsp of salt",
            #         },
            #     ],
            #     "instructions": "cook",
            # }

            # Pictures for ingredients needed in the recipe
            global ingredients
            ingredients = recipe_information["extendedIngredients"]
            global ingredients_index
            ingredients_index = 0
            req2 = Request(
                "https://spoonacular.com/cdn/ingredients_250x250/"
                + ingredients[ingredients_index]["image"],
                headers={"User-Agent": "Mozilla/5.0"},
            )
            raw_image = urlopen(req2).read()
            image = ImageTk.PhotoImage(data=raw_image)
            picture_label = tk.Label(ingredients_viewer, image=image)
            picture_label.image = image
            picture_label.grid(row=0, column=0, columnspan=2)

            title_label = tk.Label(
                ingredients_viewer, text=ingredients[ingredients_index]["nameClean"]
            )
            title_label.grid(row=1, column=0, columnspan=2)

            ingredients_status = tk.Label(
                ingredients_viewer,
                text="Ingredient "
                + str(ingredients_index + 1)
                + " of "
                + str(len(ingredients)),
                relief=tk.SUNKEN,
            )
            ingredients_status.grid(row=3, column=0, columnspan=2)

            def previous_ingredient():
                global ingredients_index

                if ingredients_index > 0:
                    for label in ingredients_viewer.grid_slaves():
                        if int(label.grid_info()["row"]) != 2:
                            label.grid_forget()

                    ingredients_index -= 1
                    req2 = Request(
                        "https://spoonacular.com/cdn/ingredients_250x250/"
                        + ingredients[ingredients_index]["image"],
                        headers={"User-Agent": "Mozilla/5.0"},
                    )
                    raw_image = urlopen(req2).read()
                    image = ImageTk.PhotoImage(data=raw_image)
                    picture_label = tk.Label(ingredients_viewer, image=image)
                    picture_label.image = image
                    picture_label.grid(row=0, column=0, columnspan=2)

                    title_label = tk.Label(
                        ingredients_viewer,
                        text=ingredients[ingredients_index]["nameClean"],
                    )
                    title_label.grid(row=1, column=0, columnspan=2)

                    ingredients_status = tk.Label(
                        ingredients_viewer,
                        text="Ingredient "
                        + str(ingredients_index + 1)
                        + " of "
                        + str(len(ingredients)),
                        relief=tk.SUNKEN,
                    )
                    ingredients_status.grid(row=3, column=0, columnspan=2)

            def next_ingredient():
                global ingredients_index

                if ingredients_index < len(ingredients) - 1:
                    for label in ingredients_viewer.grid_slaves():
                        if int(label.grid_info()["row"]) != 2:
                            label.grid_forget()

                    ingredients_index += 1
                    req = Request(
                        "https://spoonacular.com/cdn/ingredients_250x250/"
                        + ingredients[ingredients_index]["image"],
                        headers={"User-Agent": "Mozilla/5.0"},
                    )
                    raw_image = urlopen(req).read()
                    image = ImageTk.PhotoImage(data=raw_image)
                    picture_label = tk.Label(ingredients_viewer, image=image)
                    picture_label.image = image
                    picture_label.grid(row=0, column=0, columnspan=2)

                    title_label = tk.Label(
                        ingredients_viewer,
                        text=ingredients[ingredients_index]["nameClean"],
                    )
                    title_label.grid(row=1, column=0, columnspan=2)

                    ingredients_status = tk.Label(
                        ingredients_viewer,
                        text="Ingredient "
                        + str(ingredients_index + 1)
                        + " of "
                        + str(len(ingredients)),
                        relief=tk.SUNKEN,
                    )
                    ingredients_status.grid(row=3, column=0, columnspan=2)

            button_back = tk.Button(
                ingredients_viewer, text="<<", command=previous_ingredient
            )
            button_back.grid(row=2, column=0, pady=5)
            button_forward = tk.Button(
                ingredients_viewer, text=">>", command=next_ingredient
            )
            button_forward.grid(row=2, column=1, pady=5)

            recipe_window = tk.Toplevel()

            title_label = tk.Label(
                recipe_window,
                text=recipe_information["title"]
                + " by "
                + recipe_information["sourceName"],
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

            # Displaying ingredients list
            row_number_ingredients = 0
            prep_time_label = tk.Label(
                ingredients_frame,
                text="Preparation time: "
                + str(recipe_information["preparationMinutes"])
                + " mins",
            )
            prep_time_label.grid(row=row_number_ingredients, column=0)
            row_number_ingredients += 1

            cook_time_label = tk.Label(
                ingredients_frame,
                text="Cooking time: "
                + str(recipe_information["cookingMinutes"])
                + " mins",
            )
            cook_time_label.grid(row=row_number_ingredients, column=0)
            row_number_ingredients += 1

            servings_label = tk.Label(
                ingredients_frame,
                text="Number of servings: " + str(recipe_information["servings"]),
            )
            servings_label.grid(row=row_number_ingredients, column=0)
            row_number_ingredients += 1

            ingredients_string = ""
            for item in recipe_information["extendedIngredients"]:
                ingredients_string = ingredients_string + "* "
                ingredients_string = (
                    ingredients_string + item["original"].strip("*") + "\n"
                )

            ingredients_label = tk.Label(
                ingredients_frame, text="Ingredients are:\n" + ingredients_string
            )
            ingredients_label.grid(row=row_number_ingredients, column=0, sticky=tk.W)
            row_number_ingredients += 1

            # Showing the steps for making the recipe
            title_label = tk.Label(
                steps_frame, text="In order to prepare the dish do the following:\n"
            )
            title_label.grid(row=0, column=0)
            string = re.sub(" +", " ", recipe_information["instructions"])
            steps_label = tk.Label(steps_frame, text=string, wraplength=700)
            steps_label.grid(row=1, column=0)

        choose_button = tk.Button(forth_frame, text="Choose recipe", command=choose_recipe)
        choose_button.grid(row=row_number_4th, column=0, pady=5)


search_button = tk.Button(first_frame, text="Search recipes", command=create_search_string)
search_button.grid(row=row_number_1st, column=0, columnspan=4, pady=2)


extra_label1 = tk.Label(
    first_frame,
    text="*Separate them with a comma. Leave blank if none.",
)
extra_label1['font'] = small
extra_label1.grid(row=row_number_1st + 1, column=0, columnspan=4, sticky=tk.W)
extra_label2 = tk.Label(
    first_frame,
    text="**Multiple options will be interpreted as 'or'. Separate them with a comma. Leave blank if none.",
)
extra_label2.grid(row=row_number_1st + 2, column=0, columnspan=4, sticky=tk.W)
extra_label2['font'] = small

# Information and API data on second frame
api_info = tk.Label(second_frame, text="Set up your API connection")
api_info["font"] = bolded
api_info.grid(row=0, column=0, columnspan=2)

api_key_label = tk.Label(second_frame, text="Key")
api_key_label.grid(row=1, column=0)

api_key_entry = tk.Entry(second_frame, width=60, justify='center')
api_key_entry.grid(row=1, column=1, pady=3)
api_key_entry.insert(0, "Enter your private key")

api_host_label = tk.Label(second_frame, text="Host")
api_host_label.grid(row=2, column=0, pady=3)

api_host_entry = tk.Entry(second_frame, width=60, justify='center')
api_host_entry.grid(row=2, column=1)
api_host_entry.insert(0, "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")


def api_submit():
    global headers
    headers = {
        "X-RapidAPI-Key": api_key_entry.get(),
        "X-RapidAPI-Host": api_host_entry.get(),
    }
    success_label = tk.Label(second_frame, text="Success")
    success_label.grid(row=4, column=0, columnspan=2)
    second_frame.after(5000, success_label.destroy)


api_button = tk.Button(second_frame, text="Submit", command=api_submit)
api_button.grid(row=3, column=0, columnspan=2, pady=3)

info = tk.Label(
    second_frame,
    text="Powered by Spoonacular API on rapidapi.com\n App icon made by Rank Sol on iconscout.com",
)
info.grid(row=5, column=0, columnspan=2)

# Substitute search on third frame
substitute_label = tk.Label(
    third_frame, text="Type an ingredient and find out a substitute for it."
)
substitute_label["font"] = bolded
substitute_label.grid(row=0, column=0)

ingredient_entry = tk.Entry(third_frame, width=30, justify='center')
ingredient_entry.grid(row=1, column=0, pady=3)
ingredient_entry.insert(0, "butter")


def find_substitute():
    for label in third_frame.grid_slaves():
        if int(label.grid_info()["row"]) > 2:
            label.grid_forget()
    url3 = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/food/ingredients/substitutes"
    ingredient = {"ingredientName": ingredient_entry.get()}
    substitute_result_raw = requests.request(
        "GET", url3, headers=headers, params=ingredient
    )
    substitute_result = substitute_result_raw.json()
    if "status" not in substitute_result.keys():
        messagebox.showerror(
            "API connection problem!", "Check your API host and/or key information"
        )
    elif substitute_result["status"] == "success":
        label = tk.Label(third_frame, text="The ingredient can be substituted with:")
        label.grid(row=3, column=0)
        row_number_3rd = 4
        for item in substitute_result["substitutes"]:
            result_label = tk.Label(third_frame, text="* " + item)
            result_label.grid(row=row_number_3rd, column=0)
            row_number_3rd += 1
    else:
        result_label = tk.Label(third_frame, text="No results")
        result_label.grid(row=3, column=0)
        third_frame.after(5000, result_label.destroy)


substitute_button = tk.Button(third_frame, text="Find substitute", command=find_substitute)
substitute_button.grid(row=2, column=0, columnspan=2, pady=3)

root.mainloop()
