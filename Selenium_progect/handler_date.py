from datetime import date


def get_date():
    today = date.today()
    return str(today)


print(get_date())
