import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class RecipeSearchForm(FlaskForm):
    diet = SelectField('Veggie/Vegan', choices=["None", "Vegetarian", "Vegan", "Pescetarian"])
    allergies = SelectField('Allergies', choices=["None", "Dairy", "Gluten", "Peanut", "Seafood"])
    meal_type = SelectField('Meal Type', choices=["None", "Main Course", "Dessert", "Appetizer", "Salad", "Breakfast",
                                                  "Bread", "Snack"])
    ingredients = StringField('Ingredients')
    ingredients_list = TextAreaField()
    submit = SubmitField('Add Ingredient', validators=[DataRequired()])
    send = SubmitField('Get recipes!')


class GetRecipeList():
    def __init__(self, ingredients, diet, allergies, meal_type):
        # Params and headers for spoonacular API
        header = {
            "x-api-key": "26f190d703b14b4e9c5ed10eefe137d7"
        }
        params = {
            "instructionsRequired": "true",
        }

        if ingredients != None:
            params["includeIngredients"] = ingredients
        if diet != "None":
            params["diet"] = diet
        if allergies != "None":
            params["intolerances"] = allergies
        if meal_type != "None":
            params["type"] = meal_type
        self.response = requests.get("https://api.spoonacular.com/recipes/complexSearch",
                                     params=params,
                                     headers=header)
