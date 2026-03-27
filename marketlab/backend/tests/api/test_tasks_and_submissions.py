"""Integration tests for tasks & submissions API with database persistence.

Uses SQLite in-memory so tests run without Postgres.
"""

import pytest
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from marketlab.api.routes.health import router as health_router
from marketlab.api.routes.tasks import router as tasks_router
from marketlab.api.routes.submissions import router as submissions_router
from marketlab.infra.db.models import Base
from marketlab.infra.db.session import get_db

GOOD_CODE = """\
def solve(params):
    a = float(params["a"]); b = float(params["b"])
    c = float(params["c"]); d = float(params["d"])
    mode = params["mode"]
    t = float(params.get("t", 0.0))
    denom = b + d
    if mode == "none":
        p = (a - c) / denom
    elif mode == "tax":
        p = (a - c + d * t) / denom
    else:
        p = (a - c - d * t) / denom
    q = a - b * p
    return {"p_eq": p, "q_eq": q}
"""

BAD_CODE = """\
def solve(params):
    return {"p_eq": 0.0, "q_eq": 0.0}
"""

# ---------- Test DB setup (SQLite in-memory, single shared connection) ----------

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=test_engine, autoflush=False, expire_on_commit=False)


def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


def _create_test_app() -> FastAPI:
    """Create app WITHOUT lifespan (no Postgres connection needed in tests)."""
    app = FastAPI(title="MarketLab API Test")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(tasks_router)
    app.include_router(submissions_router)
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture(autouse=True)
def setup_db():
    """Create all tables before each test, drop after."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def client():
    return TestClient(_create_test_app())


# ---------- Task tests ----------

class TestTasksAPI:
    def test_list_tasks(self, client):
        resp = client.get("/api/v1/tasks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["id"] == "equilibrium_linear_v1"

    def test_get_task_detail(self, client):
        resp = client.get("/api/v1/tasks/equilibrium_linear_v1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == "equilibrium_linear_v1"
        assert len(data["input_fields"]) >= 5
        assert len(data["output_fields"]) == 2
        assert "public_test" in data

    def test_get_task_not_found(self, client):
        resp = client.get("/api/v1/tasks/no_such_task")
        assert resp.status_code == 404


# ---------- Submission tests ----------

class TestSubmissionsAPI:
    def test_submit_good_code(self, client):
        resp = client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": GOOD_CODE},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["verdict"] == "AC"
        assert data["passed"] == data["total"]
        assert data["id"] is not None

    def test_submit_bad_code(self, client):
        resp = client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": BAD_CODE},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["verdict"] == "WA"
        assert data["id"] is not None

    def test_submit_unknown_task(self, client):
        resp = client.post(
            "/api/v1/submissions",
            json={"task_id": "nope", "user_code": "def solve(p): pass"},
        )
        assert resp.status_code == 404

    def test_submit_empty_code_rejected(self, client):
        resp = client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": ""},
        )
        assert resp.status_code == 422


# ---------- Submission history ----------

class TestSubmissionHistory:
    def test_history_empty(self, client):
        resp = client.get("/api/v1/submissions")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_history_after_submit(self, client):
        client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": GOOD_CODE},
        )
        resp = client.get("/api/v1/submissions")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["verdict"] == "AC"
        assert data[0]["task_id"] == "equilibrium_linear_v1"

    def test_history_filter_by_task(self, client):
        client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": GOOD_CODE},
        )
        resp = client.get("/api/v1/submissions?task_id=equilibrium_linear_v1")
        assert len(resp.json()) == 1

        resp = client.get("/api/v1/submissions?task_id=other_task")
        assert len(resp.json()) == 0

    def test_multiple_submissions_ordered(self, client):
        client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": GOOD_CODE},
        )
        client.post(
            "/api/v1/submissions",
            json={"task_id": "equilibrium_linear_v1", "user_code": BAD_CODE},
        )
        resp = client.get("/api/v1/submissions")
        data = resp.json()
        assert len(data) == 2
        verdicts = {d["verdict"] for d in data}
        assert verdicts == {"AC", "WA"}
