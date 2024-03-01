from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db
import users

def new_to_do(content):
    user_id = users.user_id()
    user_name = users.m_username(user_id)
    if user_id == 0:
        return False
    sql = text("""
        INSERT INTO to_do_list (content, user_name, user_id, sent_at) 
        VALUES (:content, :user_name, :user_id, NOW())
    """)
    db.session.execute(sql, {"content": content, "user_name": user_name, "user_id": user_id})
    db.session.commit()
    return True

def get_to_do_list():
    user_id = users.user_id()
    sql = text("""
        SELECT M.id, M.content, U.username, M.sent_at 
        FROM to_do_list M
        JOIN users U ON M.user_id = U.id
        WHERE M.visible = TRUE AND M.user_id = :user_id
        ORDER BY M.id
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()

def remove_to_do(to_do_id):
    try:
        sql = text("UPDATE to_do_list SET visible=FALSE WHERE id=:to_do_id")
        db.session.execute(sql, {"to_do_id": to_do_id})
        db.session.commit()
    except SQLAlchemyError:
        return False
    return True
