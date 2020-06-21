init:
	pip install pipenv
build:
	pipenv install --dev
lint:
	pipenv run lint
test:
	pipenv run test