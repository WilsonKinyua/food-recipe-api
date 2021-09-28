from app import db as db
import uuid

# Model for the table 'Recipe'


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)
    cook_time = db.Column(db.String(255), nullable=False)
    imageUrl = db.Column(db.String(100), nullable=False)
    originalUrl = db.Column(db.String(255), nullable=False)

    def __init__(self, name, description, instructions,
                 cook_time, imageUrl, originalUrl):
        self.node_id = uuid.uuid4().hex[:20]
        self.name = name
        self.description = description
        self.instructions = instructions
        self.cook_time = cook_time
        self.imageUrl = imageUrl
        self.originalUrl = originalUrl

    # Method to return the recipe as a json
    def to_json(self):
        return {
            # 'id': self.id,
            "node_id": self.node_id,
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions,
            'cook_time': self.cook_time,
            'imageUrl': self.imageUrl,
            'originalUrl': self.originalUrl
        }
    # Base.query = session.query_property()
    # Method to get a single recipe by id

    @staticmethod
    def get_by_id(node_id):
        return Recipe.query.filter_by(node_id=node_id).first()

    # Method to get all recipes
    @staticmethod
    def get_all():
        return Recipe.query.all()

    # Method to update a recipe
    def update(self):
        db.session.commit()

    # Method to delete a recipe
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Recipe %r>' % self.name


# Model for the table 'Ingredient'
class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(100), nullable=False)

    def __init__(self, name, quantity, unit, recipe_id):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.recipe_id = recipe_id

    # Method to return the ingredient as a json
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'recipe_id': self.recipe_id,
        }

    # Method to get a single ingredient by id
    @staticmethod
    def get_by_id(id):
        return Ingredient.query.filter_by(id=id).first()

    # Method to get all ingredients
    @staticmethod
    def get_all():
        return Ingredient.query.all()

    # Method to update an ingredient
    def update(self):
        db.session.commit()

    # Method to delete an ingredient
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Ingredient %r>' % self.name
