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


from models import Recipe

class SingleRecipe(Resource):
    def get(self, node_id):
        recipe = Recipe.query.filter_by(node_id=node_id).first()
        if recipe:
            return recipe.to_json()
        else:
            return {"message": "Recipe not found"}, 404

    # post method to add recipe to database
    def post(self):
        data = request.get_json()
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


class RecipeList(Resource):
    # get all recipes
    def get(self):
        return {"recipes": [recipe.to_json() for recipe in Recipe.get_all()]}

# set the route and accepted methods
api.add_resource(RecipeList, "/recipes")
api.add_resource(SingleRecipe, "/recipe")
if __name__ == "__main__":
    app.run(debug=True)
