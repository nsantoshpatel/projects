__author__ = "nsantoshpatel"

import time
from lib import notify
from lib.finance_google import getQuotes

# Get StockList from file
wFilename = 'watchlist'
try:
    stockList = open(wFilename, 'r').read().splitlines()
except IOError:
    print('FAIL: File:{} not found'.format(wFilename))
    exit(1)

# Get Real time Quotes of all the stocks
quoteList = getQuotes(stockList)

# Notify user about Current Quote Values
notifyObjList = {}
for stock in quoteList:
    notifyObjList[stock['StockSymbol']] = notify()
    notifyObjList[stock['StockSymbol']].popup(stock['StockSymbol'], stock['LastTradePrice'])

time.sleep(10)
for n in notifyObjList: n.close()