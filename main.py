"""HTTP entry point for the StockFlow API."""

from fastapi import FastAPI
from api.inventory import router as inventory_router
from api.products import router as products_router
from database.connection import initialize_database


app = FastAPI(title="StockFlow API")

initialize_database()

app.include_router(products_router)
app.include_router(inventory_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok", "app": "StockFlow API"}
