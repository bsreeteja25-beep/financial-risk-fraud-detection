# Risk Rules and Scoring

| Rule | Default weight | Trigger |
|---|---:|---|
| `high_amount` | 40 | Amount >= `HIGH_AMOUNT_THRESHOLD` |
| `high_frequency` | 35 | Account reaches `FREQUENCY_COUNT_THRESHOLD` transactions within `FREQUENCY_WINDOW_MINUTES` |
| `region_change` | 25 | Region differs from most recent earlier transaction when both regions exist |

Weights and thresholds are configured in `.env`. Triggered weights are summed and capped at 100. Alerts are generated if the combined score meets `ALERT_SCORE_THRESHOLD`. Each alert record stores the combined score, the individual rule, and its reason.

This score is not a probability of fraud. Rules may produce false positives (legitimate transactions flagged) and false negatives (suspicious transactions missed). The included data is synthetic and is not representative of actual banking behavior. If labelled examples are added, report confusion-matrix counts and precision/recall; avoid overstating results.
