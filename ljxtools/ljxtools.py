"""Main module."""

from ljxtools.utils.date_operation import DatetimeSlove

if __name__ == '__main__':
    d = DatetimeSlove()
    time_now = d.str_now()
    print(time_now)
