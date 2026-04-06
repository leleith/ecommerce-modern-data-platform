from __future__ import annotations

from datetime import datetime, timedelta
from faker import Faker
import pandas as pd
import numpy as np
import random
import uuid



CUSTOMER_STATUS_WEIGHTS: dict[str, float] = {
    "active": 0.82,
    "inactive": 0.10,
    "churn_risk": 0.08,
}


EMAIL_DOMAINS = [
    "gmail.com",
    "outlook.com",
    "hotmail.com",
    "yahoo.com",
    "email.com",
]


def _build_unique_email(
    first_name: str,
    last_name: str,
    used_emails: set[str],
) -> str:
    base = (
        f"{first_name}.{last_name}"
        .lower()
        .replace(" ", "")
        .replace("'", "")
        .replace('"', "")
    )

    domain = random.choice(EMAIL_DOMAINS)
    email = f"{base}@{domain}"

    suffix = 1
    while email in used_emails:
        email = f"{base}{suffix}@{domain}"
        suffix += 1

    used_emails.add(email)
    return email


def _random_datetime_between(start_date: datetime, end_date: datetime) -> datetime:
    total_seconds = int((end_date - start_date).total_seconds())

    if total_seconds <= 0:
        raise ValueError("end_date must be greater than start_date")

    offset = random.randint(0, total_seconds)
    return start_date + timedelta(seconds=offset)


def generate_customers(
    n: int,
    start_date: datetime,
    end_date: datetime,
    seed: int = 42,
    locale: str = "pt_BR",
) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

    fake = Faker(locale)
    used_emails: set[str] = set()
    rows: list[dict] = []

    for _ in range(n):
        customer_id = str(uuid.uuid4())
        first_name = fake.first_name()
        last_name = fake.last_name()

        created_at = _random_datetime_between(start_date, end_date)

        if random.random() < 0.28:
            updated_at = _random_datetime_between(created_at, end_date)
        else:
            updated_at = created_at

        customer_status = random.choices(
            population=list(CUSTOMER_STATUS_WEIGHTS.keys()),
            weights=list(CUSTOMER_STATUS_WEIGHTS.values()),
            k=1,
        )[0]

        row = {
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": _build_unique_email(first_name, last_name, used_emails),
            "phone": fake.phone_number() if random.random() > 0.01 else None,
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "city": fake.city(),
            "state": fake.estado_sigla(),
            "country": "Brazil",
            "customer_status": customer_status,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    # Simula mudança cadastral real apenas em registros que tiveram update
    changed_mask = (df["updated_at"] > df["created_at"]) & (np.random.rand(len(df)) < 0.06)
    changed_indices = df.index[changed_mask]

    for idx in changed_indices:
        df.at[idx, "city"] = fake.city()
        df.at[idx, "state"] = fake.estado_sigla()

    df["created_at"] = pd.to_datetime(df["created_at"])
    df["updated_at"] = pd.to_datetime(df["updated_at"])

    return df
