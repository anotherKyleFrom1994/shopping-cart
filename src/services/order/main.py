from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select, insert, update
from .model import *
from ..database import database, engine, Base
from ..database.model import Order

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


@app.get("/orders")
async def get_all_orders():
    return await database.fetch_all(query=select(Order))


@app.get("/orders/{order_id}")
async def order_detail(order_id: int):
    query = select(Order).where(Order.id == order_id)
    return await database.fetch_all(query=query)


@app.post("/orders")
async def order_add(payload: OrderIn):
    query = insert(Order).values(**payload.dict())
    try:
        res = await database.execute(query=query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res


@app.put("/orders")
async def order_update(payload: OrderUpdateIn):
    query = update(Order).where(Order.id == payload.id).values(**payload.dict())
    try:
        res = await database.execute(query=query)
    except Exception as e:
        raise e
    return res
