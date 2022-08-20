from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from playlist_timemachine import PlaylistForm, PlaylistTimemachine
from recipe_finder import RecipeSearchForm, GetRecipeList
from dotenv import load_dotenv
import os
import json
import requests
import logging

load_dotenv(".env")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
FLASK_KEY = os.getenv("FLASK_KEY")

# Setup flask app
app = Flask(__name__)
Bootstrap(app)
app.secret_key = FLASK_KEY

# Global variables
recipe_string = ""

@app.route("/")
def home():
    app.logger.info("BITCHING")
    return render_template("index.html")


@app.route("/playlist-timemachine", methods=["POST", "GET"])
def playlist_time():
    date_form = PlaylistForm(day="Date")
    if request.method == "POST":
        day_date = date_form.day.data
        month_date = date_form.month.data
        year_date = date_form.year.data
        playlist = PlaylistTimemachine(year=year_date, month=month_date, day=day_date)
        return render_template("playlist-timemachine.html", form=date_form, playlist=playlist.playlist_id)
    return render_template("playlist-timemachine.html", form=date_form, playlist=None)


@app.route("/recipe-finder", methods=["POST", "GET"])
def recipe_finder():
    recipe_form = RecipeSearchForm()
    if request.method == "POST":
        diet = recipe_form.diet.data
        allergies = recipe_form.allergies.data
        meal_type = recipe_form.meal_type.data
        response = GetRecipeList(diet=diet, ingredients=recipe_string, allergies=allergies, meal_type=meal_type).response
        food_results = response.json()['results']
        if food_results == "":
            return render_template("recipe-finder.html", form=recipe_form, results="no entries")
        else:
            return render_template("recipe-finder.html", form=recipe_form, results=food_results)
    return render_template("recipe-finder.html", form=recipe_form, results=None)


@app.route("/process-user-info/<string:ingredients_string>", methods=["POST"])
def process_user_info(ingredients_string):
    global recipe_string
    recipe_string = json.loads(ingredients_string)
    return ('/')


@app.route("/recipe/<int:id>", methods=["POST", "GET"])
def show_recipe(id):
    header = {
        "x-api-key": "26f190d703b14b4e9c5ed10eefe137d7",
    }
    recipe_response = requests.get(f"https://api.spoonacular.com/recipes/{id}/information", headers=header)
    recipe = recipe_response.json()
    instructions_response = requests.get(f"https://api.spoonacular.com/recipes/{id}/analyzedInstructions",
                                         headers=header)
    instructions = instructions_response.json()
    return render_template("recipe.html", recipe=recipe, instructions=instructions)


if __name__ == "__main__":
    app.run(debug=True)
    gunicorn_logger = logging.getLogger('TEST TEST TEST')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
