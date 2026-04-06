from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class GeneratorConfig:
    customers: int = 5_000
    products: int = 800
    orders: int = 20_000
    seed: int = 42
    start_date: str = "2024-01-01"
    end_date: str = "2025-12-31"
    output_dir: str = "./data/raw"

    @property
    def start_datetime(self) -> datetime:
        return datetime.fromisoformat(self.start_date)

    @property
    def end_datetime(self) -> datetime:
        return datetime.fromisoformat(self.end_date)

    @property
    def output_path(self) -> Path:
        return Path(self.output_dir)
