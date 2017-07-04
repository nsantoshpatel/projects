import json
import os
import pynotify
import sys
import time

from git.projects.notifications.lib import googlefinance

debug       = 1
notifyWait  = 15
frequency   = 60
currentPath = os.getcwd()
if debug: print "[DEBUG] Current Path: ", currentPath

def showNotification(header, body="", icon=""):
    pynotify.init("Notification")
    notify = pynotify.Notification(header, body, currentPath+"/"+icon)
    notify.show()
    count = notifyWait
    if debug: print "[DEBUG] Wait for notification to clear"
    while count > 0:
        time.sleep(1)
        if debug: sys.stderr.write("*")
        count -=1

class googleAPI():
    def __init__(self):
        self.baseUrl = "http://finance.google.com/finance/info?client=ig&q="
        self.keyValueMap = {
            u'id'     : u'ID',
            u't'      : u'StockSymbol',
            u'e'      : u'Index',
            u'l'      : u'LastTradePrice',
            u'l_cur'  : u'LastTradeWithCurrency',
            u'ltt'    : u'LastTradeTime',
            u'lt_dts' : u'LastTradeDateTime',
            u'lt'     : u'LastTradeDateTimeLong',
            u'div'    : u'Dividend',
            u'yld'    : u'Yield'
        }

    def get(self, stockName):
        a = googlefinance.getQuotes(stockName)
        if debug: print "[DEBUG] GoogleAPI Response:\n", json.dumps(a, indent=2)
        try:
            return a[0]['LastTradePrice']
        except:
            showNotification("ERROR: GoogleAPI.get()", "'LastTradePrice' not found in API Response", "error.png")
            return -1

class yahooAPI():
    def __init__(self):
        self.baseUrl = "http://finance.yahoo.com/d/quotes.csv?f=sl1d1t1c1ohgv&s="

    # def get(self, stockName):


stock = "MRVL"
X = googleAPI()
prevQuote = 0
while True:
    currQuote = X.get(stock)
    if currQuote != -1:
        currTime = time.strftime("[%I:%M:%S %p]")
        if   prevQuote == 0:         iconToDisplay = ""
        elif prevQuote  < currQuote: iconToDisplay = "up2.png"
        elif prevQuote  > currQuote: iconToDisplay = "down2.png"
        elif prevQuote == currQuote: iconToDisplay = "equal.png"
        showNotification(stock, currTime + " Price: "+currQuote, iconToDisplay)
        if debug: print "\n[DEBUG] "+ currTime + " Quote: ",currQuote
    prevQuote = currQuote
    time.sleep(frequency - notifyWait)


# import requests
# a = requests.get("http://finance.google.com/finance/info?client=ig&q=AAPL,goog")
# print a.raise_for_status()
# print a.url
# print a.text
