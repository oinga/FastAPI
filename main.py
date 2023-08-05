# main.py

from fastapi import FastAPI, Request, Body

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from dboModel import Base, Patient, Appt
from config.database import db, session_engine, skey
from auth_middleware import token_required, bad_auth


app = FastAPI()

DBSession = sessionmaker(bind=session_engine.engine)
session = DBSession()

# for cross database queries
cursor = db.cursor()


@app.get("/")
async def root():
    return {"message": "Forbidden"}


@app.get("/patients")
async def patients(request: Request):
  no_access = bad_auth(request)
  if not bad_auth(request):
    patients = session.query(Patient).limit(500).all()
    return {"data": patients}
  else:
    return {"data": bad_auth(request)}


@app.get("/patient/{pat_id}")
async def patient(request: Request,pat_id: int):
  if not bad_auth(request):
    patient = session.query(Patient).filter_by(id = pat_id).all()
    return {"data": patient}
  else:
    return {"data": bad_auth(request)}


@app.get("/appts")
async def appts(request: Request):
  if not bad_auth(request):
    appts = session.query(Appt).limit(500).all()
    return {"data": appts}
  else:
    return {"data": bad_auth(request)}


@app.get("/appt/{npi}")
async def appt(request: Request,npi: int):
  if not bad_auth(request):
    appts = session.query(Appt).filter_by(npi = npi).all()
    return {"data": appts}
  else:
    return {"data": bad_auth(request)}



