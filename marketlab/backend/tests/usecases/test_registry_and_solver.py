import pytest

from marketlab.usecases.registry import get_task_spec, solve_task


def test_registry_returns_spec():
    spec = get_task_spec("equilibrium_linear_v1")
    assert spec.id == "equilibrium_linear_v1"
    assert len(spec.input_fields) >= 5
    assert {f.name for f in spec.output_fields} == {"p_eq", "q_eq"}


def test_solver_returns_multiple_outputs():
    result = solve_task(
        "equilibrium_linear_v1",
        {
            "a": 120,
            "b": 3,
            "c": -10,
            "d": 2,
            "mode": "tax",
            "t": 10,
        },
    )
    assert result["p_eq"] == pytest.approx(30.0)
    assert result["q_eq"] == pytest.approx(30.0)
