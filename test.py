from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session


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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        new_name = request.form["name"]
        new_password = request.form["password"]

        if len(new_password) < 8:
            return "Password length has to be at least 8 characters"
        
        existing_user = User.query.filter_by(username=new_name).first()
        if existing_user:
            return "Username already exists"

        new_user = User(
            username=new_name,
            password_hash=generate_password_hash(new_password)
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect("/login")

    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            return redirect(url_for("index", username=user.username))
        else:
            return "Invalid username or password"

    return render_template("login.html")


@app.route("/delete/<int:id>", methods=["POST"])
def delete_recipe(id):
    recipe_to_delete = Recipe.query.get(id)

    if recipe_to_delete is None:
        return "Recipe not found"

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
        time = int(request.form["time"]),
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

