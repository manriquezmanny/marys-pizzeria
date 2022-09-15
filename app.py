from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os


# Creating Flask app.
app = Flask(__name__)


# Getting and setting secret key and ensuring it isn't pushed to github by using dotenv and .gitignore
load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# Adding Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///maryspizza.db"
# Initializing Database
db = SQLAlchemy(app)


# Creating Database Models (i.e tables using sqlalchemy)
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    #Creating a dunder repr function to return a string if the class is printed or returned.
    def __repr__(self):
        return "<Email %r>" % self.email

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    email = db.Column(db.String(80), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    #Creating dunder repr function for Orders
    def __repr__(self):
        return "<Order at: %r>" % self.date_time


# Creating Form Classes using wtforms
class RegisterForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    confirmation = PasswordField("Confirm Password:", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    submit = SubmitField("Login")

class AddToOrder(FlaskForm):
    submit = SubmitField("Add to order")


# Creating a global menu to dynamically update menu template with jinja and get useful information.
MENU = {"pepperonicheese": {"small":8.00, "medium":12.00, "large":13.50, "text": "Pepperoni Pizza", "description": "Mary's take at the staple pepperoni and pizza favorite! Experience this perfectly seasoned masterpiece for yourself!"},
        "breakfastpizza": {"small":7.50, "medium":11.50, "large":14.00, "text": "Breakfast Pizza", "description": "It's always breakfast time when you're hungry! Try out this delicious breakfast pizza with hardboiled egg slices as a topping!"},
        "vegetarianpizza": {"small":9.00, "medium":13.00, "large":16.00, "text": "Vegetarian Pizza", "description": "No menu would be complete without a delicious vegetarian meal! Try this carefully crafted recepie today!"},
        "combopizza": {"small":8.50, "medium":12.50, "large":15.50, "text": "Combo Veggie Pizza", "description": "Need a little bit of everything? This combo pizza will surely satisfy any and all cravings! No meat and no compromises!"}
}

# Creating a Global dictionary that will be used to add items to order as dicts and then push the data to transactions database.
ORDER = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    order = AddToOrder()
    return render_template("menu.html", MENU=MENU, order=order)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    register = RegisterForm()
    return render_template("register.html", register=register)


@app.route("/login", methods=["GET", "POST"])
def login():
    login = LoginForm()
    return render_template("login.html", login=login)


@app.route("/rewards")
def rewards():
    return render_template("rewards.html")