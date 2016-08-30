from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass
import sys
import os

#print instructions
print("This is a Python script to auto-populate EMS for Ohio Union AV Managers.")
print("This is provided unoffically and it may break due to EMS web tool changes.")
print("Let me know (yun.112) if you notice any issues with this script.")
print("I take no responsibility for any errors or issues.")
print("")
print("*** You must check each event after the script is finished. It will not")
print("populate large event spaces automatically. ***")
print("************************************************************************")
print("Instructions:")
print("The script will ask you to enter your EMS username and password.")
print("Then it'll ask for the date and latest time to schedule you for the next")
print("day's setups.")
print("Then it'll ask for the number of manager, lead, and tech shifts, ")
print("followed by the name and time span of each shift.")
print(" - number of shifts: number of shifts of that type per day. ")
print(" - name: name of person. Prompt for First, then Last. ")
print(" - time span: time span of shift. Prompt for starting time then ending time.")
print("");
print("eg: Tech Alpha works 7am-2pm, Tech Bravo works 2pm-12am")
print("Lead Echo works 6:30am-3pm, Lead Foxtrot works 3pm-10pm")
print("Manager Sierra works 7pm-12am")
print("2 Tech shifts, Tech/Alpha/7:00/14:00, Tech/Bravo/14:00/00:00")
print("2 Lead shifts, Lead/Echo/6:30/15:00, Lead/Foxtrot/15:00/22:00")
print("1 Manager shift, Manager/Sierra/19:00/00:00")

input_continue = input("Continue? (Y/n)")
if input_continue != "Y" and input_continue != "y" and input_continue != "yes" and input_continue != "Yes" and input_continue != "YES":
    sys.exit()

#windows
os.system('cls')

#osx/linux
#os.system('clear')

#prompt EMS username/password
input_ems_username = input("Enter EMS username: ")
input_ems_passsword = getpass.getpass("Enter EMS password")

#prompt date
validDate = 0;
while not validDate:
    try:
        input_date = input("Enter date (eg May 9 2016 = \"5/9/2016\"): ")
        #input_date = "5/23/2016"

        # parse date
        date_list = input_date.split("/")
        input_month = date_list[0]
        input_day = date_list[1]
        input_year = date_list[2];
        if int(input_month) < 1 or int(input_month) > 12:
            raise Exception("Invalid month: " + input_month)
        elif int(input_day) < 1 or int(input_day) > 31:
            raise Exception("Invalid day: " + input_day)
        elif int(input_year) < 0 or int(input_year) > 2099 or (int(input_year) < 2000 and int(input_year) > 99):
            raise Exception("Invalid year: " + input_year)

        validDate = 1
    except Exception:
        print("Invalid date entry")

# if two digit year, convert to 4 digit year.
if int(input_year) < 2000:
    input_year = int(input_year) + 2000

if input_month == "1":
    name_month = "Jan"
elif input_month == "2":
    name_month = "Feb"
elif input_month == "3":
    name_month = "Mar"
elif input_month == "4":
    name_month = "Apr"
elif input_month == "5":
    name_month = "May"
elif input_month == "6":
    name_month = "Jun"
elif input_month == "7":
    name_month = "Jul"
elif input_month == "8":
    name_month = "Aug"
elif input_month == "9":
    name_month = "Sep"
elif input_month == "10":
    name_month = "Oct"
elif input_month == "11":
    name_month = "Nov"
else:
    name_month = "Dec"

# get latest time to schedule setup today
input_latest_time = input("Enter the latest time you should do setups for tomorrow, eg 10:00: ")

# get number of managers, the names and the times
input_num_mgr = input("Enter the number of manager shifts: ")
list_mgr = []
for i in range (0, int(input_num_mgr)):
    input_first = input("Enter Manager " + str(i+1) +"'s first name: ")
    input_last = input("Enter Manager " + str(i+1) +"'s last name: ")
    input_time_start = input("Enter Manager " + str(i+1) +"'s start time (5:30pm = 17:30): ")
    input_time_end = input("Enter Manager " + str(i+1) +"'s end time (5:30pm = 17:30): ")
    tup = (input_first, input_last, input_time_start, input_time_end)
    list_mgr.append(tup)
    print("")

# get number of shift leads, the names and the times
input_num_lead = input("Enter the number of shift lead shifts: ")
list_lead = []
for i in range (0, int(input_num_lead)):
    input_first = input("Enter Shift Lead " + str(i+1) +"'s first name: ")
    input_last = input("Enter Shift Lead " + str(i+1) +"'s last name: ")
    input_time_start = input("Enter Shift Lead " + str(i+1) +"'s start time (5:30pm = 17:30): ")
    input_time_end = input("Enter Shift Lead " + str(i+1) +"'s end time (5:30pm = 17:30): ")
    tup = (input_first, input_last, input_time_start, input_time_end)
    list_lead.append(tup)
    print("")


# get number of techs, the names and the times
input_num_tech = input("Enter the number of tech shifts: ")
list_tech = []
for i in range (0, int(input_num_tech)):
    input_first = input("Enter Tech " + str(i+1) +"'s first name: ")
    input_last = input("Enter Tech " + str(i+1) +"'s last name: ")
    input_time_start = input("Enter Tech " + str(i+1) +"'s start time (5:30pm = 17:30): ")
    input_time_end = input("Enter Tech " + str(i+1) +"'s end time (5:30pm = 17:30): ")
    tup = (input_first, input_last, input_time_start, input_time_end)
    list_tech.append(tup)
    print("")

# start Chrome and navigate to W2W
driver = webdriver.Chrome()
driver.get('http://ohiounion.osu.edu/ems');

# if not logged in, log in.
if driver.title == "Login Required | The Ohio State University":
    inputUser = driver.find_element_by_xpath("//*[@id=\"username\"]")
    inputUser.send_keys(input_ems_username);

    inputPass = driver.find_element_by_xpath("//*[@id=\"password\"]")
    inputPass.send_keys(input_ems_password);
    inputPass.send_keys(u'\ue007');

if driver.title == "Login Required | The Ohio State University":
    raise RuntimeError("Invalid EMS credentials")

# Log in as manager
select = Select(driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder1_ddl_position\"]"))
select.select_by_visible_text("Student Manager - AV")
submitButton = driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder1_btn_submit\"]").send_keys(u'\ue007');

# Go to date
datePicker = driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder1_txt_date\"]").clear()
datePicker = driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder1_txt_date\"]")
datePicker.send_keys(str(input_month) + "/" + str(input_day) + "/" + str(input_year))
submitButton = driver.find_element_by_xpath("//*[@id=\"ctl00_ContentPlaceHolder1_btn_submit\"]").send_keys(u'\ue007');



time.sleep(30)

driver.quit()
