from sqlalchemy.sql import text
from db import db

def new_product(product_name, type, product_number, price, user_id):
    if user_id == 0:
        return False
    sql = text("INSERT INTO products (product_name, type, product_number, price, user_id) VALUES (:product_name, :type, :product_number, :price, :user_id)")
    db.session.execute(sql, {"product_name":product_name, "type":type, "product_number":product_number, "price":price, "user_id":user_id})
    db.session.commit()
    return True

def product_register():
    sql = text("SELECT P.product_name, P.type, P.product_number, P.price FROM products P, users U WHERE P.user_id=U.id ORDER BY P.id")
    result = db.session.execute(sql)
    return result.fetchall()  