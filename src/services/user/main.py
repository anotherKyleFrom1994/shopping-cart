from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select, insert
from .model import *
from ..database import database, Base, engine
from ..database.model import User

Base.metadata.bind = engine
Base.metadata.reflect()
Base.metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def healthcheck():
    return status.HTTP_200_OK


@app.get("/users")
async def get_all_users():
    return await database.fetch_all(query=select(User))


@app.get("/users/{user_id}")
async def user_detail(user_id: int):
    query = select(User).where(User.id == user_id)
    return await database.fetch_all(query=query)


@app.post("/users")
async def user_add(payload: UserIn):
    query = insert(User).values(**payload.dict())
    try:
        res = await database.execute(query=query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res
