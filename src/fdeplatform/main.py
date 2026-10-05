from fdeplatform.ops import router as ops_router
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="FDE customer solution")
app.include_router(ops_router, prefix="/v1")
REQUIRED = ("customer", "pain", "constraint", "metric", "refusal")
STORE = []


class Engagement(BaseModel):
    customer: str
    pain: str = ""
    constraint: str = ""
    metric: str = ""
    refusal: str = ""


@app.post("/engagements")
def create(body: Engagement):
    payload = body.model_dump()
    missing = [field for field in REQUIRED if field != "customer" and not str(payload.get(field, "")).strip()]
    status = "ready_for_readout" if not missing else "draft"
    row = {**payload, "status": status, "missing": missing, "live": False}
    STORE.append(row)
    return row


@app.get("/engagements")
def list_engagements():
    return {"engagements": STORE}
