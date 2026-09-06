"""Product HTTP routes."""

from fastapi import APIRouter, HTTPException, status

from schemas.products import ProductCreate, ProductRead
from services.products import ProductAlreadyExistsError, create_product, list_products


router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product_route(product: ProductCreate) -> ProductRead:
    try:
        return create_product(product)
    except ProductAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.get("", response_model=list[ProductRead])
def list_products_route() -> list[ProductRead]:
    return list_products()
