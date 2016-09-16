from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass
import sys
import os
import json

#global variables
settings, config = ()
driver = webdriver.Chrome()

def validate_date():
    """ Validates date in config.json file and formats it

    Returns:
        (str): formatted date in MM/DD/YYYY
    """

    try:
        if int(config["month"]) < 1 or int(config["month"]) > 12:
            raise ValueError
    except ValueError:
        driver.close()
        raise ValueError("Month '{}' is invalid. Check config.json. ".format(config["month"]))

    try:
        if int(config["day"]) < 1 or int(config["day"]) > 31:
            raise ValueError
    except ValueError:
        driver.close()
        raise ValueError("Day '{}' is invalid. Check config.json. ".format(config["day"]))

    try:
        elif int(config["year"]) < 0 or int(config["year"]) > 2099 or (int(config["year"]) < 2000 and int(config["year"]) > 99):
            raise ValueError
    except ValueError:
        driver.close()
        raise ValueError("Year '{}' is invalid. Check config.json. ".format(config["year"]))

    # if two digit year, convert to 4 digit year.
    if config["year"] < 2000:
        config["year"] = config["year"] + 2000

    if config["month"] == "1":
        name_month = "Jan"
    elif config["month"] == "2":
        name_month = "Feb"
    elif config["month"] == "3":
        name_month = "Mar"
    elif config["month"] == "4":
        name_month = "Apr"
    elif config["month"] == "5":
        name_month = "May"
    elif config["month"] == "6":
        name_month = "Jun"
    elif config["month"] == "7":
        name_month = "Jul"
    elif config["month"] == "8":
        name_month = "Aug"
    elif config["month"] == "9":
        name_month = "Sep"
    elif config["month"] == "10":
        name_month = "Oct"
    elif config["month"] == "11":
        name_month = "Nov"
    else:
        name_month = "Dec"

    return str(config["month"]) + "/" + str(config["day"]) + "/" + str(config["year"])

def navigate_to_event_listing_page():
    # Navigate to EMS
    driver.get('http://ohiounion.osu.edu/ems');

    # If not logged in, log in.
    if driver.title == "Login Required | The Ohio State University":
        inputUser = driver.find_element_by_css_selector(".username")
        inputUser.send_keys(input_ems_username);

        inputPass = driver.find_element_by_css_selector(".password")
        inputPass.send_keys(input_ems_password);
        inputPass.send_keys(u'\ue007');

    if driver.title == "Login Required | The Ohio State University":
        raise RuntimeError("Invalid EMS credentials")

    # Select position, log in as manager
    driver.get("https://ohiounion.osu.edu/secure/ems/")
    try:
        select = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ddl_position"))
        select.select_by_visible_text("Student Manager - AV")
        driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_btn_submit").click()
    except NoSuchElementException:
        driver.close()
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
        settings_json=settings_file.read()
        global settings
        settings = json.loads(settings_json)
        settings_file.close()

    # open config file
    with open('config.json', 'r') as config_file:
        config_json=config_file.read()
        global config
        config = json.loads(config_json)
        config_file.close()

    formatted_date = validate_date()

    # navigate to event listing page
    navigate_to_event_listing_page()

    # Go to date
    datePicker = driver.find_element_by_css_selector(".ctl00_ContentPlaceHolder1_txt_date").clear()
    datePicker.send_keys(formatted_date)
    driver.find_element_by_css_selector(".ctl00_ContentPlaceHolder1_btn_submit").click()

def get_list_of_events():
    """ From the "Ohio Union Daily AV Setup Schedule" page, gets each pair of
    rows and returns them

    Returns:
        list_of_events: A list containing 2-tuples with the two rows for an event
    """

    # Get rows
    list_of_rows = driver.find_elements_by_css_selector("#table-responsive > table > tbody > tr")
    list_of_rows.pop(0)
    num_rows = len(list_of_rows)

    # split rows into events
    list_of_events = []
    for first_row, second_row in zip(list_of_rows[0::2], list_of_rows[1::2]):
        list_of_events.append((first_row, second_row))

    return list_of_events

