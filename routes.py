from db import db
from app import app
import visits
from flask import redirect, render_template, request, session
import users
import customers
import products

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(password1) > 20 or len(username) > 20:
            return render_template("error.html", message="Liian pitkä tunnus tai salasana. Max 20 kirjainta.")
        if len(password1) < 4 or len(username) < 4:
            return render_template("error.html", message="Liian lyhyt tunnus tai salasana. Min 4 kirjainta.")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/login")
        return render_template("error.html", message="Rekisteröinti ei onnistunut, kokeile eri käyttäjätunnusta.")
        
@app.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "GET":
        return render_template("/new_customer.html")
    if request.method == "POST":
        user_id = users.user_id()
        customer_name = request.form["customer_name"]
        address = request.form["address"]
        phonenumber = request.form["phonenumber"]
        business_id = request.form["business_id"]
        if len(customer_name) > 20 or len(address) > 20 or len(phonenumber) > 20 or len(business_id) > 20:
            return render_template("error.html", message="Joku kentistä on liian pitkä. Max 20 kirjainta")
        if len(customer_name) < 1 or len(address) < 1 or len(phonenumber) < 1 or len(business_id) < 1:
            return render_template("error.html", message="Joku kentistä puuttuu. Min 1 kirjain")
        if customers.new_customer(customer_name, address, phonenumber, business_id, user_id):
            return render_template("approve.html", message="Asiakkan luonti onnistui.")
        return render_template("error.html", message="Asiakkan luonti ei onnistunut")
        
@app.route("/customer_register")
def customer_register():
    user_id = users.user_id()
    customers_table = customers.customer_register(user_id)
    return render_template("/customer_register.html", count=len(customers_table), customers_register=customers_table)

@app.route("/new_product", methods=["GET", "POST"])
def new_product():
    if request.method == "GET":
        return render_template("/new_product.html")
    if request.method == "POST":
        user_id = users.user_id()
        product_name = request.form["product_name"]
        type = request.form["type"]
        product_number = request.form["product_number"]
        price = request.form["price"]
        if len(product_name) > 20 or len(type) > 20 or len(product_number) > 20 or len(price) > 20:
            return render_template("error.html", message="Joku kentistä on liian pitkä. Max 20 kirjainta")
        if len(product_name) < 1 or len(type) < 1 or len(product_number) < 1 or len(price) < 1:
            return render_template("error.html", message="Joku kentistä puuttuu. Min 1 kirjain")
        if products.new_product(product_name, type, product_number, price, user_id):
            return render_template("approve.html", message="Tuotteen luonti onnistui.")
        return render_template("error.html", message="Tuotteen luonti ei onnistunut")
    
@app.route("/product_register")
def product_register():
    user_id = users.user_id()
    products_table = products.product_register(user_id)
    return render_template("/product_register.html", count=len(products_table), products_register=products_table)

@app.route("/remove_customer", methods=["GET", "POST"])
def remove_customer():
    if request.method == "GET":
        return render_template("remove_customer.html")
    if request.method == "POST":
        id = request.form["ID"]
        user_id = users.user_id()
        customers_id = customers.customers_id(user_id)
        if id not in customers_id:
            return render_template("error.html", message="Asiakkaan poisto ei onnistunut, tarkista ID.")
        if customers.remove_customer(id):
            return render_template("approve.html", message="Asiakkaan poisto onnistui.")
        return render_template("error.html", message="Asiakkaan poisto ei onnistunut, tarkista ID.")
        
@app.route("/new_invoice")
def new_invoice():
    return render_template("/new_invoice.html")

@app.route("/invoice_archive")
def invoice_archive():
    return render_template("/invoice_archive.html")

@app.route("/to_do_list")
def to_do_list():
    return render_template("/to_do_list.html")

@app.route("/sent_message")
def sent_message():
    return render_template("/sent_message.html")




