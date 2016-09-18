from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
import json
import datetime

# global variables
settings = dict()
config = dict()
driver = webdriver.Chrome()


def wait_for_element_visible(css_selector, timeout=30, raise_exception=True):
    """ Waits for the element to be visible. Defaults to waiting 30s

    Args:
        css_selector (str): The CSS selector for the element
        timeout (int): The time in seconds to wait
        raise_exception (bool): Whether to raise exception

    Returns:
        webelement: The webelement corresponding to the CSS selector. None if can't find element

    Raises:
        TimeoutException: raise_exception == True and can't find element
    """

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        return element
    except TimeoutException:
        if raise_exception:
            raise TimeoutException("Couldn't find element with CSS selector: '{}'".format(css_selector))
        else:
            return None


def wait_for_presence_of_all_elements(css_selector, timeout=30, raise_exception=True):
    """ Waits for the elements to be visible. Defaults to waiting 30s

    Args:
        css_selector (str): The CSS selector for the element
        timeout (int): The time in seconds to wait
        raise_exception (bool): Whether to raise exception

    Returns:
        list of webelement: The webelements corresponding to the CSS selector. None if can't find element

    Raises:
        TimeoutException: raise_exception == True and can't find element
    """

    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
        )
        return element
    except TimeoutException:
        if raise_exception:
            raise TimeoutException("Couldn't find element with CSS selector: '{}'".format(css_selector))
        else:
            return None


def wait_for_invisibility_of_element(css_selector, timeout=30):
    """ Waits for the elements to be invisible. Defaults to waiting 30s

    Args:
        css_selector (str): The CSS selector for the element
        timeout (int): The time in seconds to wait

    Returns:
        invisible (bool): True if element is invisible, False otherwise
    """

    element = WebDriverWait(driver, timeout).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, css_selector))
    )
    return element


def validate_date():
    """ Validates date in config.json file and formats it

    Returns:
        (str): formatted date in MM/DD/YYYY
    """

    try:
        if int(config["month"]) < 1 or int(config["month"]) > 12:
            raise ValueError
    except ValueError:
        raise ValueError("Month '{}' is invalid. Check config.json. ".format(config["month"]))

    try:
        if int(config["day"]) < 1 or int(config["day"]) > 31:
            raise ValueError
    except ValueError:
        raise ValueError("Day '{}' is invalid. Check config.json. ".format(config["day"]))

    try:
        if int(config["year"]) < 0 or int(config["year"]) > 2099 or 99 < int(config["year"]) < 2000:
            raise ValueError
    except ValueError:
        raise ValueError("Year '{}' is invalid. Check config.json. ".format(config["year"]))

    # if two digit year, convert to 4 digit year.
    if config["year"] < 2000:
        config["year"] += 2000

    return str(config["month"]) + "/" + str(config["day"]) + "/" + str(config["year"])


def navigate_to_event_listing_page(select_position=True):
    # Navigate to EMS
    driver.get('http://ohiounion.osu.edu/ems')

    # If not logged in, log in.
    if driver.title == "Login Required | The Ohio State University":
        input_user = wait_for_element_visible("#username")
        input_user.send_keys(settings["username"])

        input_pass = wait_for_element_visible("#password")
        input_pass.send_keys(settings["password"])
        input_pass.send_keys(u'\ue007')

    if driver.title == "Login Required | The Ohio State University":
        raise RuntimeError("Invalid EMS credentials")

    # If select position, log in as manager
    if select_position:
        driver.get("https://ohiounion.osu.edu/secure/ems/")
        try:
            select = Select(wait_for_element_visible("#ctl00_ContentPlaceHolder1_ddl_position"))
            select.select_by_visible_text("Student Manager - AV")
            wait_for_element_visible("#ctl00_ContentPlaceHolder1_btn_submit").click()
        except NoSuchElementException:
            raise NoSuchElementException("You must be an AV Manager to use this tool.")
    else:
        if driver.current_url == "https://ohiounion.osu.edu/secure/ems/":
            try:
                select = Select(wait_for_element_visible("#ctl00_ContentPlaceHolder1_ddl_position"))
                select.select_by_visible_text("Student Manager - AV")
                wait_for_element_visible("#ctl00_ContentPlaceHolder1_btn_submit").click()
            except NoSuchElementException:
                raise NoSuchElementException("You must be an AV Manager to use this tool.")


