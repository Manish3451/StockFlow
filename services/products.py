"""Product business logic."""

import sqlite3

from repositories import products as product_repository
from schemas.products import ProductCreate, ProductRead


class ProductAlreadyExistsError(Exception):
    pass


def create_product(product: ProductCreate) -> ProductRead:
    try:
        return product_repository.create_product(product)
    except sqlite3.IntegrityError as error:
        if product_repository.is_unique_sku_error(error):
            raise ProductAlreadyExistsError(
                f"Product with SKU '{product.sku}' already exists."
            ) from error
        raise


def list_products() -> list[ProductRead]:
    return product_repository.list_products()
