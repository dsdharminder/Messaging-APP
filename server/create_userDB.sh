#!/bin/bash
#This script will cause sqlite3 to run createLogins.sql in a new empty database 
#To use new_db within the application, rename db file and edit server.ini accordingly. 
sqlite3 new_db < createLogins.sql
