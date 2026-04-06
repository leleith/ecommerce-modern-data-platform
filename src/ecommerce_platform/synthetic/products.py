from __future__ import annotations

from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import random
import uuid


CATEGORY_PRODUCTS: dict[str, list[str]] = {
    "Electronics": [
        "Headphones",
        "Smartphone",
        "Keyboard",
        "Monitor",
        "Smartwatch",
        "Speaker",
    ],
    "Home": [
        "Blender",
        "Vacuum Cleaner",
        "Coffee Maker",
        "Air Fryer",
        "Lamp",
        "Fan",
    ],
    "Sports": [
        "Running Shoes",
        "Gym Shirt",
        "Backpack",
        "Water Bottle",
        "Smart Band",
        "Towel",
    ],
    "Fashion": [
        "T-Shirt",
        "Jeans",
        "Sneakers",
        "Jacket",
        "Cap",
        "Socks",
    ],
    "Beauty": [
        "Shampoo",
        "Conditioner",
        "Moisturizer",
        "Perfume",
        "Sunscreen",
        "Soap",
    ],
    "Books": [
        "Novel",
        "Biography",
        "Cookbook",
        "Sci-Fi Book",
        "History Book",
        "Programming Book",
    ],
}

CATEGORY_WEIGHTS: dict[str, float] = {
    "Electronics": 0.22,
    "Home": 0.18,
    "Sports": 0.16,
    "Fashion": 0.18,
    "Beauty": 0.14,
    "Books": 0.12,
}

CATEGORY_PRICE_RANGES: dict[str, tuple[float, float]] = {
    "Electronics": (80.0, 3500.0),
    "Home": (40.0, 1500.0),
    "Sports": (30.0, 1200.0),
    "Fashion": (25.0, 700.0),
    "Beauty": (15.0, 400.0),
    "Books": (20.0, 180.0),
}

BRANDS = [
    "Acme",
    "Nova",
    "Prime",
    "Pulse",
    "Vertex",
    "Orbit",
    "UrbanX",
    "Nexa",
    "Atlas",
    "Lumina",
]


def _random_datetime_between(start_date: datetime, end_date: datetime) -> datetime:
    total_seconds = int((end_date - start_date).total_seconds())
    
    if total_seconds <= 0:
        raise ValueError("end_date must be greater than start_date")

    offset = random.randint(0, total_seconds)
    return start_date + timedelta(seconds=offset)


def _random_price(category: str) -> float:
    min_price, max_price = CATEGORY_PRICE_RANGES[category]
    return round(random.uniform(min_price, max_price), 2)


def generate_products(
    n: int,
    start_date: datetime,
    end_date: datetime,
    seed: int = 42,
) -> pd.DataFrame:
    random.seed(seed + 1)
    np.random.seed(seed + 1)

    rows: list[dict] = []

    for _ in range(n):
        product_id = str(uuid.uuid4())

        category = random.choices(
            population=list(CATEGORY_WEIGHTS.keys()),
            weights=list(CATEGORY_WEIGHTS.values()),
            k=1,
        )[0]

        brand = random.choice(BRANDS)
        product_base = random.choice(CATEGORY_PRODUCTS[category])

        created_at = _random_datetime_between(start_date, end_date)

        if random.random() < 0.22:
            updated_at = _random_datetime_between(created_at, end_date)
        else:
            updated_at = created_at

        row = {
            "product_id": product_id,
            "product_name": f"{brand} {product_base}",
            "category": category,
            "brand": brand,
            "unit_price": _random_price(category),
            "is_active": random.random() >= 0.08,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    # Alguns produtos atualizados recebem reajuste de preço
    price_change_mask = (df["updated_at"] > df["created_at"]) & (np.random.rand(len(df)) < 0.30)
    for idx in df.index[price_change_mask]:
        current_price = float(df.at[idx, "unit_price"])
        adjustment_factor = random.uniform(0.92, 1.15)
        df.at[idx, "unit_price"] = round(current_price * adjustment_factor, 2)

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])

    return df
