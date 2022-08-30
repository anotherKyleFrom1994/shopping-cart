from fastapi import FastAPI, status

app = FastAPI()


@app.get("/")
def healthcheck():
    return status.HTTP_200_OKstatus.HTTP_200_OK
