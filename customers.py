from sqlalchemy.sql import text
from db import db

def new_customer(customer_name, address, phonenumber, business_id, user_id):
    if user_id == 0:
        return False
    sql = text("INSERT INTO customers (customer_name, address, phonenumber, business_id, user_id) VALUES (:customer_name,:address,:phonenumber,:business_id, :user_id)")
    db.session.execute(sql, {"customer_name":customer_name, "address":address, "phonenumber":phonenumber, "business_id":business_id, "user_id":user_id})
    #Print onnistui, tai ei
    db.session.commit()
    return True

def customer_register():
    sql = text("SELECT C.customer_name, C.address, C.phonenumber, C.business_id FROM customers C, users U WHERE C.user_id=U.id ORDER BY C.id")
    result = db.session.execute(sql)
    return result.fetchall()   

    