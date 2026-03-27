from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from marketlab.api.schemas import SubmissionIn, SubmissionOut, SubmissionShort
from marketlab.domain.generator import generate_tests
from marketlab.infra.db.models import SubmissionRow
from marketlab.infra.db.repos import SubmissionRepo
from marketlab.infra.db.session import get_db
from marketlab.usecases.registry import TASK_REGISTRY
from marketlab.usecases.submit_solution import SubmitSolutionInput, submit_solution

router = APIRouter(prefix="/api/v1/submissions", tags=["submissions"])

HIDDEN_TESTS_COUNT = 25


@router.post("", response_model=SubmissionOut)
def create_submission(body: SubmissionIn, db: Session = Depends(get_db)) -> SubmissionOut:
    """Accept user code, run it against generated tests, return verdict and save to DB."""
    if body.task_id not in TASK_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Task '{body.task_id}' not found")

    tests = generate_tests(body.task_id, n=HIDDEN_TESTS_COUNT)

    report = submit_solution(
        SubmitSolutionInput(
            task_id=body.task_id,
            user_code=body.user_code,
            tests=tests,
        )
    )

    # Persist to database.
    row = SubmissionRow(
        task_id=body.task_id,
        user_code=body.user_code,
        verdict=report.verdict,
        passed=report.passed,
        total=report.total,
        message=report.message,
    )
    repo = SubmissionRepo(db)
    repo.create(row)
    db.commit()

    return SubmissionOut(
        id=row.id,
        verdict=report.verdict,
        passed=report.passed,
        total=report.total,
        message=report.message,
        failed_test_index=report.failed_test_index,
        failed_field=report.failed_field,
        created_at=row.created_at,
    )


@router.get("", response_model=list[SubmissionShort])
def list_submissions(
    task_id: str | None = None,
    limit: int = 50,
    db: Session = Depends(get_db),
) -> list[SubmissionShort]:
    """Return submission history, optionally filtered by task_id."""
    repo = SubmissionRepo(db)
    if task_id:
        rows = repo.list_by_task(task_id, limit=limit)
    else:
        rows = repo.list_recent(limit=limit)

    return [
        SubmissionShort(
            id=r.id,
            task_id=r.task_id,
            verdict=r.verdict,
            passed=r.passed,
            total=r.total,
            created_at=r.created_at,
        )
        for r in rows
    ]
