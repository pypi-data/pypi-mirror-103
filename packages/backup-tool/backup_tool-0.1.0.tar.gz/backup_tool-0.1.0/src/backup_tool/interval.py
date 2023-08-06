SECOND = 1000
MINUTE = SECOND * 60
HOUR = MINUTE * 60
DAY = HOUR * 24
WEEK = DAY * 7

UNITS = {
    "s": SECOND,
    "m": MINUTE,
    "h": HOUR,
    "d": DAY,
    "w": WEEK
}


def parse_interval(interval: str):
    value = int(interval[:-1])
    unit = interval[-1]

    if unit not in UNITS:
        raise ValueError("Unit {unit} not recognized")

    return value * UNITS[unit]
