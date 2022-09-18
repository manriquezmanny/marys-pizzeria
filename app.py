from flask import Flask, render_template, request, flash, redirect, url_for
import copy
import os


# Creating Flask app.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


# Creating Global variables to keep track of order items, prices and to give each item in order an item_number.
MENU = {"pepperonicheese": {"price":8.00, "text": "Pepperoni Pizza $8.00", "description": "Mary's take at the staple pepperoni and pizza favorite! Experience this perfectly seasoned masterpiece for yourself!"},
        "breakfastpizza": {"price":7.50, "text": "Breakfast Pizza $7.50", "description": "It's always breakfast time when you're hungry! Try out this delicious breakfast pizza with hardboiled egg slices as a topping!"},
        "vegetarianpizza": {"price":9.00, "text": "Vegetarian Pizza $9.00", "description": "No menu would be complete without a delicious vegetarian meal! Try this carefully crafted recepie today!"},
        "combopizza": {"price":8.50, "text": "Combo Veggie Pizza $8.50", "description": "Need a little bit of everything? This combo pizza will surely satisfy any and all cravings! No meat and no compromises!"}
}

ORDER = []
total_price = 0.0
item_number = 1


# Making a function I will use to remove items from order!
def remove(item_id):
    global total_price
    order_copy = copy.copy(ORDER)
    for i in range(len(order_copy)):
        if order_copy[i][3] == item_id:
            total_price -= float(ORDER[i][2])
            ORDER.remove(ORDER[i])


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