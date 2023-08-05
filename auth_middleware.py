from functools import wraps
import jwt
from fastapi import FastAPI, Request
from flask import current_app
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from dboModel import Base, Users
from config.database import db, session_engine


DBSession = sessionmaker(bind=session_engine.engine)
session = DBSession()

def token_required(request):
  token = None
  if "Authorization" in request.headers and "Identifier" in request.headers:
    # token = request.headers["Authorization"].split(" ")[1]
    username = request.headers["Identifier"]
    token = request.headers["Authorization"]
  else:
    return {
            "message": "Missing one or more authentication credentials!",
            "data": None,
            "error": "Unauthorized"
          }, 401  
  try:
    # data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    current_user=session.query(Users.username,Users.api_key,Users.active).where((Users.username == username) &
                                                  (Users.api_key == token)).one_or_none()    
    if current_user[2] != 1:
      return {
              "data": None,
              "error": "Inactive"
            }, 401 
  except Exception as e:
    if str(e) == "'NoneType' object is not subscriptable":
      return {
              "data": None,
              "error": "Invalid token or identifer"
              }, 500
    else:
      return {
              "data": None,
              "error": str(e)
            }, 500


def auth(request):
  access = token_required(request)
  if access:
    if access[0]['error'] is not None:
      return access
  else:
    return False
