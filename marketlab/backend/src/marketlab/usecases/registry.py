from __future__ import annotations

from marketlab.domain.tasks import FieldSpec, TaskSpec
from marketlab.usecases.solvers import solve_equilibrium_linear


EQUILIBRIUM_LINEAR = TaskSpec(
    id="equilibrium_linear_v1",
    title="Равновесие на конкурентном рынке (линейные спрос/предложение) с режимами",
    topic="equilibrium",
    input_fields=(
        FieldSpec("a", "float", "Параметр спроса: Qd = a - bP"),
        FieldSpec("b", "float", "Наклон спроса (b>0): Qd = a - bP"),
        FieldSpec("c", "float", "Параметр предложения: Qs = c + dP"),
        FieldSpec("d", "float", "Наклон предложения (d>0): Qs = c + dP"),
        FieldSpec("mode", "str", "Режим: none | tax | subsidy"),
        FieldSpec("t", "float", "Величина налога/субсидии (t>=0), используется при mode!=none"),
    ),
    output_fields=(
        FieldSpec("p_eq", "float", "Равновесная цена (для потребителя)"),
        FieldSpec("q_eq", "float", "Равновесный объём"),
    ),
)

TASK_REGISTRY: dict[str, tuple[TaskSpec, object]] = {
    EQUILIBRIUM_LINEAR.id: (EQUILIBRIUM_LINEAR, solve_equilibrium_linear),
}


def get_task_spec(task_id: str) -> TaskSpec:
    spec, _solver = TASK_REGISTRY[task_id]
    return spec


def solve_task(task_id: str, params: dict) -> dict[str, float]:
    spec, solver = TASK_REGISTRY[task_id]
    result = solver(params)

    expected = {f.name for f in spec.output_fields}
    got = set(result.keys())
    if got != expected:
        raise ValueError(f"Solver returned keys {sorted(got)}, expected {sorted(expected)}")

    return result
