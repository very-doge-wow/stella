install:
	pipenv install -d

test: install
	pipenv run pytest -vv --cov --cov-report=xml

lint: hadolint ruff markdownlint

hadolint:
	hadolint Dockerfile

ruff:
    # task is allowed to fail (leading -)
	-ruff check \
	  --fix \
	  --config "lint.extend-select=['E','F','B','Q','S','W','DJ']"  .

markdownlint:
	markdownlint './*.md' \
	  --ignore './test/output.md' \
	  --ignore './test/custom-template-keywords.md' \
	  --ignore './EXAMPLE_OUTPUT.md'

examples: example example-advanced

example: install
	pipenv run python stella.py \
	  -fh \
	  -css EXAMPLE/style.css \
	  -hcp EXAMPLE/prometheus \
	  -o EXAMPLE/prometheus.html

example-advanced: install
	pipenv run python stella.py \
	  -fh \
	  --advanced-html \
	  -hcp EXAMPLE/prometheus \
	  -o EXAMPLE/prometheus-advanced.html
