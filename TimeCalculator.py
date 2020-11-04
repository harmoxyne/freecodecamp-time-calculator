from utils import upper_first_character


class TimeCalculator:
    _initial_time = None
    _current_hours = None
    _current_minutes = None
    _current_period = None
    _current_day_of_week = None
    _include_day_of_week_in_result = False
    _current_days_overflow = 0

    def __init__(self, time: str, day_of_week: str = None):
        self._initial_time = time
        if day_of_week is not None:
            self._current_day_of_week = upper_first_character(day_of_week.lower())
            self._include_day_of_week_in_result = True

        [self._current_hours, self._current_minutes, self._current_period] \
            = parse_time(time)

    def add_time(self, time: str):
        [hours, minutes, _] = parse_time(time)

        if minutes > 60:
            hours += minutes // 60
            minutes = minutes % 60

        # 12-hours format not so convenient for transformations
        # convert to 24-hours format, make transformations, convert back to 12-hours format
        actual_hours = self._get_hours_in_24_format()
        actual_hours += hours

        actual_minutes = self._current_minutes
        actual_minutes += minutes

        if actual_minutes > 60:
            actual_hours += actual_minutes // 60
            actual_minutes = actual_minutes % 60

        self._current_minutes = actual_minutes
        if actual_hours > 24:
            self._current_days_overflow = actual_hours // 24
            actual_hours = actual_hours % 24

        self._convert_hours_from_24_format_to_12_format(actual_hours)

    def get_current_time(self):
        result = '{0}:{1} {2}'.format(
            self._current_hours,
            self._format_minutes(),
            self._current_period
        )

        if self._include_day_of_week_in_result:
            result += self._format_day_value()

        if self._current_days_overflow > 0:
            result += self._format_days_overflow()
        return result

    def _get_hours_in_24_format(self):
        actual_hours = self._current_hours
        if self._current_period == 'PM':
            actual_hours += 12
        return actual_hours

    def _convert_hours_from_24_format_to_12_format(self, hours):
        if hours > 12:
            self._current_hours = hours % 12
            self._current_period = 'PM'
        elif hours == 12:
            self._current_hours = hours
            self._current_period = 'PM'
        elif hours == 0:
            self._current_hours = 12
            self._current_period = 'AM'
        else:
            self._current_hours = hours
            self._current_period = 'AM'

    def _format_day_value(self):
        return ', {0}'.format(
            get_week_day_after_number_of_days(self._current_day_of_week, self._current_days_overflow)
        )

    def _format_minutes(self):
        if self._current_minutes < 10:
            return '0' + str(self._current_minutes)
        return str(self._current_minutes)

    def _format_days_overflow(self):
        if self._current_days_overflow == 0:
            return ''
        elif self._current_days_overflow == 1:
            return ' (next day)'

        return ' ({0} days later)'.format(self._current_days_overflow)


def parse_time(time: str):
    """
    Split time in format '12:34 PM/AM' to list [hours, minutes, period]

    :param time: in format '12:34 PM/AM' or '12:34'
    :return: [hours, minutes, period] or [hours, minutes, None] if period not specified
    """
    period = None
    split_time = time.split(':')
    hours = split_time[0]

    split_minutes = split_time[1].split()
    minutes = split_minutes[0]
    if len(split_minutes) > 1:
        period = split_minutes[1]
    return [int(hours), int(minutes), period]


def get_week_day_after_number_of_days(day: str, number_of_days: int):
    days = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    formatted_day = upper_first_character(day.lower())
    day_index = days.index(formatted_day)
    return days[(day_index + number_of_days) % 7]
