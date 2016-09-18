# OhioUnionEMSAutofillTool

This is a tool to auto-fill the EMS paperwork for the Ohio Union AV 
managers. This tool is provided as-is and is under active development.

## Installation
1. Install Python3
2. Install pip3
3. Download ChromeDriver and add to PATH
4. Clone this repo

## How to Run
 - Make sure dependencies are installed
 - Edit settings.json
    - Enter first name, last name, EMS credentials, etc
 - Edit config.json
    - Enter the information for the workers 
 - In Terminal/Command Prompt, call: 
    python3 ~/{...}/EMS\ Paperwork\ Tool/EMS_login.py

## To-Do
 - test with late events (ending 12:00 AM or later)
 - test with shift leads
 - make the js pulls faster
 - progress logging
 - skip events with no AV (why is this a thing?)
 - create easy to read file for setups