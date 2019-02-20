#!/usr/bin/python
# encoding: utf-8
import sys
import datetime as dt
from workflow import Workflow3
from dateutil.relativedelta import *

log = None

# goal
# # 29 Summer ☀ w5:13 ㄖ w6:52
# ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░ /6 weeks remaining/
# Using the ISO 8601 calendar and UTC time, should I use EST/Sunday instead?

dob = dt.datetime(1989, 5, 28)
now = dt.datetime.utcnow()
birthday = dt.datetime(now.year, 5, 28)
lastYear = now.year - 1
endOfLastYear = dt.datetime(lastYear, 12, 31)
age = relativedelta(now, dob).years

if now < birthday:
    myWeekNumber = (endOfLastYear.isocalendar()[1] - dt.datetime(lastYear, 5, 28).isocalendar()[1])
else:
    myWeekNumber = now.isocalendar()[1] - birthday.isocalendar()[1]

# current season and weeks in integers
if 3 <= now.month <= 5:
    season = 'Spring ❀'
    seasonWeekNumber = int(now.isocalendar()[1]) - int(dt.datetime(now.year, 3, 1).isocalendar()[1])
elif 8 >= now.month >= 6:
    season = 'Summer ☀'
    seasonWeekNumber = int(now.isocalendar()[1]) - int(dt.datetime(now.year, 6, 1).isocalendar()[1])
elif 11 >= now.month >= 9:
    season = 'Fall ☕︎'
    seasonWeekNumber = int(now.isocalendar()[1]) - int(dt.datetime(now.year, 9, 1).isocalendar()[1])
else:
    season = 'Winter ❄'
    lastYear = now.year - 1
    
    if int(now.month) == 12:
        lastYearsWeeks = 0
        seasonStart = int(dt.datetime(lastYear, 12, 1).isocalendar()[1])
    else:
        lastYearsWeeks = int(endOfLastYear.isocalendar()[1]) - int(dt.datetime(lastYear, 12, 1).isocalendar()[1])
        seasonStart = int(dt.datetime(now.year, 1, 1).isocalendar()[1])

    seasonWeekNumber = int(now.isocalendar()[1]) - seasonStart - lastYearsWeeks

# seasonal loader
empty = '░'
emptyAmount = empty * (13 - (seasonWeekNumber - 1)) * 2
filled = '▓'
filledAmount = filled * (seasonWeekNumber - 1) * 2
# Subtracting one because I generate these at the beginning of the week
loader = "{0}{1}".format(filledAmount, emptyAmount)
# percentage remaining
# percent = int((float(13 - (seasonWeekNumber - 1))/13)*100)
# percent = float(13 - (seasonWeekNumber - 1)) / 13
# percentRemaining = "/ {}% remaining /".format(percent)
weeksRemaining = "/ {} weeks remaining /".format(13-seasonWeekNumber)


def main(wf):
    header = "# {0} {1} {2}:13 ㄖ {3}:52\n{4} {5}".format(age, season, seasonWeekNumber, myWeekNumber, loader,
                                                           weeksRemaining)
    now_string = now.isoformat()
    wf.add_item(title=header, subtitle=now_string, arg=header, valid=True)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main, False))
