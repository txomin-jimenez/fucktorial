FROM python:3.7.5-slim-buster

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install

COPY . .

ENV FACTORIAL_USER "user@nextail.co"
ENV FACTORIAL_PASSWORD "XXXX"
ENV FACTORIAL_EMPLOYEE_ID 123456
ENV FACTORIAL_REGISTERS_TEMPLATE "[[\"08:30\", \"13:30\"], [\"15:00\", \"18:00\"]]"

CMD ["pipenv", "run", "python", "register_hours.py"]
