# Ohio Union EMS Autofill Tool

This is a tool to auto-fill the EMS paperwork for the Ohio Union AV managers. This tool is provided as-is and is under
active development.

## Installation
1. Install Python3
2. Install pip3
3. Install selenium from pip3
4. Download ChromeDriver and add to PATH
5. Clone this repo
6. Install Google Chrome (not Google Chrome Canary)

## Background
This tool was designed to allow Ohio Union AV Managers to quickly and easily complete the EMS paperwork for the next
day. Using Python3 and Selneium, an open source web browser automation tool, this tool will launch an instance of
Google Chrome, navigate to https://whentowork.com, log in, and pull the schedule for the day specified. Then the tool
will navigate to https://ohiounion.osu.edu/ems and complete the scheduling assignments based on the schedule pulled
from W2W. This tool may work with other Ohio Union manager positions by changing various settings.json attributes,
such as Production, but it is not tested.

## How to Run
 - Make sure dependencies are installed
 - Edit settings.json
    - Enter first name, last name, EMS credentials, WhenToWork credentials etc
 - In Terminal/Command Prompt, change directory to 'EMS Paperwork Tool/' and run:
    python3 autofill_tool.py

## settings.json
    current_manager_first_name: The current manager's first name. Used to assign early-morning setups that should be
        done the night before
    current_manager_last_name: The current manager's last name. Used to assign early-morning setups that should be
        done the night before
    ems_username: OSU name.#
    ems_password: OSU password
    w2w_username: WhenToWork username
    w2w_password: WhenToWork password
    minutes_to_advance_setup: Amount of time prior to the event start time that setup should be scheduled. e.g: If
        event starts at 5:00 PM, "minutes_to_advance_setup" = 30 means setup time is 4:30 PM.
    minutes_to_advance_checkin: Amount of time prior to the event start time that check-in should be scheduled. e.g: If
        event starts at 5:00 PM, "minutes_to_advance_checkin" = 15 means check-in time is 4:45 PM.
    minutes_to_delay_teardown: Amount of time after the event end time that teardown should be scheduled. e.g: If
        event ends at 5:00 PM, "minutes_to_delay_teardown" = 30 means teardown time is 5:30 PM.
    previous_day_setup_cutoff: The cut-off time to schedule the setup for the previous night. e.g.: If the cut-off time
        if 10:00 AM, an event that starts at 9:45 AM would be setup the night prior at "setup_time_night_before" time
        by "current_manager_last_name", "current_manager_first_name".
    setup_time_night_before: The time to setup the event if it's set up the night prior. e.g: If the event starts
        prior to the "previous_day_setup_cutoff", and "setup_time_night_before" = 12:00 AM, the setup would be
        scheduled at 12:00 AM.
    use_w2w: true to use WhenToWork to find the schedule. false to use a separate "schedule.json"
    custom_date: false to use 'tomorrow's' date. true to have the script prompt for the date.
    skip_already_scheduled: true to skip events that have either setup, check-in, or teardown already scheduled. false
        to schedule those anyways. NB: if this is set to false, it will add the schedules, even if they already exist.
    skip_already_confirmed: true to skip events where the setup, check-in, or teardown are already scheduled. false to
        schedule those events anyways.
    skip_events_with_no_av: true to schedule events where the "A/V Equipment" section is "None Found". false to
        schedule those events anyways.
    skip_rooms: true to skip events that are in one of the rooms in "skip_following_rooms". false to schedule those
        events anyways.
    manager_position: The name of the manager position that appears in https://ohiounion.osu.edu/ems that should be used
    order_to_assign_general_shift: The order to schedule events. These are the positions in the W2W headers. eg. If
        the order is "A", "B", "C", the script will try to schedule an "A" first. If there are no A's, it will try to
        schedule a "B". If there are no A's nor B's, the script will try to schedule a "C". If there are no A's, B's,
        nor C's, it will skip assignment for that time only.
    skip_following_rooms: The rooms to skip if "skip_rooms" is true.

## To-Do
 - create reports for shift-leads
 - better installation package
 - auto-confirm shifts