def get_list_of_javascript(list list_of_events):
    """ Takes a list of events (from get_list_of_events()) and pulls the
    javascript calls to navigate to the event detail page for each event.
    Uses "skip_already_confirmed", "skip_already_scheduled", "skip_rooms",
    and "skip_following_rooms" in settings.json

    Args:
        list_of_events (list): List containing 2-tuples that are the first and
        second rows of each event

    Returns:
        list_of_javascript (list): List containing strings that are the js calls
    """

    list_of_javascript = []
    for tup in list_of_events:
        first_row = tup[0]
        second_row = tup[1]

        # check if already scheduled
        if settings["skip_already_scheduled"]:
            setup_time = first_row.find_element_by_css_selector("td:nth-of-type(7)")
            checkin_time = first_row.find_element_by_css_selector("td:nth-of-type(8)")
            teardown_time = first_row.find_element_by_css_selector("td:nth-of-type(9)")

            if setup_time != "&nbsp" or checkin_time != "&nbsp" or teardown_time != "&nbsp"
                break

        # check if already confirmed
        if settings["skip_already_confirmed"]:
            setup_confirm = second_row.find_element_by_css_selector("td:nth-of-type(4)")
            checkin_confirm = second_row.find_element_by_css_selector("td:nth-of-type(5)")
            teardown_confirm = second_row.find_element_by_css_selector("td:nth-of-type(6)")

            if setup_confirm != "Confirmed" or checkin_confirm != "Confirmed" or teardown_confirm != "Confirmed"
                break

        # check if skip rooms
        if settings["skip_rooms"]:
            room_name = first_row.find_element_by_css_selector("td:nth-of-type(4)").text
            if room_name in settings["skip_following_rooms"]:
                break

        # get javascript command to go to page
        command = first_row.find_element_by_css_selector("td:nth-of-type(5) > a").get_attribute("href")
        splitted_command = command.split(:)
        list_of_javascript.append(splitted_command[1])

    return list_of_javascript

def schedule_event(string js_command):
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
        navigate_to_event_listing_page()

    # navigate to the Event Details page
    driver.implicitly_wait(5)
    driver.execute_script(js_command)
    driver.find_element_by_css_selector(".container-fluid")

    # check page is actually on Event Details page
    title = driver.title
    if title != "EMS - Event Details Page":
        driver.close()
        raise RuntimeError("After calling '{}', page wasn't on the Event Details Page. Title was '{}'".format(title))

    # get the time for the event and parse it
    time_for_event = driver.find_element_by_css_selector("#spRunTime").text
    time_for_event_split = time_for_event.split(' - ')
    event_start = time_for_event_split[0]
    event_end = time_for_event_split[1]

    # get assignment info
    setup_person, setup_time = find_setup_info(event_start)
    checkin_person, checkin_time = find_checkin_info(event_start)
    teardown_person, teardown_time = find_teardown_info(event_end)

    # Enter assignments

def enter_assignment(string person, string time, string assignment):
    """ From the event details page, enters the staff assignments, submit,
    check for errors, and check it was entered.

    Args:
        person (str): name of staff to assign (in format 'Last, First')
        time (str): time to assign (in format '12:00 AM')
        assignment (str): assignment. Valid types are: 'Setup', 'Check-In',
            'Teardown'
    """
    select_staff(person)
    select_assignment(assignment)
    enter_time(time)
    driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_btn_add_staff_assignments").click()


def find_setup_info(string event_start_time):
    """ Given an event start time, find the correct person to setup the event
    and when to setup the event.

    Start by looking at the shift leads. If there is a shift lead whose shift
    starts at or before the setup time and ends after the setup time, setup
    is assigned to that lead. If there are no shift leads who fit, start
    looking at the managers. If there is a manager whose shift starts at or
    before the setup time and ends after the setup time, setup is assigned to
    that manager. If nobody fits, nobody is assigned to that shift.

    Args:
        event_start_time (str): Time the event starts (in the format '12:00 AM')

    Returns:
        setup_info (2-tuple): First element is the name of person (in the
        format 'Last, First') and second element is the time to assign (in the
        format '12:00 AM'). If nobody can be assigned to the setup, return None
    """

    setup_time = get_setup_time(event_start_time)
    if setup_time == "12:00 AM":
        staff = settings["last_name"] + ", " + settings["first_name"]
        return (staff, setup_time)

    found = False
    person = None
    for lead in settings["leads"]:
        if compare_times(lead["start_time"], setup_time) <= 0 and compare_times(lead["end_time"], setup_time) == 1:
            found = True
            person = lead
            break

    if not found:
        for manager in settings["managers"]:
            if compare_times(manager["start_time"], setup_time) <= 0 and compare_times(manager["end_time"], setup_time) == 1:
                found = True
                person = manager
                break

    if not found:
        return None
    else:
        name = person["last_name"] + ", " + person["first_name"]
        return (name, setup_time)

