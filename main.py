import time
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

# Enable browser logging.
# This is to pull the JSON from console.log to the python window.
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
browser = webdriver.Chrome('chromedriver.exe', desired_capabilities=d)

browser.get("http://nextride.brampton.ca/RealTime.aspx")

browser.execute_script("window.alert=function alert(){};")

time.sleep(2.5)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_navFindByRoute').click(); ")
time.sleep(1)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_DropDownRoute').val('501004'); ")
time.sleep(1)
browser.execute_script(" __doPostBack('ctl00$mainPanel$MainPanel1$SearchStop1$DropDownRoute','') ")
time.sleep(1)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_DropDownStop').val('4003'); ")
time.sleep(1)
browser.execute_script(open("./set_BusJson-inject.js").read())
time.sleep(1)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_imgbtnSelectStop').click() ")

html_source = browser.page_source

def execPostBack():
    # Call it every 30s (vs. 60s with timeout after 10min with original code)
    threading.Timer(30.0, hello_world).start()
    browser.execute_script(" __doPostBack('ctl00$mainPanel$MainPanel1$MapControl2', 'rtBuses$43.72082550667789|-79.71744833758385|43.71694843060325|-79.72400365641624|500|611|17|4003|'); ")
    # Wait for response before trying to grab it.
    print("Executed PostBack successfully! Wait 7s for log response.")
    time.sleep(7)
    getConsoleLog = browser.get_log('browser')
    if str(getConsoleLog) == '[]':
        pass
    else:
        print(getConsoleLog)

execPostBack()
