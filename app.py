
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
app = Flask(__name__)
app.secret_key = "mkuu"
api = Api(app)


app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)
from models import Recipe






class RecipeList(Resource):
    # get all recipes
    def get(self):
        return {"recipes": [recipe.json() for recipe in Recipe.query.all()]}




# set the route and accepted methods
api.add_resource(RecipeList, "/recipes")

if __name__ == "__main__":
    app.run(debug=True)
