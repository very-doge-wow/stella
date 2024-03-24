install:
	pipenv install -d
test: install
	pipenv run pytest -vv