def find_checkin_info(string event_start_time):
    """ Given an event start time, find the correct person to check-in the
    event and when to check-in the event.

    Start by looking at the shift leads. If there is a shift lead whose shift
    starts at or before the check-in time and ends after the check-in time,
    check-in is assigned to that lead. If there are no shift leads who fit,
    start looking at the managers. If there is a manager whose shift starts at
    or before the check-in time and ends after the check-in time, check-in is
    assigned to that manager. If nobody fits, nobody is assigned to that shift.

    Args:
        event_start_time (str): Time the event starts (in the format '12:00 AM')

    Returns:
        checkin_info (2-tuple): First element is the name of person (in the
        format 'Last, First') and second element is the time to assign (in the
        format '12:00 AM'). If nobody can be assigned to the check-in, return
        None
    """

    checkin_time = get_checkin_time(event_start_time)

    found = False
    person = None
    for lead in settings["leads"]:
        if compare_times(lead["start_time"], checkin_time) <= 0 and compare_times(lead["end_time"], checkin_time) == 1:
            found = True
            person = lead
            break

    if not found:
        for manager in settings["managers"]:
            if compare_times(manager["start_time"], checkin_time) <= 0 and compare_times(manager["end_time"], checkin_time) == 1:
                found = True
                person = manager
                break

    if not found:
        return None
    else:
        name = person["last_name"] + ", " + person["first_name"]
        return (name, checkin_time)

def find_teardown_info(string event_end_time):
    """ Given an event end time, find the correct person to teardown the
    event and when to teardown the event.

    Start by looking at the shift leads. If there is a shift lead whose shift
    starts at or before the teardown time and ends after the teardown time,
    teardown is assigned to that lead. If there are no shift leads who fit,
    start looking at the managers. If there is a manager whose shift starts at
    or before the teardown time and ends after the teardown time, teardown is
    assigned to that manager. If nobody fits, nobody is assigned to that shift.

    Args:
        event_end_time (str): Time the event ends (in the format '12:00 AM')

    Returns:
        teardown_info (2-tuple): First element is the name of person (in the
        format 'Last, First') and second element is the time to assign (in the
        format '12:00 AM'). If nobody can be assigned to the teardown, return
        None
    """

    teardown_time = get_teardown_time(event_end_time)

    found = False
    person = None
    for lead in settings["leads"]:
        if compare_times(lead["start_time"], teardown_time) <= 0 and compare_times(lead["end_time"], teardown_time) == 1:
            found = True
            person = lead
            break

    if not found:
        for manager in settings["managers"]:
            if compare_times(manager["start_time"], teardown_time) <= 0 and compare_times(manager["end_time"], teardown_time) == 1:
                found = True
                person = manager
                break

    if not found:
        return None
    else:
        name = person["last_name"] + ", " + person["first_name"]
        return (name, teardown_time)

def parse_time(string time):
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

    return (time_first_number, time_second_number, time_ampm_part)

def compare_times(string time_1, string time_2):
    """ Given two times, compares them.

    Args:
        time_1 (str): first time (in the format '12:00 AM')
        time_2 (str): second time (in the format '12:00 AM')

    Returns:
        -1: time_1 is before time_2
        0 : time_1 is the same time as time_2
        1 : time_1 is after time_2
    """

    time_1_first_part, time_1_second_part, time_1_ampm_part = parse_time(time_1)
    time_2_first_part, time_2_second_part, time_2_ampm_part = parse_time(time_2)

    if time_1_ampm_part == 'AM' and time_2_ampm_part == 'PM':
        return -1
    elif time_1_ampm_part == 'PM' and time_2_ampm_part == 'AM':
        return 1
    else:
        # same ampm, different number

        if time_1_first_part < time_2_first_part:
            return -1
        elif time_1_first_part > time_2_first_part:
            return 1
        else:
            # same first part
            if time_1_second_part < time_2_second_part:
                return -1
            elif time_1_second_part > time_2_second_part:
                return 1
            else:
                #same second part
                return 0

def get_setup_time(string event_start_time):
    """ Given the event start time, find the setup time based on the
    delays/advances in settings.json

    Args:
        event_start_time (str): event start time (in the format '12:00 AM')

    Returns:
        setup_time (str): time to setup for event (in format '12:00 AM')
    """

    if compare_times(settings["previous_day_setup_cutoff"], event_start_time) == 1:
        return "12:00 AM"

    time_first_number, time_second_number, time_ampm_part = parse_time(event_start_time)

    time_second_number -= settings["minutes_to_advance_setup"]

    i = 0
    while time_second_number < 0:
        time_second_number += 60
        time_first_number -= 1
        i += 1

    # cover unlikely event of 12+ hour delays
    extra_ampm_flips = i/12
    time_first_number += 12 * extra_ampm_flips
    if ampm_flips % 2 == 1:
        if time_ampm_part == "AM":
            time_ampm_part == "PM"
        else:
            time_ampm_part == "AM"

    while time_first_number <= 0:
        time_first_number += 12
        if time_ampm_part == "AM":
            time_ampm_part == "PM"
        else:
            time_ampm_part == "AM"

    # return new time
    return str(time_first_number) + ":" + str(time_second_number) + " " + time_ampm_part

