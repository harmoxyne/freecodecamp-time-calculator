from TimeCalculator import TimeCalculator


def add_time(start, duration, weekday=None):
    time_calculator = TimeCalculator(start, weekday)
    time_calculator.add_time(duration)

    return time_calculator.get_current_time()
