from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from db import db

def login(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        return True
    return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password) VALUES (:username,:password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
    except SQLAlchemyError:
        return False
    db.session.commit()
    return True

def user_id():
    return session.get("user_id",0)

def usernames():
    sql = text("SELECT username FROM users ORDER BY id")
    result = db.session.execute(sql)
    users = [row[0] for row in result.fetchall()]
    return users

def m_username(u_id):
    sql = text("SELECT username FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":u_id})
    user = result.fetchone()
    return user[0]
