#!/bin/bash
# Script to install requirements for the Ohio Union EMS Autofill Tool. This
# script only runs on Mac (tested against OS X 10.11.6 El Capitan). If you're
# on a different platform (Windows/Linux), see README for manual installation.
#
# usage: ./installation.sh [-flags]
#
# Options:
#           -p: Skip pulling from repo
#           -i: Skip installations
#           -r: Reinstall dependencies
#           -v: verbose
#           -h: help

#!/bin/bash

function spinner {
  pid=$!
  # If this script is killed, kill process
  trap "sudo kill $pid 2> /dev/null" EXIT
  i=0
  sp='/-\|'
  n=${#sp}
  while sudo kill -0 $pid 2> /dev/null;do printf '\b%s' "${sp:i++%n:1}";sleep .1;done
  # Disable the trap on a normal exit.
  trap - EXIT
}

function install_git_verbose {
    cd $DIR/tmp
    curl -L https://sourceforge.net/projects/git-osx-installer/files/latest/download?source=files -o git.dmg\
    MOUNTPOINT="/Volumes/MountPoint"
    hdiutil attach -mountpoint $MOUNTPOINT git.dmg

    cp $MOUNTPOINT/*.pkg git.pkg

    hdiutil detach $MOUNTPOINT
    sudo installer -pkg git.pkg -target /
    cd $DIR
}

function install_git_silent {
    cd $DIR/tmp
    curl -sL https://sourceforge.net/projects/git-osx-installer/files/latest/download?source=files -o git.dmg &
    spinner
    MOUNTPOINT="/Volumes/MountPoint"
    hdiutil attach -quiet -mountpoint $MOUNTPOINT git.dmg &
    spinner
    cp $MOUNTPOINT/*.pkg git.pkg
    hdiutil detach $MOUNTPOINT -quiet
    sudo installer -pkg git.pkg -target / 1> /dev/null&
    spinner
    cd $DIR
}

function install_git {
    if $verbose
    then
        install_git_verbose
    else
        install_git_silent
    fi
}

function install_python_verbose {
    cd $DIR/tmp
    download_link="https://www.python.org/ftp/python/3.5.2/python-3.5.2-macosx10.6.pkg" #replace with latest link
    curl $download_link -o python3.pkg
    sudo installer -pkg python3.pkg -target /
    cd $DIR
}

function install_python_silent {
    cd $DIR/tmp
    download_link="https://www.python.org/ftp/python/3.5.2/python-3.5.2-macosx10.6.pkg" #replace with latest link
    curl $download_link -so python3.pkg &
    spinner
    sudo installer -pkg python3.pkg -target / 1> /dev/null&
    spinner
    cd $DIR
}

function install_python {
    if $verbose
    then
        install_python_verbose
    else
        install_python_silent
    fi
}

function install_pip_verbose {
    cd $DIR/tmp
    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    pip3 install --upgrade pip
    cd $DIR
}

function install_pip_silent {
    cd $DIR/tmp
    curl -sO https://bootstrap.pypa.io/get-pip.py &
    spinner
    python3 get-pip.py -q &
    spinner
    yes | pip3 install --upgrade pip 1> /dev/null &
    spinner
    cd $DIR
}

function install_pip {
    if $verbose
    then
        install_pip_verbose
    else
        install_pip_silent
    fi
}

function install_chromedriver_verbose {
    latest=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    download_location="http://chromedriver.storage.googleapis.com/$latest/chromedriver_mac64.zip"
    cd $DIR/tmp
    curl -O $download_location
    unzip chromedriver_mac64.zip
    mv -f ./chromedriver $HOME/chromedriver/chromedriver
    cd $HOME
    chmod u+x ./chromedriver/chromedriver

    # if the latest version of chromedriver isn't in PATH, add it to path
    if ! chromedriver --version 2>&1 | grep -q $latest
    then
        echo export PATH=$PWD/chromedriver:$PATH > ~/.bash_profile
	
    fi
    cd $DIR
}

function install_chromedriver_silent {
    latest=$(curl -s http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
    download_location="http://chromedriver.storage.googleapis.com/$latest/chromedriver_mac64.zip"
    cd $DIR/tmp
    curl -s -O $download_location &
    spinner
    unzip -qq chromedriver_mac64.zip &
    spinner
    mv -f ./chromedriver $HOME/chromedriver/chromedriver
    cd $HOME
    chmod u+x ./chromedriver/chromedriver

    # if the latest version of chromedriver isn't in PATH, add it to path
    if ! chromedriver --version 2>&1 | grep -q $latest
    then
        echo export PATH=$PWD/chromedriver:$PATH > ~/.bash_profile
	. ~/.bash_profile
    fi
    cd $DIR
}

function install_chromedriver {
    if $verbose
    then
        install_chromedriver_verbose
    else
        install_chromedriver_silent
    fi
}

function reinstall_dependencies {
    echo -n "Reinstalling Git... "
    install_git
    echo "OK"

    echo -n "Reinstalling Python3... "
    install_python
    echo "OK"

    echo -n "Reinstalling Pip3... "
    install_pip
    echo "OK"

    echo -n "Reinstalling ChromeDriver... "
    install_chromedriver
    echo "OK"
}

function check_for_dependencies {
    # Need to install the tools if they are not found on the machine
    echo -n "Checking if Git is installed... "
    if ! git --version >/dev/null 2>&1
    then
        echo ""
        echo -n "    git not found. Downloading latest version... "
        install_git
    fi
    echo "OK"

    echo -n "Checking if Python3 is installed... "
    if ! python3 --version >/dev/null 2>&1
    then
        echo ""
        echo -n "    python3 not found. Downloading..."
        install_python
    fi
    echo "OK"

    echo -n "Checking if Pip3 is installed... "
    if ! pip3 --version >/dev/null 2>&1
    then
        echo ""
        echo -n "    pip3 not found. Downloading..."
        install_pip
    fi
    echo "OK"

    echo -n "Checking if ChromeDriver is installed... "
    if ! chromedriver --version >/dev/null 2>&1
    then
        echo ""
        echo -n "    chromedriver not found. Checking if chromedriver exists in ~/chromedriver/... "
        if [ -f $HOME/chromedriver/chromedriver ]
        then
            echo ""
            echo -n "        chromedriver exists in $HOME/chromedriver/. Checking if latest version... "
            cd ~/chromedriver
            if ! ./chromedriver --version 2>&1 | grep -q $latest
            then
                echo -n "            chromedriver is an old version. Downloading latest version... "
                install_chromedriver
            else
                echo -n "            chromedriver is current version. Exporting PATH... "
                echo export PATH=$PWD:$PATH > .bash_profile
            fi
        else
            echo ""
            echo -n "        chromedriver doesn't exist in ~/chromedriver/. Downloading latest version... "
            install_chromedriver
        fi
    fi
    echo "OK"
}

function get_path {

    # Need to prompt the user for the installation - default to home dir
    default_path="$HOME"
    echo -n "Enter the installation path [default: $default_path/] > "
    read user_path

    if [ -z "${user_path}" ]
     then
        user_path=$default_path/
    fi

    user_path="${user_path/#\~/$HOME}"

    echo "Path is $user_path"
    echo ""
}

function pull_branches {
    QUIET=""
    if ! $verbose
    then
        QUIET="-q"
    fi

    echo -n "Cloning Repository... "
    if [ ! -d $user_path/Ohio-Union-EMS-Autofill-Tool ]
    then
        cd $user_path
        git clone $QUIET https://github.com/samyun/Ohio-Union-EMS-Autofill-Tool.git
        if [ $? -ne 0 ]; then
            exit 1
        fi
    else
        echo ""
        echo -n "    Repository already exists. Updating... "
        cd $user_path/Ohio-Union-EMS-Autofill-Tool
        git pull $QUIET
        if [ $? -ne 0 ]; then
            echo -n "Do you want to continue anyways (y/n)? "
            read CONTINUE
            if [ ! $CONTINUE = "y" ]
            then
                exit 1
            fi
        else
            echo "OK"
        fi
    fi
}

# Get options
reinstall='false' #reinstall all dependencies
skipPulls='false' #skip repo pulls
skipInstalls='false' #skip installations
verbose='false' #verbose

while getopts ":rpivh" optname
  do
    case "$optname" in
      "r")
        reinstall='true'
        ;;
      "p")
        skipPulls='true'
        ;;
      "i")
        skipInstalls='true'
        ;;
      "v")
        verbose='true'
        ;;
      "h")
        echo "usage: ./installation.sh [-flags]"
        echo "    Script to check and install dependencies for the Ohio Union EMS tools"
        echo ""
        echo "    Options:"
        echo "          -p: Skip pulling from repo"
        echo "          -i: Skip installations"
        echo "          -r: Reinstall dependencies"
        echo "          -v: verbose"
        echo "          -h: help"
        exit 1
        ;;
      "?")
        echo "Unknown option $OPTARG"
        exit 1
        ;;
      *)
      # Should not occur
        echo "Unknown error while processing options"
        ;;
    esac
done

# Need to check the OS type here
sudo clear
echo -n "Checking OS type... "
if [[ "$OSTYPE" != "darwin"* ]]
then
    echo "Only OSX is supported at this time."
    exit 1
fi
echo "OK"

# Store PWD
DIR=$PWD

# If -i flag is set, skip installs
if ! $skipInstalls
then
    # Check if folders exist
    if [ -d "tmp" ]
    then
        echo -n "Removing old tmp folder... "
        rm -r tmp
        echo "OK"
    fi
    echo -n "Creating tmp folder... "
    mkdir tmp
    echo "OK"

    if [ ! -d "$HOME/chromedriver" ]
    then
        echo -n "Creating chromedriver folder... "
        mkdir $HOME/chromedriver
        echo "OK"
    fi

    # If -r flag is set, reinstall all components
    if $reinstall
    then
        reinstall_dependencies
    else
        check_for_dependencies
    fi

    echo -n "Removing tmp folder... "
    rm -r tmp
    echo "OK"
fi

get_path

# If -p flags are set, skip repo pulls
if ! $skipPulls
then
    pull_branches
fi

# Selenium
if $verbose
then
    pip3 install -U selenium #update selenium to latest
else
    echo -n "Upgrading Selenium to latest version...  "
    yes | pip3 install -U selenium 1> /dev/null &
    spinner
    echo "OK"
fi
