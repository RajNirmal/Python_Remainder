import notify2
import signal
import os
import gi
import json
import datetime
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appIndicator3

#A library initialiser, use it to initialize libraries in the future
def initLibs():
    notify2.init("TestingApp")
    
# Pass the title and message to this function to show the notification
def showNotification(title,message):
    notification = notify2.Notification(title,message)
    notification.show()

#Fn to call before calling showAppIndicator to add the quit button
def buildMenu():
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    MenuData.append(item_quit)
    MenuData.show_all()

#Fn to add data to the app indicator
def addMenuItem(title):
    item = gtk.MenuItem(title)
    MenuData.append(item)

#Defines the function of quit button
def quit(source):
    gtk.main_quit()

#Call to show the app indicator
def showAppIndicator():
    signal.signal(signal.SIGINT,signal.SIG_DFL)
    indicator = appIndicator3.Indicator.new(APP_INDICATOR,os.path.abspath('alarm.svg'),appIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appIndicator3.IndicatorStatus.ACTIVE)
    indicator.set_menu(MenuData)
    gtk.main()

#Returns true if the bill date is nearby
def notificationFlag(date):
    now = datetime.datetime.now().day
    rangeOfDates = range(int(date)-3,int(date)+3)
    if now in rangeOfDates:
        return True
    else:
        return False

#Reads the JSON file and shows the notification and app indicator if necessary
def readFile():
    count = 0
    allBills = json.loads(open("items.json").read())
    for json_item in allBills[JARRAY_IDENTIFIER]:
        if(notificationFlag(json_item[JSON_BILL_DATE])):
            name = json_item[JSON_BILL_NAME]
            desc = json_item[JSON_BILL_DESCRIPTION] + "\npay by date " + json_item[JSON_BILL_DATE]
            nameWithDate  = json_item[JSON_BILL_NAME] + " pay by date "+json_item[JSON_BILL_DATE]
            showNotification(name,desc)
            addMenuItem(nameWithDate)
            count = count + 1
        else:
            #Do nothing, thinking of a better implementation of this function
            _ = 1
    if(count > 0):
        buildMenu()
        showAppIndicator()

#App constants
APP_INDICATOR = "myAppIndicatorId"
JARRAY_IDENTIFIER = "Bills"
JSON_BILL_NAME = "Title"
JSON_BILL_DESCRIPTION = "Description"
JSON_BILL_DATE = "DueDate"

#Menu Data
MenuData = gtk.Menu()

# Main Function
initLibs()
readFile()

