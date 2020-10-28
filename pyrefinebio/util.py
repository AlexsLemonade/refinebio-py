from pyrefinebio.http import get
from datetime import datetime


def generator_from_pagination(response, T):
    more_results = True

    while more_results:
        for result in response["results"]:
            yield T(**result)

        if response["next"] == None:
            more_results = False
        else:
            response = get(response["next"])

def parse_date(date):
    parsed = None
    try:
        parsed = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except:
        try:
            parsed = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
        except:
            pass
    
    return parsed