def setup():
    """ Performs setup for the script.
     - Clears the screen
     - Checks for settings.json and config.json files
     - Imports settings.json and config.json files
     - Validates json files
     - Navigates to page
     - Logs into EMS, goes to the date in config.json
    """

    # check platform, clear screen
    platform = sys.platform

    if platform == "win32":
        os.system('cls')
    elif platform in ["darwin", "linux2", "darwin"]:
        os.system('clear')
    else:
        raise RuntimeError("Platform '{}' not supported".format(platform))

    # check settings/config files exist
    if not os.path.isfile('settings.json'):
        raise RuntimeError("settings.json doesn't exist in path '{}'".format(os.getcwd()))

    if not os.path.isfile('config.json'):
        raise RuntimeError("config.json doesn't exist in path '{}'".format(os.getcwd()))

    # open settings file
    with open('settings.json', 'r') as settings_file:
        settings_json = settings_file.read()
        global settings
        settings = json.loads(settings_json)
        settings_file.close()

    # open config file
    with open('config.json', 'r') as config_file:
        config_json = config_file.read()
        global config
        config = json.loads(config_json)
        config_file.close()

    formatted_date = validate_date()

    # navigate to event listing page
    navigate_to_event_listing_page()

    # Go to date
    wait_for_element_visible("#ctl00_ContentPlaceHolder1_txt_date").click()
    wait_for_element_visible("#ctl00_ContentPlaceHolder1_txt_date").clear()
    wait_for_element_visible("#ctl00_ContentPlaceHolder1_txt_date").send_keys(formatted_date)
    wait_for_element_visible(".container-fluid > h2").click()
    wait_for_invisibility_of_element("#ui-datepicker-div")
    wait_for_element_visible("#ctl00_ContentPlaceHolder1_btn_submit").click()


def get_list_of_events():
    """ From the "Ohio Union Daily AV Setup Schedule" page, gets each pair of
    rows and returns them

    Returns:
        list_events: A list containing 2-tuples with the two rows for an event
    """

    # Get rows
    list_of_rows = wait_for_presence_of_all_elements(".table-responsive > table > tbody > tr")
    list_of_rows.pop(0)

    # split rows into events
    list_events = []
    for row_1, row_2 in zip(list_of_rows[0::2], list_of_rows[1::2]):
        list_events.append((row_1, row_2))

    return list_events


def get_list_of_javascript(event_list):
    """ Takes a list of events (from get_list_of_events()) and pulls the
    javascript calls to navigate to the event detail page for each event.
    Uses "skip_already_confirmed", "skip_already_scheduled", "skip_rooms",
    and "skip_following_rooms" in settings.json

    Args:
        event_list (list): List containing 2-tuples that are the first and
        second rows of each event

    Returns:
        js_list (list): List containing strings that are the js calls
    """

    js_list = []
    for tup in event_list:
        first_row = tup[0]
        second_row = tup[1]

        # check if already scheduled
        if settings["skip_already_scheduled"]:
            setup_time = first_row.find_element_by_css_selector("td:nth-of-type(7)").text
            checkin_time = first_row.find_element_by_css_selector("td:nth-of-type(8)").text
            teardown_time = first_row.find_element_by_css_selector("td:nth-of-type(9)").text

            if setup_time != " " or checkin_time != " " or teardown_time != " ":
                continue

        # check if already confirmed
        if settings["skip_already_confirmed"]:
            setup_confirm = second_row.find_element_by_css_selector("td:nth-of-type(4)").text
            checkin_confirm = second_row.find_element_by_css_selector("td:nth-of-type(5)").text
            teardown_confirm = second_row.find_element_by_css_selector("td:nth-of-type(6)").text

            if setup_confirm != "Confirmed" or checkin_confirm != "Confirmed" or teardown_confirm != "Confirmed":
                continue

        # check if skip rooms
        if settings["skip_rooms"]:
            room_name = first_row.find_element_by_css_selector("td:nth-of-type(4)").text
            if room_name in settings["skip_following_rooms"]:
                continue

        # get javascript command to go to page
        js_command = first_row.find_element_by_css_selector("td:nth-of-type(5) > a").get_attribute("href")
        splitted_command = js_command.split(":")
        js_list.append(splitted_command[1])

    return js_list


