from fastapi.testclient import TestClient

from fdeplatform.main import STORE, app

client = TestClient(app)


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
