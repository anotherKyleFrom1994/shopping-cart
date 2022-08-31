# shopping-cart-api

A basic API service for the shopping cart feature. Besides, it provides a basic checkout feature for the carts.

The application is composed with an entry service and plenty REST APIs. The entry service is for controlling the cart/checkout workflow, and the REST APIs are simply for controlling the persistence layer. By this way break the big requests into small parts. (As a future TODO, we can save the connection resources by making all small HTTP calls asynchronously.)

The services are containerized with Docker. And a entry script `start.sh` that runs docker-compose is created. The source code is also mounted to the container for seeing the real-time effects.

There are still bunch of points to improve. A complete routing mechanism (including reverse proxy) will boost this application. And DB connection mechanism should be optimized. Will list in the last paragraph.

# Initialize the application

## [Optional] Setup poetry locally (require Python3+)

This step for now only sets up the local Poetry for development purpose. Thus optional.

```bash
chmod +x ./init.sh
./init.sh
```

## Start the service

This script build up the Docker containers. It takes more time for the first build. Then takes pretty short time for the next one.

```bash
chmod +x ./start.sh
./start.sh
```

After the server started, you should be able to access the links below:

- http://localhost:8000/docs (entry) Controls the business logics
- http://localhost:8001/docs (users)
- http://localhost:8002/docs (products)
- http://localhost:8003/docs (carts)
- http://localhost:8004/docs (cart_details)
- http://localhost:8005/docs (orders)

And postgresql is serving on `localhost:5432` with default user `postgres`

# Test data

There are some test data currently used for smoke test/integration test. As the next step, unit test cases should be filled up.
FastAPI also provides a quick way to mock and test the functions.

```
    POST http://127.0.0.1:8000/create_user
    {
    "name" : "test_user"
    }

    POST http://127.0.0.1:8000/create_product
    {
    "name" : "test",
    "price": 222,
    "inventory": 44
    }

    POST http://127.0.0.1:8000/add_item_to_cart
    {
    "cart_id" : 1,
    "product_id" :3
    }

    POST http://127.0.0.1:8000/get_all_products
    POST http://127.0.0.1:8000/checkout
    {
        "cart_id": 1,
        "user_id": 2
    }
```

# TODO

- Create unit test mechanism
- A reverse proxy for the microservices
- Fill up clear comments in code
