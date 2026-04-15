from flask import Flask, render_template, request
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
    
@app.route("/add", methods=["POST"])
def add():
    recipe = Recipe(
        name = request.form["name"],
        ingredients = request.form["ingredients"],
        instructions = request.form["instructions"],
        time = request.form["time"]
        )
        
    db.session.add(recipe)
    db.session.commit()
    return "Added"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

