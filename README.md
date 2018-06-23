![Heroku](https://heroku-badge.herokuapp.com/?app=timecandle)
# Time Candle. #
##### little app about your time and life #####
This is a very simple task-tracker application that can help you to manage your time. User friendly interface provides you to create tasks and projects and use them very fast with your friends and colleagues.
## Architecture ##
For information about architecture please check Logical_View.jpg file.

## How to install? ##

### Make sure you have installed setuptools: ###
```bash
$ pip3 install -U pip setuptools 
```

### Installing time candle lib ###
First you need to install library time_candle to use console or web version, because of dependencies 
```bash
$ cd tc_lib
$ python3 setup.py install
```

### Running tests: ###
```bash
$ python3 -m unittest 
```

### Installing command line interface for time candle ###
After installing the main time candle lib you may use it from command line, if you'll do the following steps:
```bash
$ cd tc_cli
$ python3 setup.py install
```
Also be sure, that you have installed xcowsay to print whoami if you are on linux:
```bash
$ sudo apt install xcowsay
```

## How to use? ##
```bash
$ python3 -m tc_cli -h
```
This command will show you the main commands for this app from command line.
Also note that you may configure app by settings file, passing needed path's for you. 

For information about how to use library in your own application check the commands module of controller package  

Made by Paul Fon Boudervill.
