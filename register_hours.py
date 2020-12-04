import json
import requests
import os
import re
import time
import urllib

FACTORIAL_USER = os.environ['FACTORIAL_USER']
FACTORIAL_PASSWORD = os.environ['FACTORIAL_PASSWORD']
FACTORIAL_EMPLOYEE_ID = int(os.environ['FACTORIAL_EMPLOYEE_ID'])
REGISTERS_TEMPLATE = json.loads(os.environ['FACTORIAL_REGISTERS_TEMPLATE'])

YEAR = int(input("Year?: "))
MONTH = int(input("Month Number? (1-12): "))


def login(user, password):
    session = requests.Session()
    url = "https://api.factorialhr.com/users/sign_in"
    authenticity_token = get_auth_token(session)
    payload = f"authenticity_token={authenticity_token}&user%5Bemail%5D={user}&user%5Bpassword%5D={password}&user%5Bremember_me%5D=1"
    headers = {
        'Accept': "*/*",
        'Content-Type': "application/x-www-form-urlencoded",
    }

    session.request("POST", url, data=payload, headers=headers)
    return session


def get_auth_token(session):
    url = 'https://api.factorialhr.com/users/sign_in?return_host=factorialhr.es'
    headers = {
        'Accept': '*/*'
    }
    response = session.request("GET", url, headers=headers)
    token = re.search(
        '<meta name="csrf-token" content="(.+?)" />', response.text).group(1)
    time.sleep(0.5)
    return urllib.parse.quote_plus(token)


def get_period(session, employee_id, year, month):
    url = "https://api.factorialhr.com/attendance/periods"
    querystring = {"year": f"{year}", "month": f"{month}",
                   "employee_id": f"{employee_id}"}
    headers = {}

    response = session.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return(data[0])


def get_calendar(session, period):
    url = "https://api.factorialhr.com/attendance/calendar"
    querystring = {"year": f"{period['year']}",
                   "month": f"{period['month']}", "id": f"{period['employee_id']}"}
    headers = {}

    response = session.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    data.sort(key=lambda tup: tup['day'])
    return(data)


def print_calendar(calendar_data, period):
    print("═" * 50)
    print(f"{' ' * 15}YEAR {period['year']} MONTH {period['month']}")
    print("═" * 50)
    for day in calendar_data:
        registered_minutes = period['distribution'][day['day'] - 1]

        if registered_minutes > 0:
            status = '\033[92m' + \
                f"ALREADY REGISTERED {registered_minutes/60} hours"
        else:
            if day['is_leave']:
                status = '\033[94m' + f"LEAVE DAY: {day['leave_name']}"
            else:
                if day['is_laborable']:
                    status = '\033[93m' + f"WILL REGISTER {REGISTERS_TEMPLATE}"
                else:
                    status = '\033[91m' + "NON WORKING DAY"
        status = status + '\033[0m'

        print('%10s - %-12s' % (day['day'], status))
    print("═" * 50)


def register_pending(session, calendar_data, period):
    for day in calendar_data:
        registered_minutes = period['distribution'][day['day'] - 1]
        if day['is_laborable'] and not day['is_leave'] and registered_minutes == 0:
            register_day(session, period['id'], day['day'])
            time.sleep(0.1)


def register_day(session, period_id, day):
    for register in REGISTERS_TEMPLATE:
        register_hours(session, period_id, day, register[0], register[1])


def register_hours(session, period_id, day, clock_in, clock_out):
    url = "https://api.factorialhr.com/attendance/shifts"
    querystring = {"locale": "en-US"}
    payload = json.dumps({"period_id": period_id, "clock_in": f"{clock_in}",
                          "clock_out": f"{clock_out}", "minutes": 0, "day": day, "observations": "", "history": []})
    headers = {
        'Content-Type': "application/json",
    }

    response = session.request(
        "POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)


if __name__ == "__main__":
    session = login(FACTORIAL_USER, FACTORIAL_PASSWORD)
    period = get_period(session, FACTORIAL_EMPLOYEE_ID, YEAR, MONTH)
    calendar_data = get_calendar(session, period)
    print_calendar(calendar_data, period)

    confirm = input("Continue? (Y/N): ").upper()

    if confirm == 'Y':
        register_pending(session, calendar_data, period)
        print("CHANGES APPLIED. Confirm changes in Factorial UI.")
    else:
        print("No changes applied.")
