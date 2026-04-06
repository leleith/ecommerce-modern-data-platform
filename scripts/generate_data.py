from __future__ import annotations

import argparse

from ecommerce_platform.synthetic.validators import validate_generated_data
from ecommerce_platform.synthetic.customers import generate_customers
from ecommerce_platform.synthetic.products import generate_products
from ecommerce_platform.synthetic.config import GeneratorConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate synthetic raw data for the ecommerce portfolio project."
    )

    parser.add_argument("--customers", type=int, default=5_000)
    parser.add_argument("--products", type=int, default=800)
    parser.add_argument("--orders", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-date", type=str, default="2024-01-01")
    parser.add_argument("--end-date", type=str, default="2025-12-31")
    parser.add_argument("--output-dir", type=str, default="./data/raw")

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config = GeneratorConfig(
        customers=args.customers,
        products=args.products,
        orders=args.orders,
        seed=args.seed,
        start_date=args.start_date,
        end_date=args.end_date,
        output_dir=args.output_dir,
    )

    config.output_path.mkdir(parents=True, exist_ok=True)

    print("Generating customers...")
    customers_df = generate_customers(
        n=config.customers,
        start_date=config.start_datetime,
        end_date=config.end_datetime,
        seed=config.seed,
    )

    print("Generating products...")
    products_df = generate_products(
        n=config.products,
        start_date=config.start_datetime,
        end_date=config.end_datetime,
        seed=config.seed,
    )

    print("Validating generated data...")
    validate_generated_data(
        customers_df=customers_df,
        products_df=products_df,
    )

    customers_output = config.output_path / "customers.csv"
    products_output = config.output_path / "products.csv"

    print(f"Writing {customers_output} ...")
    customers_df.to_csv(customers_output, index=False)

    print(f"Writing {products_output} ...")
    products_df.to_csv(products_output, index=False)

    print("Done.")
    print(f"customers: {len(customers_df):,}")
    print(f"products: {len(products_df):,}")


if __name__ == "__main__":
    main()
