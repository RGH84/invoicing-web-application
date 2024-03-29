import secrets
from datetime import datetime
from flask import redirect, url_for, render_template, request, session, abort
from app import app
import visits
import users
import customers
import products
import invoices
import messages
import to_do

@app.route("/")
def index():
    visits.add_visit()
    counter = visits.get_counter()
    return render_template("index.html", counter=counter)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        usernames = users.usernames()
        return render_template("login.html", usernames=usernames, csrf_token=session["csrf_token"])
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        return render_template("error.html", message="Väärä tunnus tai salasana.")
    return None

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        session["csrf_token"] = secrets.token_hex(16)
        usernames = users.usernames()
        return render_template("register.html", usernames=usernames,
                                csrf_token=session["csrf_token"])
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if is_field_too_long(password1, username) or is_too_short(password1, username):
            return render_template("error.html",
                                    message="Tarkista syötteiden pituudet.")
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/login")
        return render_template("error.html",
                                message="Rekisteröinti ei onnistunut, kokeile eri käyttäjätunnusta")
    return None

@app.route("/new_customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "GET":
        return render_template("/new_customer.html", csrf_token=session["csrf_token"])
    if request.method == "POST":
        user_id = users.user_id()
        customer_name = request.form["customer_name"]
        address = request.form["address"]
        phonenumber = request.form["phonenumber"]
        business_id = request.form["business_id"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if is_field_too_long(customer_name, address, phonenumber, business_id):
            return render_template("error.html", message="Syöte on liian pitkä. Max 20 kirjainta.")
        if is_field_missing(customer_name, address, phonenumber, business_id):
            return render_template("error.html", message="Joku kentistä puuttuu. Min 1 kirjain.")
        if customers.new_customer(customer_name, address, phonenumber, business_id, user_id):
            return render_template("/new_customer.html", csrf_token=session["csrf_token"])
        return render_template("error.html", message="Asiakkaan luonti ei onnistunut.")
    return None

@app.route("/customer_register")
def customer_register():
    user_id = users.user_id()
    customers_table = customers.customer_register(user_id)
    return render_template("/customer_register.html",
                            count=len(customers_table), customers_register=customers_table)

@app.route("/remove_customer", methods=["GET", "POST"])
def remove_customer():
    if request.method == "GET":
        user_id = users.user_id()
        customers_id = customers.customers_id(user_id)
        return render_template("remove_customer.html",
                               customers_id=customers_id, csrf_token=session["csrf_token"])
    if request.method == "POST":
        if not request.form.get("ID"):
            return render_template("error.html", message="ID-kenttä ei saa olla tyhjä.")
        customer_id = int(request.form["ID"])
        user_id = users.user_id()
        customers_id = customers.customers_id(user_id)
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if customer_id in customers_id and customers.remove_customer(customer_id):
            return render_template("remove_customer.html",
                                    customers_id=customers_id, csrf_token=session["csrf_token"])
        return render_template("error.html", message="Asiakkaan poisto ei onnistunut, tarkista ID.")
    return None

@app.route("/new_product", methods=["GET", "POST"])
def new_product():
    if request.method == "GET":
        return render_template("/new_product.html", csrf_token=session["csrf_token"])
    if request.method == "POST":
        user_id = users.user_id()
        product_name = request.form["product_name"]
        product_type = request.form["type"]
        product_number = request.form["product_number"]
        price = request.form["price"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if is_field_too_long(product_name, product_type, product_number, price):
            return render_template("error.html",
                                   message="Joku kentistä on liian pitkä. Max 20 kirjainta.")
        if is_field_missing(product_name, product_type, product_number, price):
            return render_template("error.html", message="Joku kentistä puuttuu. Min 1 kirjain.")
        if products.new_product(product_name, product_type, product_number, price, user_id):
            return render_template("/new_product.html", csrf_token=session["csrf_token"])
        return render_template("error.html", message="Tuotteen luonti ei onnistunut.")
    return None

@app.route("/product_register")
def product_register():
    user_id = users.user_id()
    products_table = products.product_register(user_id)
    return render_template("/product_register.html",
        count=len(products_table), products_register=products_table)

@app.route("/remove_product", methods=["GET", "POST"])
def remove_product():
    if request.method == "GET":
        user_id = users.user_id()
        products_id = products.products_id(user_id)
        return render_template("remove_product.html",
                                products_id=products_id, csrf_token=session["csrf_token"])
    if request.method == "POST":
        if not request.form.get("ID"):
            return render_template("error.html", message="ID-kenttä ei saa olla tyhjä.")
        product_id = int(request.form["ID"])
        user_id = users.user_id()
        products_id = products.products_id(user_id)
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if product_id in products_id and products.remove_product(product_id):
            return render_template("remove_product.html",
                                    products_id=products_id, csrf_token=session["csrf_token"])
        return render_template("error.html", message="Tuotteen poistaminen ei onnistunut.")
    return None

@app.route("/new_invoice", methods=["GET", "POST"])
def new_invoice():
    if request.method == "GET":
        user_id = users.user_id()
        products_id = products.products_id(user_id)
        customers_id = customers.customers_id(user_id)
        invoice_numbers = invoices.numbers(user_id)
        return render_template("/new_invoice.html",
                                products_id=products_id, customers_id=customers_id,
                                invoice_numbers=invoice_numbers, csrf_token=session["csrf_token"])
    if request.method == "POST":
        required_fields = [
            "biller_ID", "customer_ID", "invoice_number", "product_1", "product_2",
            "product_3", "product_4", "product_5", "margin"
        ]
        for field in required_fields:
            if not request.form.get(field):
                return render_template("error.html", message="Mikään kenttä ei saa olla tyhjä.")
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
        no_margin_sum = (
            int(product_one_info[0][3]) +
            int(product_two_info[0][3]) +
            int(product_three_info[0][3]) +
            int(product_four_info[0][3]) +
            int(product_five_info[0][3])
            )
        margin = int(request.form["margin"])
        total_sum = no_margin_sum * (margin / 100 + 1)
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if invoices.new_invoice(
            biller_id, customer_id, form_time, invoice_number,
            product_one_id, product_two_id, product_three_id,
            product_four_id, product_five_id, no_margin_sum,
            margin, total_sum, user_id
            ):
            return render_template(
                "/invoice.html",
                biller_info=biller_info,
                customer_info=customer_info,
                invoice_number=invoice_number,
                product_one_info=product_one_info,
                product_two_info=product_two_info,
                product_three_info=product_three_info,
                product_four_info=product_four_info,
                product_five_info=product_five_info,
                sum=total_sum,
                margin=margin,
                no_margin_sum=no_margin_sum,
                form_time=form_time)
        return render_template("error.html", message="Laskun luonti ei onnistunut.")
    return None

@app.route("/invoice_archive", methods=["GET", "POST"])
def invoice_archive():
    if request.method == "GET":
        user_id = users.user_id()
        invoices_table = invoices.invoice_archive(user_id)
        invoice_numbers = invoices.numbers(user_id)
        return render_template("/invoice_archive.html",
            count=len(invoices_table),
            invoice_archive=invoices_table,
            invoice_numbers=invoice_numbers,
            csrf_token=session["csrf_token"])
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
        total_sum = invoice_info[0][11]
        form_time=invoice_info[0][1]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        return render_template(
                "/invoice.html",
                biller_info=biller_info,
                customer_info=customer_info,
                invoice_number=invoice_number,
                product_one_info=product_one_info,
                product_two_info=product_two_info,
                product_three_info=product_three_info,
                product_four_info=product_four_info,
                product_five_info=product_five_info,
                sum=total_sum,
                margin=margin,
                no_margin_sum=no_margin_sum,
                form_time=form_time,
                invoice_numbers=invoice_numbers)
    return None

@app.route("/remove_invoice", methods=["POST"])
def remove_invoice():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    invoice_number = request.form["invoice_number"]
    if invoices.remove_invoice(invoice_number):
        return redirect(url_for("invoice_archive"))
    return render_template("error.html", message="Laskun poisto ei onnistunut.")

@app.route("/to_do_list", methods=["GET", "POST"])
def to_do_list():
    if request.method == "GET":
        to_do_info = to_do.get_to_do_list()
        return render_template("/to_do_list.html", count=len(to_do_info),
                               to_do_info=to_do_info, csrf_token=session["csrf_token"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        to_do_info = to_do.get_to_do_list()
        content = request.form["content"]
        if len(content) < 1 or len(content) > 200:
            return render_template("error.html", message="Tarkista syötteen pituus.")
        if to_do.new_to_do(content):
            to_do_info = to_do.get_to_do_list()
            return render_template("/to_do_list.html", count=len(to_do_info),
                        to_do_info=to_do_info, csrf_token=session["csrf_token"])
        return render_template("error.html", message="Viestin lähetys ei onnistunut.")
    return None

@app.route("/remove_to_do", methods=["POST"])
def remove_to_do():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    to_do_id = request.form["to_do_id"]
    if to_do.remove_to_do(to_do_id):
        return redirect(url_for("to_do_list"))
    return render_template("error.html", message="Tehtävän poisto ei onnistunut.")

@app.route("/send_message", methods=["GET", "POST"])
def send_message():
    if request.method == "GET":
        messages_list = messages.get_messages()
        return render_template("/send_message.html", count=len(messages_list),
                               messages_list=messages_list, csrf_token=session["csrf_token"])
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        messages_list = messages.get_messages()
        content = request.form["content"]
        if len(content) < 1 or len(content) > 200:
            return render_template("error.html", message="Tarkista syötteen pituus.")
        if messages.new_message(content):
            messages_list = messages.get_messages()
            return render_template("/send_message.html", count=len(messages_list),
                                   messages_list=messages_list, csrf_token=session["csrf_token"])
        return render_template("error.html", message="Viestin lähetys ei onnistunut.")
    return None

@app.route("/remove_message", methods=["POST"])
def remove_message():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    message_id = request.form["message_id"]
    if messages.remove_message(message_id):
        return redirect(url_for("send_message"))
    return render_template("error.html", message="Viestin poisto ei onnistunut.")

def is_field_too_long(*fields, max_length=20):
    return any(len(field) > max_length for field in fields)

def is_field_missing(*fields):
    return any(len(field) < 1 for field in fields)

def is_too_short(*fields, min_length=4):
    return any(len(field) < min_length for field in fields)
