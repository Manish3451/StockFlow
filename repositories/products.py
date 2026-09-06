"""Product database queries."""

import sqlite3
from typing import Optional

from database.connection import get_connection
from schemas.products import ProductCreate, ProductRead, ProductUpdate


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


def update_product(sku: str, product_update: ProductUpdate) -> Optional[ProductRead]:
    values_by_column = {}

    if product_update.name is not None:
        values_by_column["name"] = product_update.name

    if product_update.reorder_level is not None:
        values_by_column["reorder_level"] = product_update.reorder_level

    if not values_by_column:
        return get_product_by_sku(sku)

    columns = ", ".join(
        f"{column} = ?"
        for column in values_by_column
    )
    values = list(values_by_column.values())

    with get_connection() as connection:
        connection.execute(
            f"""
            UPDATE products
            SET {columns}
            WHERE sku = ?
            """,
            values + [sku],
        )

    return get_product_by_sku(sku)


def is_unique_sku_error(error: sqlite3.IntegrityError) -> bool:
    return "products.sku" in str(error)
