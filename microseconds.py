from datetime import datetime


def microseconds():
    current_time = datetime.now()
    current_time = current_time.microsecond \
                   + current_time.second * 1000000 \
                   + current_time.minute * 1000000 * 60 \
                   + current_time.hour * 1000000 * 60 * 60 + current_time.day * 1000000 * 60 * 60 * 24
    return current_time
