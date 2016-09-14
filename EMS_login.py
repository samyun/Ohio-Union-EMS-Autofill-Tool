from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass
import sys
import os
import json

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
    settings = json.loads(settings_json)
    settings_file.close()

# open config file
with open('config.json', 'r') as config_file:
    config_json=config_file.read()
    config = json.loads(config_json)
    config_file.close()

# validate date
    try:
        if int(config[month]) < 1 or int(config[month]) > 12:
            raise ValueError
    except ValueError:
        raise ValueError("Month '{}' is invalid. Check config.json. ".format(config[month]))

    try:
        if int(config[day]) < 1 or int(config[day]) > 31:
            raise ValueError
    except ValueError:
        raise ValueError("Day '{}' is invalid. Check config.json. ".format(config[day]))

    try:
        elif int(config[year]) < 0 or int(config[year]) > 2099 or (int(config[year]) < 2000 and int(config[year]) > 99):
            raise ValueError
    except ValueError:
        raise ValueError("Year '{}' is invalid. Check config.json. ".format(config[year]))

# if two digit year, convert to 4 digit year.
if config[year] < 2000:
    config[year] = config[year] + 2000

if config[month] == "1":
    name_month = "Jan"
elif config[month] == "2":
    name_month = "Feb"
elif config[month] == "3":
    name_month = "Mar"
elif config[month] == "4":
    name_month = "Apr"
elif config[month] == "5":
    name_month = "May"
elif config[month] == "6":
    name_month = "Jun"
elif config[month] == "7":
    name_month = "Jul"
elif config[month] == "8":
    name_month = "Aug"
elif config[month] == "9":
    name_month = "Sep"
elif config[month] == "10":
    name_month = "Oct"
elif config[month] == "11":
    name_month = "Nov"
else:
    name_month = "Dec"

# start Chrome and navigate to W2W
driver = webdriver.Chrome()
driver.get('http://ohiounion.osu.edu/ems');

# if not logged in, log in.
if driver.title == "Login Required | The Ohio State University":
    inputUser = driver.find_element_by_css_selector(".username")
    inputUser.send_keys(input_ems_username);

    inputPass = driver.find_element_by_css_selector(".password")
    inputPass.send_keys(input_ems_password);
    inputPass.send_keys(u'\ue007');

if driver.title == "Login Required | The Ohio State University":
    raise RuntimeError("Invalid EMS credentials")

# Log in as manager
select = Select(driver.find_element_by_css_selector(".ctl00_ContentPlaceHolder1_ddl_position"))
select.select_by_visible_text("Student Manager - AV")
driver.find_element_by_css_selector(".ctl00_ContentPlaceHolder1_btn_submit").click()

# Go to date
datePicker = driver.find_element_by_css_selector(".ctl00_ContentPlaceHolder1_txt_date").clear()
datePicker.send_keys(str(input_month) + "/" + str(input_day) + "/" + str(input_year))
driver.find_element_by_css_selector(".ctl00_ContentPlaceHolder1_btn_submit").click()

# Get rows
list_of_rows = driver.find_elements_by_css_selector("#table-responsive > table > tbody > tr")
list_of_rows.pop(0)
num_rows = len(list_of_rows)

# split rows into events
list_of_events = []
for first_row, second_row in zip(list_of_rows[0::2], list_of_rows[1::2]):
    list_of_events.append((first_row, second_row))

# get list of javascript commands
list_of_javascript = []
for tup in list_of_events:
    first_row = tup[0]
    second_row = tup[1]

    # check if already scheduled
    setup = first_row.find_element_by_css_selector("td:nth-of-type(7)")
    checkin = first_row.find_element_by_css_selector("td:nth-of-type(8)")
    teardown = first_row.find_element_by_css_selector("td:nth-of-type(9)")

    if setup == "&nbsp" or checkin == "&nbsp" or teardown == "&nbsp"
        break

    # get javascript command to go to page
    command = first_row.find_element_by_css_selector("td:nth-of-type(5) > a").get_attribute("href")
    splitted_command = command.split(:)
    list_of_javascript.append(splitted_command[1])

# go to event and schedule
for command in list_of_javascript
    driver.execute_script(command)




time.sleep(30)

driver.quit()
