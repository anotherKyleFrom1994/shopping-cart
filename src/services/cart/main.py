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
async def cart_detail(cart_id: int):
    query = select(Cart).where(Cart.id == cart_id)
    return await database.fetch_all(query=query)


@app.post("/carts")
async def cart_add(payload: CartIn):
    query = insert(Cart).values(**payload.dict())
    try:
        res = await database.execute(query=query)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return res


# @app.put("/carts/{cart_id}")
# def cart_update(cart: Cart, cart_id: int):
#     cart_check(cart_id)
#     cart[cart_id].update(cart)

#     return {"cart": cart[cart_id]}


# @app.delete("/carts/{cart_id}")
# def cart_delete(cart_id: int):
#     cart_check(cart_id)
#     del cart[cart_id]

#     return {"carts": cart}
