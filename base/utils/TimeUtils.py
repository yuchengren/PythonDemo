import time
import calendar
import datetime

# 年月日 日期格式
FORMAT_YEAR_MONTH_DAY_HYPHEN = "%Y-%m-%d"
# 周末索引列表
weekend_list = [5, 6]


def todayWeekday():
    return datetime.datetime.now().weekday()


def isTodayWeekend():
    return todayWeekday() in weekend_list


def isToadyWeekday():
    return not isTodayWeekend()


def isWeekend(_datetime: datetime.datetime):
    return _datetime.weekday() in weekend_list


def isWeekday(_datetime: datetime.datetime):
    return not isWeekend(_datetime)


def formatToDayStr(_datetime: datetime.datetime, _format: str = FORMAT_YEAR_MONTH_DAY_HYPHEN):
    return _datetime.strftime(_format)


def parseToDatetime(_str: str,  _format: str = FORMAT_YEAR_MONTH_DAY_HYPHEN):
    return datetime.datetime.strptime(_str, _format)


def addDays(_datetime: datetime.datetime, days: int):
    return _datetime + datetime.timedelta(days=days)

