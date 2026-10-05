# FDE customer solution platform

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/fdeplatform/main.py`](src/fdeplatform/main.py) | HTTP handlers: `POST /engagements`, `GET /engagements` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_engagement.py`](tests/test_engagement.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn fdeplatform.main:app --reload
```

<!-- project-guide:end -->

Level: Capstone

Skills: Customer engineering, a constraint, a metric, an API

An engagement needs five fields: customer, pain, constraint, metric, and refusal. Missing any of the last four keeps the status at `draft` and names the gap.

A complete record is `ready_for_readout`. `live` stays false. The platform does not mark a customer live from this form.

```bash
pip install -r requirements.txt
pytest -q
```

