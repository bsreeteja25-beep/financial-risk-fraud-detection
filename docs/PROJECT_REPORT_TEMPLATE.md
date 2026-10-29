# Project Report: Financial Risk Analysis and Rule-Based Fraud Detection System

## Abstract
This project analyzes synthetic transactions using explainable rules to prioritize manual review. It stores transactions and alerts, records review outcomes, and produces reports.

## Objectives
- Import and retrieve synthetic transactions through REST APIs.
- Apply amount, frequency, and region-change rules.
- Store reason-coded alerts and review status.
- Generate risk distribution and alert trend reports.
- Maintain an audit trail for key actions.

## Architecture
Client/API docs -> FastAPI -> SQLAlchemy services/rule engine -> SQLite or MySQL -> Pandas/NumPy -> Matplotlib reports.

## Methodology
Describe generated data, validation, thresholds, rules, and scoring.

## Results
Insert actual report API output, chart screenshots, and test results. Do not invent performance figures.

## Limitations
Discuss synthetic data, false positives, false negatives, optional region fields, and the fact that scores are not fraud probabilities.

## Future work
Consider CSV upload, role-based access control, Alembic migrations, a frontend dashboard, and evaluated anomaly detection.
