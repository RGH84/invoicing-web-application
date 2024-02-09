from sqlalchemy.sql import text
from db import db

def new_product(product_name, type, product_number, price, user_id):
    if user_id == 0:
        return False
    sql = text("INSERT INTO products (product_name, type, product_number, price, user_id) VALUES (:product_name, :type, :product_number, :price, :user_id)")
    db.session.execute(sql, {"product_name":product_name, "type":type, "product_number":product_number, "price":price, "user_id":user_id})
    db.session.commit()
    return True

def product_register(user_id):
    sql = text("SELECT P.id, P.product_name, P.type, P.product_number, P.price FROM products P WHERE P.user_id=:user_id AND P.visible=TRUE ORDER BY P.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()  

def remove_product(id):
    try:
        sql = text("UPDATE products SET visible=FALSE WHERE id=:id")
        db.session.execute(sql, {"id": id})
        db.session.commit()
    except:
        return False
    return True

def products_id(user_id):
    sql = text("SELECT P.id FROM products P WHERE P.user_id=:user_id AND P.visible=TRUE ORDER BY P.id")
    result = db.session.execute(sql, {"user_id": user_id})
    id_list = [row[0] for row in result.fetchall()]
    return id_list

def info(product_id, user_id):
    sql = text("SELECT P.product_name, P.type, P.product_number, P.price FROM products P WHERE P.user_id=:user_id AND P.id =:product_id AND P.visible=TRUE ORDER BY P.id")
    result = db.session.execute(sql, {"product_id": product_id, "user_id": user_id})
    return result.fetchall() 
