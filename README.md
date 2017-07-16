# Ohio Union EMS Autofill Tool

This is a tool to auto-fill the EMS paperwork for the Ohio Union AV managers. This tool is provided as-is and is under
active development.

## Table of Contents
* [Installation](#installation)
   * [Python3](#python3)
   * [Pip3](#pip3)
   * [Selenium](#selenium)
   * [Google Chrome](#google-chrome)
   * [ChromeDriver](#chromedriver)
   * [EMS.Paperwork.Tool.zip](#ems.paperwork.tool.zip)
* [macOS Installation Script](#macos-installation-script)
* [Background](#background)
* [How to Run](#how-to-run)
* [settings.json](#settings.json)
* [To-Do](#to-do)

## Installation
Mac users: See [macOS Installation Script](#macos-installation-script) for an automated installation, or follow the 
manual steps below.

#### Python3
Python is the scripting language that the autofill tool is written in. There are two versions of Python: Python 2.x 
and Python 3.x which are incompatible with each other. This tool is written in Python 3. It's been tested with version 
3.4 and later.
   1. Download and install the latest version of Python 3
      * ([Windows](https://www.python.org/downloads/windows/ "Python for Windows")):
         1. I recommend installing to <code>C:\python3</code> instead of the installer default
         2. Check the box to install for all users and Add to PATH.
      * ([macOS](https://www.python.org/downloads/mac-osx/ "Python for macOS")):
         1. Install normally
   2. Ensure Python is added to PATH
      * Windows:
         1. Launch Command Prompt
         2. Type <code>python --version</code>
         3. If the output is not <code>Python 3.x.x</code> (e.g. <code>'python' is not recognized as an internal 
         or external command, operable program or batch file.</code> or <code>Python 2.7.x</code>):
            1. Click Start, type <code>environment variables</code> and click on "Edit environment variables for your 
            account"
            2. Under <code>System variables</code>, look for <code>Path</code>, and double click on it
            3. Add a new entry with path <code>C:\python3</code> and another with path <code>C:\python3\Scripts</code> 
            or the other installation path from Step 1.
            4. Move those entries to the top.
            5. If double-clicking on <code>Path</code> launched a box with a single text box, type 
            <code>C:\python3;C:\python3\Scripts;</code> to the beginning of the text box. Make sure the <code>;</code> 
            is at the end.
            6. NOTE: If the output of <code>python --version</code> was <code>Python 2.7.x</code>, this may cause 
            any application that uses Python 2 to have issues. Consider renaming <code>python.exe</code> in 
            <code>C:\python3</code> to <code>python3.exe</code> and <code>pythonw.exe</code> to 
            <code>pythonw3.exe</code>. This will preserve compatibility with Python 2 
            applications, while Python 3 commands below will need to be run with <code>python3</code> instead of 
            <code>python</code>
            7. Exit and relaunch Command Prompt, and verify <code>python --version</code> returns 
            <code>Python 3.x.x</code>. If it doesn't, double check your steps.
      * macOS:
         1. Launch Terminal
         2. Type <code>python3 --version</code>
         3. If the output is not <code>Python 3.x.x</code> (e.g. <code>-bash: python: command not found</code>), type 
         the following commands in Terminal:
            1. Type <code>cd ~</code>
            2. Type <code>nano .bash_profile</code>
            3. If there's a line starting with <code>export PATH=</code>, right after <code>export PATH=</code>, 
            type <code>/usr/local/bin/:</code>, so the line now looks like 
               <code>export PATH=/usr/local/bin:[...]</code>
            4. Otherwise, on a new blank line, type 
            <code>export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</code>
            5. Inside the Terminal window with <code>nano .bash_profile</code> open, type <code>ctrl + X</code> to 
            exit nano, then <code>Enter</code> to save, then <code>Enter</code> to save that file name.
            6. Type <code>source .bash_profile</code> to apply changes from <code>.bash_profile</code>
            7. Verify python3 is in the correct path by typing <code>python3 --version</code> and verify the output says 
            <code>Python 3.x.x</code>. If it doesn't, double check your steps.
            
##### Pip3
Pip is a Python package installer. It is used to install Python packages, specifically [Selenium](#selenium).
   1. Launch Command Prompt/Terminal
   2. Type <code>python3 -m pip install -U pip</code>. 
   3. Resolve any errors before continuing
   
##### Selenium
Selenium (WebDriver) is a web-application testing tool that automates actions on a web browser. Selenium provides the interface 
 between the Python commands and the actual websites. 
   1. Launch Command Prompt/Terminal
   2. Type <code>python3 -m pip install -U selenium</code>. 
   3. Resolve any errors before continuing
   
##### [Google Chrome](https://www.google.com/chrome/browser/desktop/index.html "Google Chrome")
Google Chrome is a popular web browser, and is the only browser supported by this tool. Other browsers could be used 
after minor modifications to the script, but that has not been tested.
   * Install the regular version of Google Chrome (not Google Chrome Canary or Chromium or Google Chrome Channels)

##### [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/ "Chromedriver")
ChromeDriver is a server that provides the interface for Selenium Webdriver to work with Google Chrome.
   1. Download the latest version of Chromedriver from link above.
   2. Extract into
      * Windows: <code>C:\chromedriver\\</code>
      * macOS: <code>/Users/%USERNAME%/chromedriver/</code> where <code>%USERNAME%</code> is your username - 
      can be found at the top of the Terminal window
   3. Only file inside <code>chromedriver/</code> should be <code>chromedriver</code>
   4. Add <code>chromedriver/</code> to PATH:
      * Windows:
         1. Click Start, type <code>environment variables</code> and click on "Edit environment variables for your 
            account"
         2. Under <code>System variables</code>, look for <code>Path</code>, and double click on it
         3. Add a new entry with path <code>C:\chromedriver</code>
         4. Move the entry to the top.
         5. If double-clicking on <code>Path</code> launched a box with a single text box, type 
         <code>C:\chromedriver;</code> to the beginning of the text box. Make sure the <code>;</code> 
         is at the end.
         6. Exit and relaunch Command Prompt
      * macOS:
         1. <code>cd ~</code>
         2. <code>nano .bash_profile</code>
         3. If there's a line starting with <code>export PATH=</code>, right after <code>export PATH=</code>, 
         type <code>/Users/%USERNAME%/chromedriver/:</code>, so the line now looks like 
         <code>export PATH=/Users/%USERNAME%/chromedriver:[...]</code>. Replace <code>%USERNAME%</code> as above.
         4. Otherwise, on a new blank line, type 
         <code>export PATH=/Users/%USERNAME%/chromedriver:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</code>
         5. Inside the Terminal window with <code>nano .bash_profile</code> open, type <code>ctrl + X</code> to 
         exit nano, then <code>Enter</code> to save, then <code>Enter</code> to save that file name.
         6. Type <code>source .bash_profile</code> to apply changes from <code>.bash_profile</code>
   5. Verify chromedriver is in the correct path by typing <code>chromedriver --version</code> and verify it returns 
         <code>ChromeDriver x.x[...]</code>. If it doesn't, double check your steps.
         
##### EMS.Paperwork.Tool.zip
This zip folder contains the autofill tool and the configuration files to run it.

Download the latest <code>EMS.Paperwork.Tool.zip</code> from 
https://github.com/samyun/Ohio-Union-EMS-Autofill-Tool/releases/latest and extract it to a new folder.

## macOS Installation Script
This installation script is for macOS only. It's been tested with a fresh installation of macOS Sierra 10.12.5.

1. Download the latest <code>installation.sh</code> from 
https://github.com/samyun/Ohio-Union-EMS-Autofill-Tool/releases/latest and save it to a location of your drive (eg 
~/)
2. Launch Terminal and navigate to the directory containing <code>installation.sh</code>
   * e.g. <code>cd ~/</code>
3. Type <code>./installation.sh [-flags]</code>
   * Flags:
      * -p: Skip pulling from repo
      * -i: Skip installations
      * -r: Reinstall dependencies
      * -v: verbose
      * -h: help
   * For a standard installation, type <code>./installation.sh</code> and follow the prompts. This will check for 
   components, install missing dependencies, and download and extract the latest release of 
   <code>EMS.Paperwork.Tool.zip</code>
   * For a developer's installation, type <code>./installation.sh -d</code> and follow the prompts. This run the same 
   as the standard installation, but it will also clone the <code>master</code> branch of the source code.

## Background
This tool was designed to allow Ohio Union AV Managers to quickly and easily complete the EMS paperwork for the next
day. Using Python3 and Selenium, an open source web browser automation tool, this tool will launch an instance of
Google Chrome, navigate to https://whentowork.com, log in, and pull the schedule for the day specified. Then the tool
will navigate to https://ohiounion.osu.edu/ems and complete the scheduling assignments based on the schedule pulled
from W2W. This tool may work with other Ohio Union manager positions by changing various settings.json attributes,
such as Production, but it is not tested.

## How to Run
 - Make sure dependencies are installed
 - Edit [settings.json](#settings.json)
    - Enter first name, last name, EMS credentials, WhenToWork credentials etc
 - In Terminal/Command Prompt, change directory to 'EMS Paperwork Tool/' and run:
    python3 autofill_tool.py

## settings.json
 - current_manager_first_name: The current manager's first name. Used to assign early-morning setups that should be
    done the night before
 - current_manager_last_name: The current manager's last name. Used to assign early-morning setups that should be
    done the night before
 - ems_username: OSU name.#
 - ems_password: OSU password
 - w2w_username: WhenToWork username
 - w2w_password: WhenToWork password
 - minutes_to_advance_setup: Amount of time prior to the event start time that setup should be scheduled. e.g: If
    event starts at 5:00 PM, "minutes_to_advance_setup" = 30 means setup time is 4:30 PM.
 - minutes_to_advance_checkin: Amount of time prior to the event start time that check-in should be scheduled. e.g: If
    event starts at 5:00 PM, "minutes_to_advance_checkin" = 15 means check-in time is 4:45 PM.
 - minutes_to_delay_teardown: Amount of time after the event end time that teardown should be scheduled. e.g: If
    event ends at 5:00 PM, "minutes_to_delay_teardown" = 30 means teardown time is 5:30 PM.
 - previous_day_setup_cutoff: The cut-off time to schedule the setup for the previous night. e.g.: If the cut-off time
    if 10:00 AM, an event that starts at 9:45 AM would be setup the night prior at "setup_time_night_before" time
    by "current_manager_last_name", "current_manager_first_name".
 - setup_time_night_before: The time to setup the event if it's set up the night prior. e.g: If the event starts
    prior to the "previous_day_setup_cutoff", and "setup_time_night_before" = 12:00 AM, the setup would be
    scheduled at 12:00 AM.
 - use_w2w: true to use WhenToWork to find the schedule. false to use a separate "schedule.json"
 - custom_date: false to use 'tomorrow's' date. true to have the script prompt for the date.
 - skip_already_scheduled: true to skip events that have either setup, check-in, or teardown already scheduled. false
    to schedule those anyways. NB: if this is set to false, it will add the schedules, even if they already exist.
 - skip_already_confirmed: true to skip events where the setup, check-in, or teardown are already scheduled. false to
    schedule those events anyways.
 - skip_events_with_no_av: true to schedule events where the "A/V Equipment" section is "None Found". false to
    schedule those events anyways.
 - skip_rooms: true to skip events that are in one of the rooms in "skip_following_rooms". false to schedule those
    events anyways.
 - manager_position: The name of the manager position that appears in https://ohiounion.osu.edu/ems that should be used
 - order_to_assign_general_shift: The order to schedule events. These are the positions in the W2W headers. eg. If
    the order is "A", "B", "C", the script will try to schedule an "A" first. If there are no A's, it will try to
    schedule a "B". If there are no A's nor B's, the script will try to schedule a "C". If there are no A's, B's,
    nor C's, it will skip assignment for that time only.
 - skip_following_rooms: The rooms to skip if "skip_rooms" is true.

## To-Do
 - create reports for shift-leads
 - better installation package
 - auto-confirm shifts