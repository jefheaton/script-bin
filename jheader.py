#!/usr/bin/python
# encoding: utf-8
import datetime as dt
import sys

import pytz
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



def main(wf):

    def generate_header():
        dob = dt.datetime(1989, 5, 28, tzinfo=pytz.timezone('utc'))
        now = dt.datetime.now(tz=pytz.timezone('utc'))
        last_year = now.year - 1
        last_week_of_last_year = Week.last_week_of_year(last_year).week
        age = relativedelta(now, dob).years
        my_birthday_happened_this_year = now > dt.datetime(now.year, 5, 28, tzinfo=pytz.timezone('utc'))

        if my_birthday_happened_this_year:
            last_birthday = dt.datetime(now.year, 5, 28)
            weeks_lived_this_year = Week.thisweek().week - Week.withdate(last_birthday).week
        else:
            last_birthday = dt.datetime(last_year, 5, 28)
            weeks_lived_this_year = Week.withdate(now).week + last_week_of_last_year - Week.withdate(last_birthday).week

        seasons = [
            ([3, 4, 5], 'Spring ❀'),
            ([6, 7, 8], 'Summer ☀'),
            ([9, 10, 11], 'Fall ☕︎'),
            ([1, 2, 12], 'Winter ❄'),
        ]

        season_week_number = 0

        for season in seasons:
            if now.month in season[0]:
                current_season = season[1]
                season_week_number = Week.thisweek().week - Week.withdate(
                    dt.datetime(now.year, season[0][0], 1, tzinfo=pytz.timezone('utc'))).week

            if now.month in [1, 2]:
                season_week_number += last_week_of_last_year - Week.withdate(
                    dt.datetime(last_year, 12, 1, tzinfo=pytz.timezone('utc'))).week

        assert season_week_number > 0

        # seasonal loader
        empty = '░'
        empty_amount = empty * (13 - (season_week_number - 1)) * 2
        filled = '▓'
        filled_amount = filled * (season_week_number - 1) * 2
        # Subtracting one because I generate these at the beginning of the week
        loader = "{0}{1}".format(filled_amount, empty_amount)
        weeks_remaining = "/ {} weeks remaining /".format(13 - season_week_number)

        return "# {0} {1} {2}:13 ㄖ {3}:52\n{4} {5}".format(age, current_season, season_week_number,
                                                           weeks_lived_this_year, loader, weeks_remaining)

    header = generate_header()
    now_string = dt.datetime.now(dt.timezone.utc).isoformat()
    wf.add_item(title=header, subtitle=now_string, arg=header, valid=True)
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main, False))
