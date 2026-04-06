# Ecommerce Modern Data Platform

A modern data engineering portfolio project designed to demonstrate reproducible local development, synthetic data generation, modular project structure, and a foundation for orchestration, transformations, and CI/CD.

## Overview

This project simulates the early foundation of a modern data platform for an e-commerce domain.

At the current stage, it includes:

- synthetic data generation for core raw entities
- reproducible Python environment management with `uv`
- `src/`-based project structure
- basic validation rules for generated datasets
- raw CSV outputs ready for ingestion into a database or warehouse
- a codebase structured to evolve into a complete end-to-end data platform

The long-term goal is to expand this repository into a full portfolio project with:

- raw ingestion
- warehouse loading
- dbt transformations
- orchestration with Dagster
- data quality checks
- CI/CD pipelines
- containerized local execution

## Current Features

### Synthetic data generation

The project currently generates the following raw datasets:

- `customers`
- `products`

These files are written to:

```text
data/raw/