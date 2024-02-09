from sqlalchemy.sql import text
from db import db

def new_invoice(biller_id, customer_id, form_time, invoice_number, product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum, user_id):
    if user_id == 0:
        return False
    try:
        sql = text("INSERT INTO invoices (biller_id, customer_id, form_time, invoice_number, product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum, user_id) VALUES (:biller_id, :customer_id, :form_time, :invoice_number, :product_one_id, :product_two_id, :product_three_id, :product_four_id, :product_five_id, :no_margin_sum, :margin, :sum, :user_id)")
        db.session.execute(sql, {"biller_id":biller_id, "customer_id":customer_id, "form_time":form_time, "invoice_number":invoice_number, "product_one_id":product_one_id, "product_two_id":product_two_id, "product_three_id":product_three_id, "product_four_id":product_four_id, "product_five_id":product_five_id, "no_margin_sum":no_margin_sum, "margin":margin, "sum":sum, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def invoice_archive(user_id):
    sql = text("SELECT  invoice_number, form_time, biller_id, customer_id,  product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum FROM invoices I WHERE I.user_id=:user_id AND I.visible=TRUE ORDER BY I.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall() 
     

#def info(biller_id, user_id):
 #   sql = text("SELECT C.customer_name, C.address, C.phonenumber, C.business_id FROM customers C WHERE C.id=:biller_id AND C.user_id=:user_id AND C.visible=TRUE ORDER BY C.id")
  #  result = db.session.execute(sql, {"biller_id": biller_id, "user_id": user_id})
   # return result.fetchall() 