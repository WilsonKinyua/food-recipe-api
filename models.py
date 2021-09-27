from api import db
from datetime import datetime


# Model for the table 'Recipe'
class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    imageUrl = db.Column(db.String(100), nullable=False)
    originalUrl = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, name, description, ingredients, instructions,
                 cook_time, imageUrl, originalUrl):
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.cook_time = cook_time
        self.imageUrl = imageUrl
        self.originalUrl = originalUrl

    # Method to return the recipe as a json
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'cook_time': self.cook_time,
            'imageUrl': self.imageUrl,
            'originalUrl': self.originalUrl,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    # Method to get a single recipe by id
    @staticmethod
    def get_by_id(id):
        return Recipe.query.filter_by(id=id).first()

    # Method to get all recipes
    @staticmethod
    def get_all():
        return Recipe.query.all()

    # Method to add a new recipe
    def add(self):
        db.session.add(self)
        db.session.commit()

    # Method to update a recipe
    def update(self):
        db.session.commit()

    # Method to delete a recipe
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Recipe %r>' % self.name
