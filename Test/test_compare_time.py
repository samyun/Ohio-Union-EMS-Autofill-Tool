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


