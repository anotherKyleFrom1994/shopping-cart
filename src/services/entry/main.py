import json
from enum import Enum

import requests
from fastapi import FastAPI, HTTPException, status

from .model import *

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
        raise HTTPException(status_code=400, detail=str(e))
    return json.loads(response.content.decode("UTF-8"))


@app.get("/get_all_products")
async def get_all_products():
    try:
        response = requests.get(PRODUCT_ENDPOINT)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return json.loads(response.content.decode("UTF-8"))


@app.post("/create_user")
async def create_user(payload: CreateUserIn):
    try:
        response = requests.post(USER_ENDPOINT, json=payload.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return json.loads(response.content.decode("UTF-8"))


@app.post("/add_item_to_cart")
async def add_item_to_cart(payload: AddItemIn):
    # check the product id before adding to a cart
    product_res = requests.get(f"{PRODUCT_ENDPOINT}/{payload.product_id}")
    if product_res.status_code == status.HTTP_200_OK:
        product = json.loads(product_res.content.decode("UTF-8"))[0]
    else:
        raise HTTPException(
            status_code=product_res.status_code, detail="product not found"
        )

    # Create a new car if there is none
    if payload.cart_id != None:
        cart_res = requests.get(f"{CART_ENDPOINT}/{payload.cart_id}")
    else:
        cart_res = requests.post(f"{CART_ENDPOINT}")

    if cart_res.status_code == status.HTTP_200_OK:
        cart = json.loads(cart_res.content.decode("UTF-8"))
        cart_id = cart if type(cart) == int else cart[0]["id"]
    else:
        raise HTTPException(status_code=cart_res.status_code)

    # Add product to cart and create the relation
    cart_detail_res = requests.post(
        CART_DETAIL_ENDPOINT,
        json={"cart_id": cart_id, "product_id": product["id"]},
    )
    if cart_detail_res.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=cart_detail_res.status_code, detail="add to cart failed"
        )
    return json.loads(cart_detail_res.content.decode("UTF-8"))


@app.post("/checkout")
async def checkout(payload: CheckOutIn):
    cart_detail_res = requests.get(f"{CART_DETAIL_ENDPOINT}/{payload.cart_id}")
    if cart_detail_res.status_code == status.HTTP_200_OK:
        cart_detail = json.loads(cart_detail_res.content.decode("UTF-8"))
    else:
        raise HTTPException(status_code=cart_detail_res.status_code)

    # Create Order
    if payload.order_id != None:
        order_res = requests.get(f"{ORDER_ENDPOINT}/{payload.order_id}")
    else:
        order_res = requests.post(
            ORDER_ENDPOINT,
            json={
                "cart_id": payload.cart_id,
                "user_id": payload.user_id,
                "status": OrderStatus.ACTIVE.value,
            },
        )

    if order_res.status_code == status.HTTP_200_OK:
        order = json.loads(order_res.content.decode("UTF-8"))
        order_id = order if type(order) == int else order[0]["id"]
    else:
        raise HTTPException(status_code=order_res.status_code)

    # Update Order Status
    order_res = requests.put(
        ORDER_ENDPOINT,
        json={
            "id": order_id,
            "cart_id": payload.cart_id,
            "user_id": payload.user_id,
            "status": OrderStatus.PAID.value,
        },
    )

    if order_res.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=order_res.status_code)

    # Update product inventory
    success = True
    product_res = requests.get(PRODUCT_ENDPOINT)
    products = json.loads(product_res.content.decode("UTF-8"))

    product_ids = [c["product_id"] for c in cart_detail]
    products = [p for p in products if p["id"] in product_ids]

    # TBD: Refactor the sync call to async. (httpx or aiohttp-requests)
    for p in products:
        product_res = requests.post(
            PRODUCT_ENDPOINT,
            json={
                "id": p["id"],
                "name": p["name"],
                "price": p["price"],
                "inventory": int(p["inventory"])
                - 1,  # Need to update the cart detail schema to enable quantity
            },
        )
        if product_res.status_code != 200:
            success = False
            raise HTTPException(status_code=product_res.status_code)

    return "Success" if success else "Failed"


@app.get("/get_all_orders")
async def checkout():
    try:
        response = requests.get(ORDER_ENDPOINT)
    except Exception as e:
        raise HTTPException(status_code=400)
    return json.loads(response.content.decode("UTF-8"))


class OrderStatus(Enum):
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    EXPIRED = "EXPIRED"
