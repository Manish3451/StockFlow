"""Product business logic."""

import sqlite3

from repositories import products as product_repository
from schemas.products import ProductCreate, ProductRead, ProductUpdate


class ProductAlreadyExistsError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class EmptyProductUpdateError(Exception):
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


def get_product(sku: str) -> ProductRead:
    product = product_repository.get_product_by_sku(sku)
    if product is None:
        raise ProductNotFoundError(f"Product with SKU '{sku}' was not found.")

    return product


def update_product(sku: str, product_update: ProductUpdate) -> ProductRead:
    fields_set = getattr(product_update, "model_fields_set", None)
    if fields_set is None:
        fields_set = product_update.__fields_set__

    if not fields_set:
        raise EmptyProductUpdateError("Provide at least one field to update.")

    if (
        "name" in fields_set
        and product_update.name is None
    ):
        raise EmptyProductUpdateError("Product name cannot be null.")

    if (
        "reorder_level" in fields_set
        and product_update.reorder_level is None
    ):
        raise EmptyProductUpdateError("Reorder level cannot be null.")

    existing_product = product_repository.get_product_by_sku(sku)
    if existing_product is None:
        raise ProductNotFoundError(f"Product with SKU '{sku}' was not found.")

    updated_product = product_repository.update_product(sku, product_update)
    if updated_product is None:
        raise ProductNotFoundError(f"Product with SKU '{sku}' was not found.")

    return updated_product