def schedule_event(js_command):
    """ Takes the javascript command to navigate to the event page from the
    "Ohio Union Daily AV Setup Schedule" page. Schedules the event based on
    input from config.json. Also uses "skip_events_with_no_av" to skip events
    without any AV equipment listed.

    Args:
        js_command (string): the Javascript command to navigate to the event
        page.
    """

    # check page is on events page
    if driver.current_url != "https://ohiounion.osu.edu/ems/":
        navigate_to_event_listing_page(select_position=False)

    # navigate to the Event Details page
    driver.execute_script(js_command)
    wait_for_element_visible(".container-fluid")

    # check page is actually on Event Details page
    title = driver.title
    if title != "EMS - Event Details Page":
        raise RuntimeError("Page wasn't on the Event Details Page. Title was '{}'".format(title))

    # get the time for the event and parse it
    time_for_event = wait_for_element_visible("#spRunTime").text
    time_for_event_split = time_for_event.split(' - ')
    event_start_time = time_for_event_split[0]
    event_end_time = time_for_event_split[1]

    event_start_dt, event_end_dt = convert_times_to_datetime(event_start_time, event_end_time)

    # get assignment info
    try:
        setup_person, setup_time = find_setup_info(event_start_dt)
        checkin_person, checkin_time = find_checkin_info(event_start_dt)
        teardown_person, teardown_time = find_teardown_info(event_end_dt)
    except TypeError:
        return

    # Enter assignments
    assign_setup(setup_person, setup_time)
    assign_checkin(checkin_person, checkin_time)
    assign_teardown(teardown_person, teardown_time)


def enter_assignment(person, time_to_enter, assignment):
    """ From the event details page, enters the staff assignments, submit,
    check for errors, and check it was entered.

    Args:
        person (str): name of staff to assign (in format 'Last, First')
        time_to_enter (str): time to assign (in format '12:00 AM')
        assignment (str): assignment. Valid types are: 'Setup', 'Check-In',
            'Teardown'
    """
    select_staff(person)
    select_assignment(assignment)
    enter_time(time_to_enter)
    wait_for_element_visible("#ctl00_ContentPlaceHolder1_btn_add_staff_assignments").click()

    # check assigned correctly
    table = wait_for_element_visible("#ctl00_ContentPlaceHolder1_dg_staff_assignments")
    table_rows = table.find_elements_by_css_selector("tr")
    found = False
    for row in table_rows:
        assign_type = row.find_element_by_css_selector("td:nth-of-type(1)").text
        if assignment in assign_type:
            staff_name = row.find_element_by_css_selector("td:nth-of-type(2)").text
            if person in staff_name:
                assign_time = row.find_element_by_css_selector("td:nth-of-type(3)").text
                if time_to_enter in assign_time:
                    found = True
                    break

    if not found:
        raise RuntimeError("After assigning '{0}' to '{1}' at '{2}', assignment wasn't found in the table.".format
                           (person, assignment, time))


def assign_setup(person, setup_time):
    """ Assigns the setup to the given person at the given time.

    Args:
        person (str): Person to assign setup. Format 'Last, First'
        setup_time (str): Time to assign setup. Format '12:00 AM'
    """
    enter_assignment(person, setup_time, "Setup")


def assign_checkin(person, checkin_time):
    """ Assigns the check-in to the given person at the given time.

    Args:
        person (str): Person to assign to check-in. Format 'Last, First'
        checkin_time (str): Time to assign to check-in. Format '12:00 AM'
    """
    enter_assignment(person, checkin_time, "Check-In")


