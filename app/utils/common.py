import enum

class QuoteDataEnum(enum.Enum):
    date = 0
    open = 1
    high = 2
    low = 3
    close = 4
    adj_close = 5

def parse_period(period: str):
    '''Take Input period as 1W, 6M etc. and return timedelta object'''

    duration_to_days = {}
    duration_to_days['W'] = 7
    duration_to_days['M'] = 30
    duration_to_days['Y'] = 365

    value = (int(period[:-1]))*duration_to_days[period[-1]]

    return value
