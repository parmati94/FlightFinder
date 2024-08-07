from datetime import datetime

def convert_timestamp(timestamp):
    if timestamp is None:
        return None
    time_str = datetime.fromtimestamp(timestamp).strftime('%I:%M %p')
    return time_str.lstrip('0')