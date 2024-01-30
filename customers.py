from sqlalchemy.sql import text
from db import db

def new_customer(customer_name, address, phonenumber, business_id, user_id):
    try:
        sql = text("INSERT INTO customers (customer_name, address, phonenumber, business_id, user_id) VALUES (:customer_name,:address,:phonenumber,:business_id, :user_id)")
        db.session.execute(sql, {"customer_name":customer_name, "address":address, "phonenumber":phonenumber, "business_id":business_id, "user_id":user_id})
    except:
        return False
    #Print onnistui, tai ei
    db.session.commit()
    return True

    