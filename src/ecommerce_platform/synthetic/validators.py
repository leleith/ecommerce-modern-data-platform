from __future__ import annotations

import pandas as pd


def validate_customers(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("customers dataframe is empty")

    if df["customer_id"].isna().any():
        raise ValueError("customers.customer_id contains nulls")

    if not df["customer_id"].is_unique:
        raise ValueError("customers.customer_id is not unique")

    if df["email"].isna().any():
        raise ValueError("customers.email contains nulls")

    if not df["email"].is_unique:
        raise ValueError("customers.email is not unique")

    if (df["updated_at"] < df["created_at"]).any():
        raise ValueError("customers.updated_at is earlier than created_at")


def validate_products(df: pd.DataFrame) -> None:
    if df.empty:
        raise ValueError("products dataframe is empty")

    if df["product_id"].isna().any():
        raise ValueError("products.product_id contains nulls")

    if not df["product_id"].is_unique:
        raise ValueError("products.product_id is not unique")

    if df["unit_price"].isna().any():
        raise ValueError("products.unit_price contains nulls")

    if (df["unit_price"] <= 0).any():
        raise ValueError("products.unit_price must be greater than zero")

    if (df["updated_at"] < df["created_at"]).any():
        raise ValueError("products.updated_at is earlier than created_at")


def validate_generated_data(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
) -> None:
    validate_customers(customers_df)
    validate_products(products_df)
