from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import getpass

# prompt W2W username/password
#input_w2w_username = input("Enter W2W username: ")
#input_w2w_password = getpass.getpass("Enter W2W password: ")

#prompt EMS username/password
#input_ems_username = input("Enter EMS username: ")
#input_ems_passsword = getpass.getpass("Enter EMS password")

#prompt date

input_w2w_username = "yun.112"
input_w2w_password = "Syun6645"
input_ems_username = "yun.112"
input_ems_password = "Trollface9"

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
    input_year += 2000

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

name_date = name_month + "-" + input_day

# start Chrome and navigate to W2W
driver = webdriver.Chrome()
driver.get('http://www.whentowork.com');

# click to log in
driver.find_element_by_xpath("/html/body/table[1]/tbody/tr/td[2]/table/tbody/tr[1]/td[3]/a").click()

# if not logged in, log in.
if driver.title == "W2W Sign In - WhenToWork Online Employee Scheduling Program":
    inputUser = driver.find_element_by_name("UserId1")
    inputUser.send_keys(input_w2w_username);

    inputPass = driver.find_element_by_name("Password1")
    inputPass.send_keys(input_w2w_password);
    inputPass.submit();

if driver.title == "Sign In - WhenToWork Online Employee Scheduling Program":
    raise RuntimeError("Invalid W2W credentials")

# navigate to Everyone's Schedule
click = driver.find_element_by_xpath("/html/body/div[2]/table/tbody/tr/td[2]/table/tbody/tr[2]/td").click()

# save current window handle
current_window = driver.current_window_handle

#open date picker and select date
click = driver.find_element_by_xpath("//*[@id=\"calbtn\"]/nobr/a[4]").click()
driver.switch_to.window(driver.window_handles[-1])
driver.execute_script("var y = " + input_year + "; var m = " + input_month + "; var d = " + input_day + ";if (window.opener.top) {window.opener.top.location=window.opener.top.location+\"&Date=\"+m + \"/\" + d + \"/\" + y;}self.close();")
driver.switch_to.window(current_window)

# Filter by My Positions (ASSUMES I HAVE MANAGER AND SHIFT LEAD)
select = Select(driver.find_element_by_name("EmpListSkill"))
select.select_by_visible_text("My Positions")

# Get correct column number by date
dateRow = driver.find_element_by_xpath("/html/body/div[4]/table[2]/tbody/tr[2]/td/table/tbody/tr/td/table[1]/tbody/tr")
tds = dateRow.find_elements_by_tag_name("td")
i = 0;
colNum = 0;
for x in tds:
    try:
        a = x.find_element_by_partial_link_text(name_date)
        colNum = i
        i += 1
    except Exception:
        i += 1

print(colNum)

time.sleep(30)

driver.quit()
