from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db
import users

def new_message(content):
    user_id = users.user_id()
    user_name = users.m_username(user_id)
    if user_id == 0:
        return False
    sql = text("""
        INSERT INTO messages (content, user_name, user_id, sent_at) 
        VALUES (:content, :user_name, :user_id, NOW())
    """)
    db.session.execute(sql, {"content": content, "user_name": user_name, "user_id": user_id})
    db.session.commit()
    return True

def get_messages():
    sql = text("""
        SELECT M.id, M.content, U.username, M.sent_at 
        FROM messages M
        JOIN users U ON M.user_id = U.id
        WHERE M.visible = TRUE 
        ORDER BY M.id
    """)
    result = db.session.execute(sql)
    return result.fetchall()

def remove_message(message_id):
    try:
        sql = text("UPDATE messages SET visible=FALSE WHERE id=:message_id")
        db.session.execute(sql, {"message_id": message_id})
        db.session.commit()
    except SQLAlchemyError:
        return False
    return True
