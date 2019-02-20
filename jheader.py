#!/usr/bin/python
# encoding: utf-8
import datetime as dt
import sys
from unittest import TestCase

from dateutil.relativedelta import *
from freezegun import freeze_time
from isoweek import Week
from workflow import Workflow3

log = None


# goal
# # 29 Summer ☀ w5:13 ㄖ w6:52
# ▓▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░ /6 weeks remaining/
# Using the ISO 8601 calendar and UTC time, should I use EST/Sunday instead?

class GenerateHeaderTests(TestCase):
    @freeze_time('2001-03-01')
    def test_should_generate_header(self):
        actual = main()
        expected = ''
        self.assertEqual(actual, expected)

    @freeze_time('2001-01-01')
    def test_should_handle_winter_weeks(self):
        pass


def generate_header():
    dob = dt.datetime(1989, 5, 28, tzinfo=dt.timezone.utc)
    now = dt.datetime.now(dt.timezone.utc)
    last_year = now.year - 1
    last_week_of_last_year = Week.last_week_of_year(last_year)
    age = relativedelta(now, dob).years
    my_birthday_happened_this_year = now < dt.datetime(now.year, 5, 28, tzinfo=dt.datetime.utc)

    if my_birthday_happened_this_year:
        last_birthday = dt.datetime(now.year, 5, 28)
        weeks_lived_this_year = Week.thisweek() - Week.withdate(last_birthday)
    else:
        last_birthday = dt.datetime(last_year, 5, 28)
        weeks_lived_this_year = Week(now) + last_week_of_last_year - Week.withdate(last_birthday)

    seasons = [([3, 4, 5], 'Spring ❀'), ([6, 7, 8], 'Summer ☀'), ([9, 10, 11], 'Fall ☕︎'), ([12, 1, 2], 'Winter ❄'), ]

    season_week_number = 0

    for season in seasons:
        if now.month in season[0]:
            current_season = season[1]
            season_week_number = Week.thisweek() - Week.withdate(
                dt.datetime(now.year, season[0][0], 1, tzinfo=dt.timezone.utc))

        if now.month in [1, 2]:
            season_week_number += last_week_of_last_year - Week.withdate(
                dt.datetime(last_year, 12, 1, tzinfo=dt.timezone.utc))

    assert season_week_number != 0

    # seasonal loader
    empty = '░'
    emptyAmount = empty * (13 - (season_week_number - 1)) * 2
    filled = '▓'
    filled_amount = filled * (season_week_number - 1) * 2
    # Subtracting one because I generate these at the beginning of the week
    loader = "{0}{1}".format(filled_amount, emptyAmount)
    # percentage remaining
    # percent = int((float(13 - (seasonWeekNumber - 1))/13)*100)
    # percent = float(13 - (seasonWeekNumber - 1)) / 13
    # percentRemaining = "/ {}% remaining /".format(percent)
    weeks_remaining = "/ {} weeks remaining /".format(13 - season_week_number)

    return "# {0} {1} {2}:13 ㄖ {3}:52\n{4} {5}".format(age, season, season_week_number, weeks_lived_this_year, loader,
                                                         weeks_remaining)


def main(wf):
    now_string = dt.datetime.now(dt.timezone.utc).isoformat()
    wf.add_item(title=generate_header(), subtitle=now_string, arg=generate_header(), valid=True)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main, False))
