

def parse_time(time):
    """ Parse a time in the format '12:00 AM' into three parts: hour, minute,
    AM/PM.

    Args:
        time (str): time in format '12:00 AM'

    Returns:
        parsed_time (3-tuple): first element is the hour as an int, second
            element is the minute as an int, and third element is the AM/PM as a str
    """

    time_split = time.split(' ')
    time_number_part_split = time_split[0].split(':')
    time_first_number = int(time_number_part_split[0])
    time_second_number = int(time_number_part_split[1])
    time_ampm_part = time_split[1]

    return time_first_number, time_second_number, time_ampm_part


def get_setup_time(event_start_time, foo=30):
    """ Given the event start time, find the setup time based on the
    delays/advances in settings.json

    Args:
        event_start_time (str): event start time (in the format '12:00 AM')

    Returns:
        setup_time (str): time to setup for event (in format '12:00 AM')
    """

    time_first_number, time_second_number, time_ampm_part = parse_time(event_start_time)

    time_second_number -= foo

    i = 0
    while time_second_number < 0:
        time_second_number += 60
        time_first_number -= 1
        i += 1

    # cover unlikely event of 12+ hour delays
    extra_ampm_flips = int(i/12)
    time_first_number += 12 * extra_ampm_flips
    i -= 12 * extra_ampm_flips
    if extra_ampm_flips % 2 == 1:
        if time_ampm_part == "AM":
            time_ampm_part = "PM"
        else:
            time_ampm_part = "AM"

    while time_first_number < 1:
        time_first_number += 12
        if time_ampm_part == "AM":
            time_ampm_part = "PM"
        else:
            time_ampm_part = "AM"

    if i + time_first_number >= 12 and i > 0:
        if time_ampm_part == "AM":
            time_ampm_part = "PM"
        else:
            time_ampm_part = "AM"

    # return new time
    formatted_time = ""
    if time_first_number < 10:
        formatted_time += "0"
        formatted_time += str(time_first_number)
    else:
        formatted_time += str(time_first_number)

    formatted_time += ":"

    if time_second_number < 10:
        formatted_time += "0"
        formatted_time += str(time_second_number)
    else:
        formatted_time += str(time_second_number)

    formatted_time += " " + time_ampm_part

    return formatted_time


def test_12am():
    assert get_setup_time("12:00 AM") == "11:30 PM"


def test_12pm():
    assert get_setup_time("12:00 PM") == "11:30 AM"


def test_1130pm():
    assert get_setup_time("11:30 PM") == "11:00 PM"


def test_1130am():
    assert get_setup_time("11:30 AM") == "11:00 AM"


def test_10am():
    assert get_setup_time("10:00 AM") == "09:30 AM"


def test_10pm():
    assert get_setup_time("10:00 PM") == "09:30 PM"


def test_2am():
    assert get_setup_time("2:00 AM") == "01:30 AM"


def test_2pm():
    assert get_setup_time("2:00 PM") == "01:30 PM"


def test_130am():
    assert get_setup_time("1:30 AM") == "01:00 AM"


def test_130pm():
    assert get_setup_time("1:30 PM") == "01:00 PM"


def test_1am():
    assert get_setup_time("1:00 AM") == "12:30 AM"


def test_1pm():
    assert get_setup_time("1:00 PM") == "12:30 PM"


def test_1230am():
    assert get_setup_time("12:30 AM") == "12:00 AM"


def test_1230pm():
    assert get_setup_time("12:30 PM") == "12:00 PM"


def test_12am_60():
    assert get_setup_time("12:00 AM", 60) == "11:00 PM"


def test_12pm_60():
    assert get_setup_time("12:00 PM", 60) == "11:00 AM"


def test_1130pm_60():
    assert get_setup_time("11:30 PM", 60) == "10:30 PM"


def test_1130am_60():
    assert get_setup_time("11:30 AM", 60) == "10:30 AM"


def test_10am_60():
    assert get_setup_time("10:00 AM", 60) == "09:00 AM"


def test_10pm_60():
    assert get_setup_time("10:00 PM", 60) == "09:00 PM"


def test_2am_60():
    assert get_setup_time("2:00 AM", 60) == "01:00 AM"


def test_2pm_60():
    assert get_setup_time("2:00 PM", 60) == "01:00 PM"


def test_130am_60():
    assert get_setup_time("1:30 AM", 60) == "12:30 AM"


def test_130pm_60():
    assert get_setup_time("1:30 PM", 60) == "12:30 PM"


def test_1am_60():
    assert get_setup_time("1:00 AM", 60) == "12:00 AM"


def test_1pm_60():
    assert get_setup_time("1:00 PM", 60) == "12:00 PM"


def test_1230_60am():
    assert get_setup_time("12:30 AM", 60) == "11:30 PM"


def test_1230_60pm():
    assert get_setup_time("12:30 PM", 60) == "11:30 AM"

