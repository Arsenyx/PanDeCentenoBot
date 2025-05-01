from datetime import datetime, timedelta

def calculate_ready_time(cart):
    prep_time = 36 if 'бородинский' in cart else 24
    return datetime.now() + timedelta(hours=prep_time)

def round_to_delivery_window(dt):
    start_hour, end_hour = 11, 20
    delivery_start = dt.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    delivery_end = dt.replace(hour=end_hour, minute=0, second=0, microsecond=0)
    if dt < delivery_start:
        return delivery_start
    elif dt > delivery_end:
        return (dt + timedelta(days=1)).replace(hour=start_hour)
    return dt

def get_delivery_time(cart):
    ready_time = calculate_ready_time(cart)
    delivery_time = round_to_delivery_window(ready_time)
    return delivery_time.strftime('%d.%m.%Y %H:%M')
