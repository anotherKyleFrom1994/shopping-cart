from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select, insert
from .model import *
from ..database import database, Base, engine
from ..database.model import Product

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


@app.get("/products")
async def get_all_products():
    return await database.fetch_all(query=select(Product))


@app.get("/products/{product_id}")
async def product_detail(product_id: int):
    query = select(Product).where(Product.id == product_id)
    res = await database.fetch_all(query=query)

    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    return res


@app.post("/products")
async def product_add(payload: ProductIn):
    query = insert(Product).values(**payload.dict())
    try:
        res = await database.execute(query=query)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return res


# @app.put("/products/{product_id}")
# def product_update(product: product, product_id: int):
#     product_check(product_id)
#     product[product_id].update(product)

#     return {"product": product[product_id]}


# @app.delete("/products/{product_id}")
# def product_delete(product_id: int):
#     product_check(product_id)
#     del product[product_id]

#     return {"products": product}


# def product_check(product_id):
#     if not product[product_id]:
#         raise HTTPException(status_code=404, detail="product Not Found")
