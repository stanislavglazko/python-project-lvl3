install:
	@poetry install

lint:
	@poetry run flake8 page_loader

selfcheck:
	poetry check

check: selfcheck lint

build: check
	@poetry build

run_test:
	poetry run pytest --cov=page_loader --cov-report xml tests/