def assign_teardown(person, teardown_time):
    """ Assigns the teardown to the given person at the given time.

    Args:
        person (str): Person to assign to teardown. Format 'Last, First'
        teardown_time (str): Time to assign to teardown. Format '12:00 AM'
    """
    enter_assignment(person, teardown_time, "Teardown")


def find_setup_info(event_start_time):
    """ Given an event start time, find the correct person to setup the event
    and when to setup the event.

    Start by looking at the shift leads. If there is a shift lead whose shift
    starts at or before the setup time and ends after the setup time, setup
    is assigned to that lead. If there are no shift leads who fit, start
    looking at the managers. If there is a manager whose shift starts at or
    before the setup time and ends after the setup time, setup is assigned to
    that manager. If nobody fits, nobody is assigned to that shift.

    Args:
        event_start_time (datetime.datetime): Time the event starts

    Returns:
        setup_info (2-tuple): First element is the name of person (in the
        format 'Last, First') and second element is the time to assign (in the
        format '12:00 AM'). If nobody can be assigned to the setup, return None
    """

    setup_dt = get_setup_time(event_start_time)
    setup_time = convert_datetime_to_time(setup_dt)
    if setup_time == "12:00 AM":
        staff = settings["last_name"] + ", " + settings["first_name"]
        return staff, setup_time

    found = False
    person = None
    for lead in config["leads"]:
        start_time, end_time = convert_times_to_datetime(lead["start_time"], lead["end_time"])
        if compare_times(start_time, setup_dt) <= 0 and compare_times(end_time, setup_dt) == 1:
            found = True
            person = lead
            break

    if not found:
        for manager in config["managers"]:
            start_time, end_time = convert_times_to_datetime(manager["start_time"], manager["end_time"])
            if compare_times(start_time, setup_dt) <= 0 and compare_times(end_time, setup_dt) == 1:
                found = True
                person = manager
                break

    if not found:
        return None
    else:
        name = person["last_name"] + ", " + person["first_name"]
        return name, setup_time


def find_checkin_info(event_start_time):
    """ Given an event start time, find the correct person to check-in the
    event and when to check-in the event.

    Start by looking at the shift leads. If there is a shift lead whose shift
    starts at or before the check-in time and ends after the check-in time,
    check-in is assigned to that lead. If there are no shift leads who fit,
    start looking at the managers. If there is a manager whose shift starts at
    or before the check-in time and ends after the check-in time, check-in is
    assigned to that manager. If nobody fits, nobody is assigned to that shift.

    Args:
        event_start_time (datetime.datetime): Time the event starts (in the format '12:00 AM')

    Returns:
        checkin_info (2-tuple): First element is the name of person (in the
        format 'Last, First') and second element is the time to assign (in the
        format '12:00 AM'). If nobody can be assigned to the check-in, return
        None
    """

    checkin_dt = get_checkin_time(event_start_time)
    checkin_time = convert_datetime_to_time(checkin_dt)

    found = False
    person = None
    for lead in config["leads"]:
        start_time, end_time = convert_times_to_datetime(lead["start_time"], lead["end_time"])
        if compare_times(start_time, checkin_dt) <= 0 and compare_times(end_time, checkin_dt) == 1:
            found = True
            person = lead
            break

    if not found:
        for manager in config["managers"]:
            start_time, end_time = convert_times_to_datetime(manager["start_time"], manager["end_time"])
            if compare_times(start_time, checkin_dt) <= 0 and compare_times(end_time, checkin_dt) == 1:
                found = True
                person = manager
                break

    if not found:
        return None
    else:
        name = person["last_name"] + ", " + person["first_name"]
        return name, checkin_time


