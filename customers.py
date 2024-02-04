from sqlalchemy.sql import text
from db import db

def new_customer(customer_name, address, phonenumber, business_id, user_id):
    if user_id == 0:
        return False
    sql = text("INSERT INTO customers (customer_name, address, phonenumber, business_id, user_id) VALUES (:customer_name,:address,:phonenumber,:business_id, :user_id)")
    db.session.execute(sql, {"customer_name":customer_name, "address":address, "phonenumber":phonenumber, "business_id":business_id, "user_id":user_id})
    db.session.commit()
    return True

def customer_register(user_id):
    sql = text("SELECT C.id, C.customer_name, C.address, C.phonenumber, C.business_id FROM customers C WHERE C.user_id=:user_id AND C.visible=TRUE ORDER BY C.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()  

def remove_customer(id):
    sql = text("UPDATE customers SET visible=FALSE WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()
    return True

def customers_id(user_id):
    sql = text("SELECT C.id FROM customers C WHERE C.user_id=:user_id AND C.visible=TRUE ORDER BY C.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()
    