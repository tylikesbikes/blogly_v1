from datetime import datetime as dt

def show_friendly_date(date_time):
    days_of_week = {1:'Sunday',
    2:'Monday',
    3:'Tuesday',
    4:'Wednesday',
    5:'Thursday',
    6:'Friday',
    7:'Saturday'}

    months_of_year = {1:'January',
    2:'February',
    3:'March',
    4:'April',
    5:'May',
    6:'June',
    7:'July',
    8:'August',
    9:'September',
    10:'October',
    11:'November',
    12:'December'}

    def adjust_hour_with_ampm(hour):
        ampm = 'AM'
        if hour == 0:
            hour = 12
        elif hour > 12:
            hour -= 12
            ampm = 'PM'

        return (hour, ampm)
    
    hour_ampm = adjust_hour_with_ampm(date_time.hour)

    return f'{days_of_week[date_time.weekday()]} {months_of_year[date_time.month]} {date_time.day}, {hour_ampm[0]}:{date_time.minute} {hour_ampm[1]}'