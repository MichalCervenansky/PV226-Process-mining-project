init:
	pip install pipenv
build:
	pipenv install --dev
lint:
	pipenv lint
test:
	pipenv test