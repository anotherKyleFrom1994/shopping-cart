from email import message
from fastapi import FastAPI, status, HTTPException

from .model import *
import requests
import json

app = FastAPI()

USER_ENDPOINT = "http://host.docker.internal:8001/users"
PRODUCT_ENDPOINT = "http://host.docker.internal:8002/products"
CART_ENDPOINT = "http://host.docker.internal:8003/carts"
CART_DETAIL_ENDPOINT = "http://host.docker.internal:8004/cart_details"
ORDER_ENDPOINT = "http://host.docker.internal:8005/orders"


@app.get("/")
def healthcheck():
    return status.HTTP_200_OK


@app.post("/create_product")
async def create_product(payload: CreateProductIn):
    try:
        response = requests.post(PRODUCT_ENDPOINT, json=payload.dict())
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return json.loads(response.content.decode("UTF-8"))


@app.get("/get_all_products")
async def get_all_products():
    try:
        response = requests.get(PRODUCT_ENDPOINT)
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return json.loads(response.content.decode("UTF-8"))


@app.post("/add_item_to_cart")
async def add_item_to_cart(payload: AddItemIn):

    product_res = requests.get(f"{PRODUCT_ENDPOINT}/{payload.product_id}")
    if product_res.status_code == status.HTTP_200_OK:
        product = json.loads(product_res.content.decode("UTF-8"))[0]
    else:
        raise HTTPException(
            status_code=product_res.status_code, detail="product not found"
        )

    if payload.cart_id != None:
        cart_res = requests.get(f"{CART_ENDPOINT}/{payload.cart_id}")
    else:
        cart_res = requests.post(f"{CART_ENDPOINT}")

    if cart_res.status_code == status.HTTP_200_OK:
        cart = json.loads(cart_res.content.decode("UTF-8"))[0]
    else:
        raise HTTPException(status_code=cart_res.status_code)

    cart_detail_res = requests.post(
        CART_DETAIL_ENDPOINT,
        json={"cart_id": cart["id"], "product_id": product["id"]},
    )
    if cart_detail_res.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=cart_detail_res.status_code, detail="add to cart failed"
        )
    return json.loads(cart_detail_res.content.decode("UTF-8"))


@app.post("/checkout")
async def checkout(payload: CheckOutIn):
    return