def find_teardown_info(event_end_time):
    """ Given an event end time, find the correct person to teardown the
    event and when to teardown the event.

    Start by looking at the shift leads. If there is a shift lead whose shift
    starts at or before the teardown time and ends after the teardown time,
    teardown is assigned to that lead. If there are no shift leads who fit,
    start looking at the managers. If there is a manager whose shift starts at
    or before the teardown time and ends after the teardown time, teardown is
    assigned to that manager. If nobody fits, nobody is assigned to that shift.

    Args:
        event_end_time (datetime.datetime): Time the event ends (in the format '12:00 AM')

    Returns:
        teardown_info (2-tuple): First element is the name of person (in the
        format 'Last, First') and second element is the time to assign (in the
        format '12:00 AM'). If nobody can be assigned to the teardown, return
        None
    """

    teardown_dt = get_teardown_time(event_end_time)
    teardown_time = convert_datetime_to_time(teardown_dt)

    found = False
    person = None
    for lead in config["leads"]:
        start_time, end_time = convert_times_to_datetime(lead["start_time"], lead["end_time"])
        if compare_times(start_time, teardown_dt) <= 0 and compare_times(end_time, teardown_dt) == 1:
            found = True
            person = lead
            break

    if not found:
        for manager in config["managers"]:
            start_time, end_time = convert_times_to_datetime(manager["start_time"], manager["end_time"])
            if compare_times(start_time, teardown_dt) <= 0 and compare_times(end_time, teardown_dt) == 1:
                found = True
                person = manager
                break

    if not found:
        return None
    else:
        name = person["last_name"] + ", " + person["first_name"]
        return name, teardown_time


def parse_time(time_to_parse):
    """ Parse a time in the format '12:00 AM' into three parts: hour, minute,
    AM/PM.

    Args:
        time_to_parse (str): time in format '12:00 AM'

    Returns:
        parsed_time (3-tuple): first element is the hour as an int, second
            element is the minute as an int, and third element is the AM/PM as a str
    """

    time_split = time_to_parse.split(' ')
    time_number_part_split = time_split[0].split(':')
    time_first_number = int(time_number_part_split[0])
    time_second_number = int(time_number_part_split[1])
    time_ampm_part = time_split[1]

    return time_first_number, time_second_number, time_ampm_part


def convert_times_to_datetime(start_time, end_time):
    """ Given a start and end time, converts the two times to DateTime objects.

    Args:
        start_time (str): Start time. In the form '12:00 AM'
        end_time (str): End time. In the form '12:00 AM'

    Returns:
        start_time_dt (datetime.datetime): Start time as a datetime.
        end_time_dt (datetime.datetime): End time as a datetime.
    """

    start_time_first_part, start_time_second_part, start_time_ampm_part = parse_time(start_time)
    end_time_first_part, end_time_second_part, end_time_ampm_part = parse_time(end_time)

    if start_time_ampm_part == "AM":
        start_time_dt = datetime.datetime(2016, 1, 1, start_time_first_part, start_time_second_part)
    else:
        start_time_dt = datetime.datetime(2016, 1, 1, start_time_first_part + 12, start_time_second_part)

    if end_time_ampm_part == "AM" and start_time_ampm_part == "AM":
        end_time_dt = datetime.datetime(2016, 1, 1, end_time_first_part, end_time_second_part)
    elif end_time_ampm_part == "AM" and start_time_ampm_part == "PM":
        end_time_dt = datetime.datetime(2016, 1, 2, end_time_first_part, end_time_second_part)
    else:
        end_time_dt = datetime.datetime(2016, 1, 1, end_time_first_part + 12, end_time_second_part)

    return start_time_dt, end_time_dt


def convert_time_to_datetime(t1):
    """ Given a time, converts it to DateTime object.

    Args:
        t1 (str): time. In the form '12:00 AM'

    Returns:
        t1_dt (datetime.datetime): Start time as a datetime.
    """

    time_first_part, time_second_part, time_ampm_part = parse_time(t1)

    if time_ampm_part == "AM":
        t1_dt = datetime.datetime(2016, 1, 1, time_first_part, time_second_part)
    else:
        t1_dt = datetime.datetime(2016, 1, 1, time_first_part + 12, time_second_part)

    return t1_dt


def convert_datetime_to_time(t1):
    """ Given a datetime, converts it to time.

    Args:
        t1 (datetime.datetime): datetime.

    Returns:
        t1_time (str): time. In the form '12:00 AM'
    """

    hour = t1.time().hour
    minute = t1.time().minute

    if hour > 12:
        hour -= 12
        ampm = "PM"
    else:
        ampm = "AM"

    if minute < 10:
        return str(hour) + ":0" + str(minute) + " " + ampm
    else:
        return str(hour) + ":" + str(minute) + " " + ampm


