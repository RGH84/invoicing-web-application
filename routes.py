from db import db
from app import app
import visits
from flask import redirect, render_template, request, session
import users
import customers

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
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/login")
        return render_template("error.html", message="Rekisteröinti ei onnistunut, kokeile eri käyttäjkätunnusta.")
        
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
        #tähän väliin errorit ja ehdot..
        if customers.new_customer(customer_name, address, phonenumber, business_id, user_id):
            return render_template("approve.html", message="Asiakkan luonti onnistui.")
        return render_template("error.html", message="Asiakkan luonti ei onnistunut")
        #Lisää paluu etusivulle/uusi asiakas nappi

@app.route("/customer_register")
def customer_register():
    customers_table = customers.customer_register()
    return render_template("/customer_register.html", count=len(customers_table), customers_register=customers_table)



