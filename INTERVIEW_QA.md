# fde-customer-solution-platform — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does fde-customer-solution-platform address, and what can you demonstrate?

An engagement needs five fields: customer, pain, constraint, metric, and refusal. Missing any of the last four keeps the status at `draft` and names the gap.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/fdeplatform/main.py`](src/fdeplatform/main.py): Implementation or supporting configuration.
- [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`Dockerfile`](Dockerfile): Container build/service configuration.
- [`Makefile`](Makefile): Implementation or supporting configuration.
- [`docker-compose.yml`](docker-compose.yml): Container build/service configuration.
- [`tests/test_engagement.py`](tests/test_engagement.py): Executable checks and regression examples.
- [`tests/test_ops.py`](tests/test_ops.py): Executable checks and regression examples.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Is this a running application or a reference repository?

The inspected checkout contains notes, examples, or source assets rather than an identified service entry point. I would describe the actual contents and avoid inventing a backend, database, or deployment. The architecture document records the components that exist.

## 4. What input validation and failure behavior are implemented?

Explicit failure paths include:

- `HTTPException(status_code=404, detail='workspace not found')` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L77).
- `HTTPException(status_code=404, detail='job not found')` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L100).
- `HTTPException(status_code=404, detail='job not found')` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L109).
- `HTTPException(status_code=403, detail='production apply is disabled in this lab')` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L113).

I would test both the condition that reaches each exception and the caller that translates it. An explicit raise does not mean every malformed input or dependency failure is handled.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_engagement.py`](tests/test_engagement.py#L8) contains `test_a_complete_engagement_is_a_readout_and_not_live`:

```python
def test_a_complete_engagement_is_a_readout_and_not_live():
    STORE.clear()
    draft = client.post("/engagements", json={"customer": "Northwind", "pain": "two day wait"}).json()
    assert draft["status"] == "draft"
    assert "constraint" in draft["missing"]
    ready = client.post("/engagements", json={
        "customer": "Northwind",
        "pain": "two day wait",
        "constraint": "no laptop apply",
        "metric": "render in under two minutes",
        "refusal": "prod is not self-serve",
    }).json()
    assert ready["status"] == "ready_for_readout"
    assert ready["live"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `POST /engagements` → `create` in [`src/fdeplatform/main.py`](src/fdeplatform/main.py#L20).
- `GET /engagements` → `list_engagements` in [`src/fdeplatform/main.py`](src/fdeplatform/main.py#L30).
- `GET /readyz` → `readyz` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L74).
- `POST /workspaces` → `create_workspace` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L80).
- `GET /workspaces` → `list_workspaces` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L98).
- `POST /workspaces/{workspace_id}/jobs` → `create_job` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L106).
- `GET /jobs/{job_id}` → `get_job` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L130).
- `POST /jobs/{job_id}/approve` → `approve_job` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py#L140).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. Where does state live, and what happens with multiple workers?

Module-level containers include `STORE` in [`src/fdeplatform/main.py`](src/fdeplatform/main.py); `_WORKSPACES`, `_JOBS`, `_AUDIT`, `_METRICS` in [`src/fdeplatform/ops.py`](src/fdeplatform/ops.py).

These containers belong to a Python process. Inspect which are constant fixtures and which are mutated. Mutable process state needs an explicit shared-storage or synchronization strategy before multiple workers can provide consistent behavior.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What does the operations plane add, and where is its limit?

[`src/fdeplatform/ops.py`](src/fdeplatform/ops.py) declares `GET /readyz`, `POST /workspaces`, `GET /workspaces`, `POST /workspaces/{workspace_id}/jobs`, `GET /jobs/{job_id}`, `POST /jobs/{job_id}/approve`, `GET /audit`, `GET /metrics`. Inspect the application’s `include_router` call for its URL prefix.

Its state containers are `_WORKSPACES`, `_JOBS`, `_AUDIT`, `_METRICS`. The job-approval handler defines whether a target is accepted or refused; check that branch and the associated tests instead of treating a recorded job as a successful infrastructure apply.