def compare_times(time_1, time_2):
    """ Given two times, compares them. Times must have come from convert_times_to_datetime

    Args:
        time_1 (datetime.datetime): first time
        time_2 (datetime.datetime): second time

    Returns:
        -1: time_1 is before time_2
        0 : time_1 is the same time as time_2
        1 : time_1 is after time_2
    """

    if time_1 < time_2:
        return -1
    elif time_2 < time_1:
        return 1
    else:
        return 0


def get_setup_time(event_start_time):
    """ Given the event start time, find the setup time based on the delays/advances in settings.json

    Args:
        event_start_time (datetime.datetime): event start time

    Returns:
        setup_time (datetime.datetime): time to setup for event
    """
    if compare_times(convert_time_to_datetime(settings["previous_day_setup_cutoff"]), event_start_time) == 1:
        return "12:00 AM"

    time_delta = datetime.timedelta(minutes=settings["minutes_to_advance_setup"])

    return event_start_time - time_delta


def get_checkin_time(event_start_time):
    """ Given the event start time, find the check-in time based on the delays/advances in settings.json

    Args:
        event_start_time (datetime.datetime): event start time

    Returns:
        checkin_time (datetime.datetime): time to check-in event
    """

    time_delta = datetime.timedelta(minutes=settings["minutes_to_advance_checkin"])

    return event_start_time - time_delta


def get_teardown_time(event_end_time):
    """ Given the event end time, find the teardown time based on the delays/advances in settings.json

    Args:
        event_end_time (datetime.datetime): event end time

    Returns:
        teardown_time (datetime.datetime): time to teardown event
    """

    time_delta = datetime.timedelta(minutes=settings["minutes_to_delay_teardown"])

    return event_end_time + time_delta


def select_staff(staff):
    """ Selects the person with name 'staff' in the Staff Assignment form

    Args:
        staff (string): name of person to select in format 'Last, First'

    Raises:
        NoSuchElementException: couldn't find that person in the list
    """

    select = Select(wait_for_element_visible("#ctl00_ContentPlaceHolder1_ddl_staff"))
    list_of_options = [i.text for i in select.options]
    for option in list_of_options:
        if staff in option:
            select.select_by_index(list_of_options.index(option))
            break
    else:
        raise NoSuchElementException("'{}' wasn't found in the list of staff".format(staff))


def select_assignment(assignment):
    """ Selects the assignment 'assignment' in the Staff Assignment form

    Args:
        assignment (string): type of assignment to select

    Raises:
        NoSuchElementException: couldn't find that assignment in the list
    """

    select = Select(wait_for_element_visible("#ctl00_ContentPlaceHolder1_ddl_assignments"))
    list_of_options = [i.text for i in select.options]
    for option in list_of_options:
        if assignment in option:
            select.select_by_index(list_of_options.index(option))
            break
    else:
        raise NoSuchElementException("'{}' wasn't found in the list of assignments".format(assignment))


def enter_time(time_to_enter):
    """ Enters the time in the Staff Assignment form.

    Args:
        time_to_enter (string): time to enter in the format "12:00 PM"
    """

    time_split = time_to_enter.split(" ")

    text_box = wait_for_element_visible("#ctl00_ContentPlaceHolder1_txt_start_time")
    text_box.clear()
    text_box.send_keys(time_split[0])

    try:
        select = Select(wait_for_element_visible("#ctl00_ContentPlaceHolder1_ddl_start_time"))
        select.select_by_visible_text(time_split[1])
    except NoSuchElementException:
        raise NoSuchElementException("'{}' wasn't found in the list of AM/PM".format(time_split[1]))

# Setup environment and get the webdriver
setup()

# get list of events
list_of_events = get_list_of_events()

# get list of javascript commands
list_of_javascript = get_list_of_javascript(list_of_events)

# go to event and schedule
for command in list_of_javascript:
    schedule_event(command)

driver.quit()
