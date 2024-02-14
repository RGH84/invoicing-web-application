from sqlalchemy.sql import text
from db import db

def new_invoice(biller_id, customer_id, form_time, invoice_number, product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum, user_id):
    if user_id == 0:
        return False
    sql = text("INSERT INTO invoices (biller_id, customer_id, form_time, invoice_number, product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum, user_id) VALUES (:biller_id, :customer_id, :form_time, :invoice_number, :product_one_id, :product_two_id, :product_three_id, :product_four_id, :product_five_id, :no_margin_sum, :margin, :sum, :user_id)")
    db.session.execute(sql, {"biller_id":biller_id, "customer_id":customer_id, "form_time":form_time, "invoice_number":invoice_number, "product_one_id":product_one_id, "product_two_id":product_two_id, "product_three_id":product_three_id, "product_four_id":product_four_id, "product_five_id":product_five_id, "no_margin_sum":no_margin_sum, "margin":margin, "sum":sum, "user_id":user_id})
    db.session.commit()
    return True
    
def invoice_archive(user_id):
    sql = text("SELECT  invoice_number, form_time, biller_id, customer_id,  product_one_id, product_two_id, product_three_id, product_four_id, product_five_id, no_margin_sum, margin, sum FROM invoices I WHERE I.user_id=:user_id AND I.visible=TRUE ORDER BY I.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall() 
     

def info(invoice_number, user_id):
    sql = text("""
    SELECT 
        invoice_number, 
        form_time, 
        biller_id, 
        customer_id, 
        product_one_id,
        product_two_id,
        product_three_id,
        product_four_id,
        product_five_id,
        no_margin_sum, 
        margin, 
        sum
    FROM 
        invoices
    WHERE 
        visible = TRUE AND invoice_number=:invoice_number AND user_id=:user_id
    """)
    result = db.session.execute(sql, {"invoice_number": invoice_number, "user_id": user_id})
    return result.fetchall() 

def numbers(user_id):
    sql = text("SELECT invoice_number FROM invoices WHERE user_id=:user_id AND visible=TRUE ORDER BY id")
    result = db.session.execute(sql, {"user_id": user_id})
    numbers = [row[0] for row in result.fetchall()]
    return numbers 