"""Tests for the test-case generator."""

import pytest

from marketlab.domain.generator import generate_tests
from marketlab.usecases.registry import solve_task


class TestGeneratorEquilibrium:
    TASK_ID = "equilibrium_linear_v1"

    def test_returns_requested_count(self):
        tests = generate_tests(self.TASK_ID, n=30, seed=42)
        assert len(tests) == 30

    def test_first_test_is_public_with_seed(self):
        tests = generate_tests(self.TASK_ID, n=5, seed=0)
        first = tests[0]
        assert first["a"] == 120.0
        assert first["mode"] == "tax"
        assert first["t"] == 10.0

    def test_all_modes_covered(self):
        tests = generate_tests(self.TASK_ID, n=25, seed=42)
        modes = {t["mode"] for t in tests}
        assert modes == {"none", "tax", "subsidy"}

    def test_every_test_produces_valid_equilibrium(self):
        tests = generate_tests(self.TASK_ID, n=100, seed=123)
        for i, params in enumerate(tests):
            result = solve_task(self.TASK_ID, params)
            assert result["p_eq"] > 0, f"Test {i}: P* must be positive"
            assert result["q_eq"] > 0, f"Test {i}: Q* must be positive"

    def test_deterministic_with_same_seed(self):
        a = generate_tests(self.TASK_ID, n=10, seed=999)
        b = generate_tests(self.TASK_ID, n=10, seed=999)
        assert a == b

    def test_different_seeds_give_different_tests(self):
        a = generate_tests(self.TASK_ID, n=10, seed=1)
        b = generate_tests(self.TASK_ID, n=10, seed=2)
        assert a[1:] != b[1:]

    def test_unknown_task_raises(self):
        with pytest.raises(ValueError, match="No test generator"):
            generate_tests("nonexistent_task", n=5)
