# Recipe-Search

Recipe-Search is a Python3 desktop application with a Tkinter GUI for searching, browsing, and viewing food recipes using the Spoonacular API.

## Features

- Search for recipes by ingredients, cuisine, diet, and meal type
- Browse recipe details including ingredients, instructions, and images
- View ingredient substitutes when searching for alternatives
- Use a visual GUI with filters and an image viewer

## Installation

1. Clone the repository.
2. Install Python 3 if needed.
3. Run the setup script:

```bash
./setup.sh
```

4. Alternatively, install dependencies manually:

```bash
python3 -m pip install -r requirements.txt
```

## Configuration

The app requires Spoonacular API credentials.

1. Subscribe to Spoonacular on RapidAPI.
2. Add your API key and host to the configuration fields in the GUI when the app starts.

## Usage

Run the application from the repository root:

```bash
python3 src/main.py
```

Then:

- enter your Spoonacular API credentials
- choose filters and search options
- select a recipe from the results list
- view ingredients, instructions, and images
- use the substitution search field to find ingredient alternatives

## License

This project is licensed under the terms described in the `LICENSE` file.
