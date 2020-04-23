from fastapi import FastAPI
from routers import github_webhooks

app = FastAPI(openapi_prefix="/api")
app.include_router(github_webhooks.router)


@app.get("/")
def github_push():
    return {"status": "received"}
