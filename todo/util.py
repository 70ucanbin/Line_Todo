from datetime import timedelta, datetime as dt

def text_conv(full_width: str):
    return full_width.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})).replace('\n','')

def time_conv(text_time: str):
    text_time = text_time.replace('/','-')
    date_time = [i for i in text_time.split()]

    try:
        date = dt.strptime(date_time.pop(0),'%m-%d')
        if date_time:
            time = dt.strptime(date_time.pop(0),'%H:%M')
        else:
            time = dt.now()
            
        limit_time = dt(
            dt.now().year,
            date.month,
            date.day,
            time.hour,
            time.minute
            )
        limit_time = limit_time - timedelta(hours=9)

        if limit_time <= dt.now():
            raise ValueError
    except ValueError:
        raise ValueError


    return limit_time