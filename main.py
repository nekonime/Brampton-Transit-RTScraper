import time
import threading
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

# Enable browser logging.
# This is to pull the JSON from console.log to the python window.
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }
browser = webdriver.Chrome('chromedriver.exe', desired_capabilities=d)

# Specify the route and destination stop number here.
# For example, 501 Zum Queen WEST is route value 500104. The final stop is Downtown Brampton Terminal, stop number 4020
routeValue = '501004'
routeFinalStop = '4020'

browser.get("http://nextride.brampton.ca/RealTime.aspx")
# Attempt to supress the STUPID 'minX undefined' alert message.
########## browser.execute_script("window.alert = function() {};") ##########
# If an alert showed up while this script was in the middle of executing, Python would freak out and disconnect from the browser
# So, the backup plan.
time.sleep(3)
try:
    browser.switch_to.alert.accept()
except:
    pass

# Sleep between every exec to allow for page to load.
# Probably should make them longer. 1.5s maybe.
time.sleep(2.5)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_navFindByRoute').click(); ")
time.sleep(1)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_DropDownRoute').val('" + routeValue + "'); ")
time.sleep(1)
browser.execute_script(" __doPostBack('ctl00$mainPanel$MainPanel1$SearchStop1$DropDownRoute','') ")
time.sleep(1)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_DropDownStop').val('" + routeFinalStop + "'); ")
time.sleep(1)
browser.execute_script(open("./set_BusJson-inject.js").read())
time.sleep(1)
browser.execute_script(" $('#ctl00_mainPanel_MainPanel1_SearchStop1_imgbtnSelectStop').click() ")

html_source = browser.page_source

def execPostBack():
    # Call it every 30s (vs. 60s that times out after 10min with original code)
    threading.Timer(30.0, execPostBack).start()
    browser.execute_script(" __doPostBack('ctl00$mainPanel$MainPanel1$MapControl2', 'rtBuses$43.72082550667789|-79.71744833758385|43.71694843060325|-79.72400365641624|500|611|17|4003|'); ")
    # Wait for response before trying to grab it.
    print("Executed PostBack successfully! Wait 7s for log response.")
    time.sleep(7)
    getConsoleLog = browser.get_log('browser')
    if str(getConsoleLog) == '[]':
        pass
    else:
        # NOTE: The output will also include other messages such as Google API errors. This should be easy to parse out though.
        f = open('logOutput.json', 'w')
        f.write(str(getConsoleLog))
        f.close

execPostBack()