def get_checkin_time(string event_start_time):
    """ Given the event start time, find the check-in time based on the
    delays/advances in settings.json

    Args:
        event_start_time (str): event start time (in the format '12:00 AM')

    Returns:
        checkin_time (str): time to check-in event (in format '12:00 AM')
    """

    time_first_number, time_second_number, time_ampm_part = parse_time(event_start_time)

    time_second_number -= settings["minutes_to_advance_checkin"]

    i = 0
    while time_second_number < 0:
        time_second_number += 60
        time_first_number -= 1
        i += 1

    # cover unlikely event of 12+ hour delays
    extra_ampm_flips = i/12
    time_first_number += 12 * extra_ampm_flips
    if ampm_flips % 2 == 1:
        if time_ampm_part == "AM":
            time_ampm_part == "PM"
        else:
            time_ampm_part == "AM"

    while time_first_number <= 0:
        time_first_number += 12
        if time_ampm_part == "AM":
            time_ampm_part == "PM"
        else:
            time_ampm_part == "AM"

    # return new time
    return str(time_first_number) + ":" + str(time_second_number) + " " + time_ampm_part

def get_teardown_time(string event_end_time):
    """ Given the event end time, find the teardown time based on the
    delays/advances in settings.json

    Args:
        event_end_time (str): event end time (in the format '12:00 AM')

    Returns:
        teardown_time (str): time to teardown event (in format '12:00 AM')
    """

    time_first_number, time_second_number, time_ampm_part = parse_time(event_end_time)

    time_second_number += settings["minutes_to_delay_teardown"]

    i = 0
    while time_second_number >= 60:
        time_second_number -= 60
        time_first_number += 1
        i += 1

    # cover unlikely event of 12+ hour delays
    extra_ampm_flips = i/12
    time_first_number += 12 * extra_ampm_flips
    if ampm_flips % 2 == 1:
        if time_ampm_part == "AM":
            time_ampm_part == "PM"
        else:
            time_ampm_part == "AM"

    while time_first_number > 0:
        time_first_number -= 12
        if time_ampm_part == "AM":
            time_ampm_part == "PM"
        else:
            time_ampm_part == "AM"

    # return new time
    return str(time_first_number) + ":" + str(time_second_number) + " " + time_ampm_part

def select_staff(string staff):
    """ Selects the person with name 'staff' in the Staff Assignment form

    Args:
        staff (string): name of person to select

    Raises:
        NoSuchElementException: couldn't find that person in the list
    """

    try:
        select = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ddl_staff"))
        select.select_by_visible_text(staff)
    except NoSuchElementException:
        driver.close()
        raise NoSuchElementException("'{}' wasn't found in the list of staff".format(staff))

def select_assignment(string assignment):
    """ Selects the assignment 'assignment' in the Staff Assignment form

    Args:
        assignment (string): type of assignment to select

    Raises:
        NoSuchElementException: couldn't find that assignment in the list
    """

    try:
        select = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ddl_assignments"))
        select.select_by_visible_text(assignment)
    except NoSuchElementException:
        driver.close()
        raise NoSuchElementException("'{}' wasn't found in the list of assignments".format(assignment))

def enter_time(string time):
    """ Enters the time 'time' in the Staff Assignment form. Assumes 'time' is
    correctly formatted.

    Args:
        time (string): time to enter in the format "12:00 PM"
    """

    time_split = time.split(" ")

    text_box = driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_txt_start_time")
    text_box.send_keys(time[0])

    try:
        select = Select(driver.find_element_by_css_selector("#ctl00_ContentPlaceHolder1_ddl_start_time"))
        select.select_by_visible_text(time[1])
    except NoSuchElementException:
        driver.close()
        raise NoSuchElementException("'{}' wasn't found in the list of AM/PM".format(time[1]))

# Setup environment and get the webdriver
setup()

# get list of events
list_of_events = get_list_of_events()

# get list of javascript commands
list_of_javascript = get_list_of_javascript (list_of_events)

# go to event and schedule
for command in list_of_javascript

    driver.execute_script(command)





time.sleep(30)

driver.quit()
