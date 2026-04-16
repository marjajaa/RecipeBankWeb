from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./recipes.db'
db = SQLAlchemy(app)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    instructions = db.Column(db.String(200), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Recipe {self.name}>"
    
@app.route("/delete/<int:id>", methods=["POST"])
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get(id)

    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "Error deleting recipe"

    
@app.route("/add", methods=["POST"])
def add_recipe():
    recipe = Recipe(
        name = request.form["name"],
        ingredients = request.form["ingredients"],
        instructions = request.form["instructions"],
        time = int(request.form["time"])
        )
        
    db.session.add(recipe)
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>")
def edit_recipe(id):
    recipe = Recipe.query.get(id)
    return render_template("edit.html", recipe=recipe)

@app.route("/update/<int:id>", methods=["POST"])
def update_recipe(id):
    recipe = Recipe.query.get(id)

    recipe.name = request.form["name"]
    recipe.ingredients = request.form["ingredients"]
    recipe.instructions = request.form["instructions"]
    recipe.time = int(request.form["time"])

    db.session.commit()
    return redirect("/")

@app.route("/", methods=["GET"])
def index():
    recipes = Recipe.query.all()
    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

