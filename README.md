# Fucktorial. Automatic hour register in Factorial
Recently Factorial removed a feature that allowed us to copy one time register and fill other pending days of the month. If you miss that feature, and you would like to avoid manual register, this script helps to automatically fill all pending days for a month with a predefined time schedule template.

It uses Factorial API to communicate and register work hours. Feel free to modify, improve, play... with it but **use it at your own risk** take caution when playing with the API.

## Requisites
- Python 3
- pipenv: https://github.com/pypa/pipenv

## Installation and configuration
You will need to install dependencies before first use
```
pipenv install
```

This script needs your Factorial credentials to be provided inside env vars. Please ensure that email at `@` character is HTML escaped with `%40`:
```
export FACTORIAL_USER="user%40mycompany.com"
export FACTORIAL_PASSWORD="XXXX"
```

It also needs your Factorial internal employee ID. It can be easily obtained with browser's dev tool observing request payloads (see screenshot for an example)
```
export FACTORIAL_EMPLOYEE_ID=123456
```

![](./get_employee_id.png?raw=true)

It also needs your time schedule template. Please do not use single quotes. It should be formatted using an array of time slots:
```
export FACTORIAL_REGISTERS_TEMPLATE="[[\"08:30\", \"13:30\"], [\"15:00\", \"18:00\"]]"
```

## Usage
Once configured simply run in a shell:
```
pipenv run python register_hours.py
```

It will prompt for desired year and month number.
Then a list with proposed changes will appear and will ask for confirmation before apply any changes.
Please **be mindful and check before confirm**, any mistakes will need manual correction inside Factorial UI.



