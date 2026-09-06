"""Product database queries."""

import sqlite3
from typing import Optional

from database.connection import get_connection
from schemas.products import ProductCreate, ProductRead


def create_product(product: ProductCreate) -> ProductRead:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO products (sku, name, reorder_level)
            VALUES (?, ?, ?)
            """,
            (product.sku, product.name, product.reorder_level),
        )

        row = connection.execute(
            """
            SELECT id, sku, name, reorder_level, created_at
            FROM products
            WHERE id = ?
            """,
            (cursor.lastrowid,),
        ).fetchone()

    return ProductRead(**dict(row))


def get_product_by_sku(
    sku: str,
    connection: Optional[sqlite3.Connection] = None,
) -> Optional[ProductRead]:
    if connection is None:
        with get_connection() as connection:
            return get_product_by_sku(sku, connection)

    row = connection.execute(
        """
        SELECT id, sku, name, reorder_level, created_at
        FROM products
        WHERE sku = ?
        """,
        (sku,),
    ).fetchone()

    if row is None:
        return None

    return ProductRead(**dict(row))


def list_products() -> list[ProductRead]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, sku, name, reorder_level, created_at
            FROM products
            ORDER BY id
            """
        ).fetchall()

    return [ProductRead(**dict(row)) for row in rows]


def is_unique_sku_error(error: sqlite3.IntegrityError) -> bool:
    return "products.sku" in str(error)
