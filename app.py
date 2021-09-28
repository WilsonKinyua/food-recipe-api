from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.secret_key = "mkuu"
api = Api(app)


# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://developer:developerwilson@localhost/recipe_app'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)


from models import Recipe,Ingredient

# recipe resource
class SingleRecipe(Resource):
    def get(self, node_id):
        recipe = Recipe.query.filter_by(node_id=node_id).first()
        if recipe:
            return recipe.to_json()
        else:
            return {"message": "Recipe not found"}, 404

    # update method to update a recipe
    def put(self, node_id):
        data = request.get_json()
        recipe = Recipe.query.filter_by(node_id=node_id).first()
        if recipe:
            recipe.name = data["name"]
            recipe.description = data["description"]
            recipe.instructions = data["instructions"]
            recipe.cook_time = data["cook_time"]
            recipe.imageUrl = data["imageUrl"]
            recipe.originalUrl = data["originalUrl"]
            db.session.commit()
            return recipe.to_json()
        else:
            return {"message": "Recipe not found"}, 404

    # delete method to delete a recipe
    def delete(self, node_id):
        recipe = Recipe.query.filter_by(node_id=node_id).first()
        if recipe:
            db.session.delete(recipe)
            db.session.commit()
            return {"message": "Recipe deleted"}
        else:
            return {"message": "Recipe not found"}, 404
    


class RecipeList(Resource):
    # get all recipes
    def get(self):
        return {"recipes": [recipe.to_json() for recipe in Recipe.get_all()]}
        # post method to add recipe to database
    def post(self):
        data = request.get_json()
        print(data)
        recipe = Recipe(
            # node_id = uuid.uuid4().hex[:6],
            name=data["name"],
            description=data["description"],
            instructions=data["instructions"],
            cook_time=data["cook_time"],
            imageUrl=data["imageUrl"],
            originalUrl=data["originalUrl"]
        )
        print(recipe)
        db.session.add(recipe)
        db.session.commit()
        return recipe.to_json()



# Ingredients resource
class SingleIngredient(Resource):
    def get(self, node_id):
        ingredient = Ingredient.query.filter_by(node_id=node_id).first()
        if ingredient:
            return ingredient.to_json()
        else:
            return {"message": "Ingredient not found"}, 404


    # # update method to update an ingredient
    def put(self, node_id):
        data = request.get_json()
        ingredient = Ingredient.query.filter_by(node_id=node_id).first()
        if ingredient:
            ingredient.name = data["name"]
            ingredient.quantity = data["quantity"]
            ingredient.unit = data["unit"]
            db.session.commit()
            return ingredient.to_json()
        else:
            return {"message": "Ingredient not found"}, 404

    # # delete method to delete an ingredient
    def delete(self, node_id):
        ingredient = Ingredient.query.filter_by(node_id=node_id).first()
        if ingredient:
            db.session.delete(ingredient)
            db.session.commit()
            return {"message": "Ingredient deleted"}
        else:
            return {"message": "Ingredient not found"}, 404


class IngredientsList(Resource):
    def get(self):
        return {"ingredients": [ingredient.to_json() for ingredient in Ingredient.get_all()]}
        # post method to add ingredient to database
    def post(self):
        data = request.get_json()
        ingredient = Ingredient(
            recipe_id = data["recipe_id"],
            name=data["name"],
            quantity=data["quantity"],
            unit=data["unit"]
        )
        print(ingredient)
        db.session.add(ingredient)
        db.session.commit()
        return ingredient.to_json()


# get all ingredients for a recipe by recipe_id 
class RecipeIngredients(Resource):
    def get(self, recipe_id):
        return {"ingredients": [ingredient.to_json() for ingredient in Ingredient.get_by_recipe_id(recipe_id)]}


# set the route and accepted methods


# recipe endpoints
api.add_resource(RecipeList, "/recipes")
api.add_resource(SingleRecipe, "/recipe")

# ingredient endpoints
api.add_resource(IngredientsList, "/ingredients")
api.add_resource(SingleIngredient, "/ingredient")

# get all ingredients for a recipe by recipe_id
api.add_resource(RecipeIngredients, "/recipe/<recipe_id>/ingredients")
if __name__ == "__main__":
    app.run(debug=True)
