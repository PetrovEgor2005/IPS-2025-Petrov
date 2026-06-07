"""
Эндпоинты по сабмитам: приём решения, список прошлых сабмитов, прогресс пользователя.
Решать можно и без логина — тогда saved=False и в БД ляжет user_id=NULL.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from marketlab.api.deps import get_current_user, get_current_user_optional
from marketlab.api.limiter import limiter
from marketlab.api.schemas import SubmissionIn, SubmissionOut, SubmissionShort
from marketlab.domain.generator import generate_tests
from marketlab.infra.db.models import SubmissionRow, UserRow
from marketlab.infra.db.repos.submission_repo import SubmissionRepo
from marketlab.infra.db.session import get_db
from marketlab.usecases.registry import TASK_REGISTRY
from marketlab.usecases.submit_solution import SubmitSolutionInput, submit_solution

router = APIRouter(prefix="/api/v1/submissions", tags=["submissions"])

HIDDEN_TESTS_COUNT = 25


#приём решения. лимит 20/мин с IP — защита от брута/случайных циклов на клиенте
@router.post("", response_model=SubmissionOut)
@limiter.limit("20/minute")
def create_submission(
    request: Request,
    body: SubmissionIn,
    db: Session = Depends(get_db),
    current_user: UserRow | None = Depends(get_current_user_optional),
):
    if body.task_id not in TASK_REGISTRY:
        raise HTTPException(status_code=404, detail="Task not found")

    #25 свежих случайных тестов на каждый сабмит — чтобы нельзя было подогнать решение под пример
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
        user_id=current_user.id if current_user else None,  #None = анонимный сабмит
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
        saved=current_user is not None,  #фронт по этому полю показывает баннер "войди чтобы сохранять прогресс"
    )


#список сабмитов с разной выборкой в зависимости от того, залогинен пользователь или нет
@router.get("", response_model=list[SubmissionShort])
def list_submissions(
    task_id: str | None = None,
    db: Session = Depends(get_db),
    current_user: UserRow | None = Depends(get_current_user_optional),
):
    repo = SubmissionRepo(db)
    if current_user is not None:
        #залогиненный видит свои сабмиты
        if task_id:
            rows = repo.list_by_task_and_user(task_id, current_user.id)
        else:
            rows = repo.list_by_user(current_user.id)
    else:
        #гость — общий пул (для интереса, что вообще присылали)
        if task_id:
            rows = repo.list_by_task(task_id)
        else:
            rows = repo.list_recent()
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


#сводка по прогрессу: для каждой задачи статус "solved" / "in_progress"
@router.get("/my-progress")
def my_progress(
    db: Session = Depends(get_db),
    current_user: UserRow = Depends(get_current_user),
):
    repo = SubmissionRepo(db)
    rows = repo.list_by_user(current_user.id, limit=500)

    #если есть хоть один AC по задаче — она решена, иначе in_progress
    task_statuses: dict[str, str] = {}
    for r in rows:
        if r.task_id not in task_statuses:
            task_statuses[r.task_id] = "in_progress"
        if r.verdict == "AC":
            task_statuses[r.task_id] = "solved"

    return task_statuses
