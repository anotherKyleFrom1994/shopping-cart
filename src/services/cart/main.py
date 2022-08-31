from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select, insert
from .model import CartIn
from ..database import database, Base, engine
from ..database.model import Cart

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


@app.get("/carts")
async def get_all_carts():
    return await database.fetch_all(query=select(Cart))


@app.get("/carts/{cart_id}")
async def get_cart(cart_id: int):
    try:
        query = select(Cart).where(Cart.id == cart_id)
        res = await database.fetch_all(query=query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res


@app.post("/carts")
async def cart_add():
    query = insert(Cart).values()
    try:
        res = await database.execute(query=query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return res
