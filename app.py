from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import copy
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

# Creating a global menu to dynamically update menu template with jinja and get useful information.
MENU = {"pepperonicheese": {"price":8.00, "text": "Pepperoni Pizza $8.00", "description": "Mary's take at the staple pepperoni and pizza favorite! Experience this perfectly seasoned masterpiece for yourself!"},
        "breakfastpizza": {"price":7.50, "text": "Breakfast Pizza $7.50", "description": "It's always breakfast time when you're hungry! Try out this delicious breakfast pizza with hardboiled egg slices as a topping!"},
        "vegetarianpizza": {"price":9.00, "text": "Vegetarian Pizza $9.00", "description": "No menu would be complete without a delicious vegetarian meal! Try this carefully crafted recepie today!"},
        "combopizza": {"price":8.50, "text": "Combo Veggie Pizza $8.50", "description": "Need a little bit of everything? This combo pizza will surely satisfy any and all cravings! No meat and no compromises!"}
}

# Creating a Global dictionary that will be used to add items to order as dicts and then push the data to transactions database.
ORDER = []
total_price = 0.0
item_number = 1



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu", methods=["GET", "POST"])
def menu():
    if request.method == "GET":
        return render_template("menu.html", MENU=MENU)
    else:
        for item in MENU:
            if request.form.get(item):
                size = request.form[item+"size"]
                if size == "NONE":
                    flash("Please Select Pizza Size!")
                    return redirect(url_for("menu"))
                else:
                    ORDER.append([item, size, str(MENU[item]["price"])])
                    flash(f"Succesfully added a {size.title()} {MENU[item]['text'][:-6]} to order, click Checkout on top right when ready!")
        return redirect(url_for("menu"))


def remove(item_id):
    global total_price
    order_copy = copy.copy(ORDER)
    for i in range(len(order_copy)):
        if order_copy[i][3] == item_id:
            total_price -= float(ORDER[i][2])
            ORDER.remove(ORDER[i])


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    global total_price
    global item_number
    if request.method == "GET":
        for item in ORDER:
            if item[1] == "medium":
                item[2] = float(item[2]) + 2.00
                item[1] = item[1].title()
                total_price += item[2]
                item[2] = str(item[2])
                item.append(item_number)
                item_number += 1
            elif item[1] == "large":
                item[2] = float(item[2]) + 4.00
                item[1] = item[1].title()
                total_price += item[2]
                item[2] = str(item[2])
                item.append(item_number)
                item_number += 1
            elif item[1] == "small":
                item[1] = item[1].title()
                item[2] = float(item[2])
                total_price += float(item[2])
                item[2] = str(item[2])
                item.append(item_number)
                item_number += 1
        return render_template("checkout.html", ORDER=ORDER, MENU=MENU, TOTAL="$"+str(total_price)+"0")
    else:
        item_id = int(request.form.get("item_id"))
        print(ORDER)
        remove(item_id)
        print(ORDER)
        return redirect(url_for("checkout"))



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