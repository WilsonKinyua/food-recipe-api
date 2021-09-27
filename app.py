from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "mkuu"
api = Api(app)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://developer:developerwilson@localhost/recipe_app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

from models import Recipe

if __name__ == "__main__":
    app.run(debug=True)
