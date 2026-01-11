.PHONY: fmt lint test check

fmt:
	cd backend && ruff format .

lint:
	cd backend && ruff check --fix .

test:
	cd backend && pytest -q

check: lint fmt test
