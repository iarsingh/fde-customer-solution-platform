# FDE customer solution platform

Level: Capstone

Skills: Customer engineering, a constraint, a metric, an API

An engagement needs five fields: customer, pain, constraint, metric, and refusal. Missing any of the last four keeps the status at `draft` and names the gap.

A complete record is `ready_for_readout`. `live` stays false. The platform does not mark a customer live from this form.

```bash
pip install -r requirements.txt
pytest -q
```

