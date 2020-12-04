build:
	docker build -t factorial .

run: build
	docker run -it -e FACTORIAL_EMPLOYEE_ID -e FACTORIAL_USER -e FACTORIAL_PASSWORD -e FACTORIAL_REGISTERS_TEMPLATE factorial:latest

lint:
	pipenv run python -m flake8
