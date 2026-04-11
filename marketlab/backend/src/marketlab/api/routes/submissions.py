from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from marketlab.api.schemas import SubmissionIn, SubmissionOut, SubmissionShort
from marketlab.domain.generator import generate_tests
from marketlab.infra.db.models import SubmissionRow, UserRow
from marketlab.infra.db.repos.submission_repo import SubmissionRepo
from marketlab.infra.db.session import get_db
from marketlab.usecases.registry import TASK_REGISTRY
from marketlab.usecases.submit_solution import SubmitSolutionInput, submit_solution
from marketlab.api.deps import get_current_user

router = APIRouter(prefix="/api/v1/submissions", tags=["submissions"])

HIDDEN_TESTS_COUNT = 25


@router.post("", response_model=SubmissionOut)
def create_submission(
    body: SubmissionIn,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user),
):
    if body.task_id not in TASK_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Task not found")

    tests = generate_tests(body.task_id, n=HIDDEN_TESTS_COUNT)

    report = submit_solution(
        SubmitSolutionInput(
            task_id=body.task_id,
            user_code=body.user_code,
            tests=tests,
        )
    )

    row = SubmissionRow(
        task_id=body.task_id,
        user_id=current_user.id,
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
        failed_input=report.failed_input,
        failed_expected=report.failed_expected,
        failed_got=report.failed_got,
        created_at=str(row.created_at) if row.created_at else "",
    )


@router.get("", response_model=list[SubmissionShort])
def list_submissions(
    task_id: str | None = None,
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user),
):
    repo = SubmissionRepo(db)
    if task_id:
        rows = repo.list_by_task_and_user(task_id, current_user.id)
    else:
        rows = repo.list_by_user(current_user.id)
    return [
        SubmissionShort(
            id=r.id,
            task_id=r.task_id,
            verdict=r.verdict,
            passed=r.passed,
            total=r.total,
            created_at=str(r.created_at) if r.created_at else "",
        )
        for r in rows
    ]


@router.get("/my-progress")
def my_progress(
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user),
):
    repo = SubmissionRepo(db)
    rows = repo.list_by_user(current_user.id, limit=500)

    task_statuses: dict[str, str] = {}
    for r in rows:
        if r.task_id not in task_statuses:
            task_statuses[r.task_id] = "in_progress"
        if r.verdict == "AC":
            task_statuses[r.task_id] = "solved"

    return task_statuses
