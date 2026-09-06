"""Product HTTP routes."""

from fastapi import APIRouter, HTTPException, status

from schemas.products import ProductCreate, ProductRead, ProductUpdate
from services.products import (
    EmptyProductUpdateError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    create_product,
    get_product,
    list_products,
    update_product,
)


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


@router.get("/{sku}", response_model=ProductRead)
def get_product_route(sku: str) -> ProductRead:
    try:
        return get_product(sku)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error


@router.patch("/{sku}", response_model=ProductRead)
def update_product_route(sku: str, product_update: ProductUpdate) -> ProductRead:
    try:
        return update_product(sku, product_update)
    except ProductNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except EmptyProductUpdateError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
