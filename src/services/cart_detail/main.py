from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select, insert
from .model import CartDetailIn
from ..database import database, Base, engine
from ..database.model import CartDetail

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


@app.get("/cart_details/{cart_id}")
async def get_cart_detail(cart_id: int):
    query = select(CartDetail).where(CartDetail.id == cart_id)
    return await database.fetch_all(query=query)


@app.post("/cart_details")
async def cart_detail_add(payload: CartDetailIn):
    query = insert(CartDetail).values(**payload.dict())
    try:
        res = await database.execute(query=query)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return res
