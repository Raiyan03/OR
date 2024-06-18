from datetime import datetime

def intoTime(time):
    seconds = time / 1000
    return datetime.fromtimestamp(seconds);

def totalHours(fromTime, toTime):
    time1 = intoTime(fromTime)
    time2 = intoTime(toTime)

    hour_diff = time2 - time1
    return hour_diff.total_seconds() / 3600
