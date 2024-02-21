from db import db
from app import app
import visits
from flask import redirect, render_template, request, session
import users
import customers
import products
import invoices
from datetime import datetime

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        usernames = users.usernames()
        return render_template("login.html", usernames=usernames)
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
        usernames = users.usernames()
        return render_template("register.html", usernames=usernames)
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

@app.route("/remove_customer", methods=["GET", "POST"])
def remove_customer():
    if request.method == "GET":
        user_id = users.user_id()
        customers_id = customers.customers_id(user_id)
        return render_template("remove_customer.html", customers_id=customers_id)
    if request.method == "POST":
        id = int(request.form["ID"])
        user_id = users.user_id()
        customers_id = customers.customers_id(user_id)
        if id in customers_id and customers.remove_customer(id):
                return render_template("remove_customer.html", customers_id=customers_id)
        return render_template("error.html", message="Asiakkaan poisto ei onnistunut, tarkista ID.")

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

@app.route("/remove_product", methods=["GET", "POST"])
def remove_product():
    if request.method == "GET":
        user_id = users.user_id()
        products_id = products.products_id(user_id)
        return render_template("remove_product.html", products_id=products_id)
    if request.method == "POST":
        id = int(request.form["ID"])
        user_id = users.user_id()
        products_id = products.products_id(user_id)
        if id in products_id and products.remove_product(id):
            return render_template("remove_product.html", products_id=products_id)
        return render_template("error.html", message="Tuotteen poistaminen ei onnistunut")
     
@app.route("/new_invoice", methods=["GET", "POST"])
def new_invoice():
    if request.method == "GET":
        return render_template("/new_invoice.html")
    if request.method == "POST":
        create_time = datetime.now()
        form_time = create_time.strftime("%d-%m-%Y %H:%M:%S")
        user_id = users.user_id()
        biller_id = int(request.form["biller_ID"])
        biller_info = customers.info(biller_id, user_id)
        customer_id = int(request.form["customer_ID"])
        customer_info = customers.info(customer_id, user_id)
        invoice_number = request.form["invoice_number"]
        product_one_id = int(request.form["product_1"])
        product_two_id = int(request.form["product_2"])
        product_three_id = int(request.form["product_3"])
        product_four_id = int(request.form["product_4"])
        product_five_id = int(request.form["product_5"])
        product_one_info = products.info(product_one_id, user_id)
        product_two_info = products.info(product_two_id, user_id)
        product_three_info = products.info(product_three_id, user_id)
        product_four_info = products.info(product_four_id, user_id)
        product_five_info = products.info(product_five_id, user_id)
        no_margin_sum = int(product_one_info[0][3]) + int(product_two_info[0][3]) + int(product_three_info[0][3]) + int(product_four_info[0][3]) + int(product_five_info[0][3])
        margin = int(request.form["margin"])
        sum = no_margin_sum * (margin / 100 + 1) 
        if invoices.new_invoice(biller_id, customer_id, form_time, invoice_number, product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum, user_id):
            return render_template("/invoice.html", biller_info=biller_info, customer_info=customer_info, invoice_number=invoice_number, product_one_info=product_one_info, product_two_info=product_two_info, product_three_info=product_three_info, product_four_info=product_four_info, product_five_info=product_five_info, sum=sum, margin=margin, no_margin_sum=no_margin_sum, form_time=form_time)
        return render_template("error.html", message="Laskun luonti ei onnistunut.")

@app.route("/invoice_archive", methods=["GET", "POST"])
def invoice_archive():
    if request.method == "GET":
        user_id = users.user_id()
        invoices_table = invoices.invoice_archive(user_id)
        invoice_numbers = invoices.numbers(user_id)
        return render_template("/invoice_archive.html", count=len(invoices_table), invoice_archive=invoices_table, invoice_numbers=invoice_numbers)
    if request.method == "POST":
        user_id = users.user_id()
        invoices_table = invoices.invoice_archive(user_id)
        invoice_number = request.form["invoice_number"]
        invoice_numbers = invoices.numbers(user_id)
        if invoice_number not in invoice_numbers:
            return render_template("error.html", message="Tarkista laskun numero.")
        invoice_info = invoices.info(invoice_number, user_id)
        biller_id = invoice_info[0][2]
        biller_info = customers.info(biller_id, user_id)
        customer_id = invoice_info[0][3]
        customer_info = customers.info(customer_id, user_id)
        product_one_id = invoice_info[0][4]
        product_two_id = invoice_info[0][5]
        product_three_id = invoice_info[0][6]
        product_four_id = invoice_info[0][7]
        product_five_id = invoice_info[0][8]
        product_one_info = products.info(product_one_id, user_id)
        product_two_info = products.info(product_two_id, user_id)
        product_three_info = products.info(product_three_id, user_id)
        product_four_info = products.info(product_four_id, user_id)
        product_five_info = products.info(product_five_id, user_id)
        no_margin_sum = invoice_info[0][9]
        margin = margin=invoice_info[0][10]
        sum = sum=invoice_info[0][11]
        form_time=invoice_info[0][1]
        return render_template("/invoice.html", biller_info=biller_info, customer_info=customer_info, invoice_number=invoice_number, product_one_info=product_one_info, product_two_info=product_two_info, product_three_info=product_three_info, product_four_info=product_four_info, product_five_info=product_five_info, sum=sum, margin=margin, no_margin_sum=no_margin_sum, form_time=form_time, invoice_numbers=invoice_numbers)
    
@app.route("/to_do_list")
def to_do_list():
    return render_template("/to_do_list.html")

@app.route("/sent_message")
def sent_message():
    return render_template("/sent_message.html")




