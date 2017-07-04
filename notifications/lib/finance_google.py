import json, sys

try:
    from urllib.request import Request, urlopen, HTTPError
except ImportError:  # python 2
    from urllib2 import Request, urlopen, HTTPError

# YahooURL = "http://finance.yahoo.com/d/quotes.csv?f=sl1d1t1c1ohgv&s="

googleFinanceKeyToFullName = {
    u'id'     : u'ID',
    u't'      : u'StockSymbol',
    u'e'      : u'Index',
    u'l'      : u'LastTradePrice',
    u'lt_dts' : u'LastTradeDateTime',
    u'c'      : u'ChangeValue',
    u'cp'     : u'ChangePercentage'
}

def buildUrl(symbols):
    symbol_list = ','.join([symbol for symbol in symbols])
    # a deprecated but still active & correct api
    return 'http://finance.google.com/finance/info?client=ig&q=' \
        + symbol_list

def request(symbols):
    url = buildUrl(symbols)
    print('URL: '+ url)
    req = Request(url)
    try:
        resp = urlopen(req)
    except HTTPError as e:
        print('FAIL: Invalid URL Response: {}'.format(e)); return 'FAIL'
    print('Response Code: {}'.format(resp.getcode()))
    # remove special symbols such as the pound symbol
    content = resp.read().decode('ascii', 'ignore').strip()
    content = content[3:]
    print('Response: '+ content)
    return content

def replaceKeys(quotes):
    global googleFinanceKeyToFullName
    print('Parse JSON Response and Map Values')
    quotesWithReadableKey = []
    for q in quotes:
        qReadableKey = {}
        for k in googleFinanceKeyToFullName:
            try:
                qReadableKey[googleFinanceKeyToFullName[k]] = q[k]
            except:
                pass
        quotesWithReadableKey.append(qReadableKey)
        print('Parsed: '+ qReadableKey['StockSymbol'] +':'+ qReadableKey['LastTradePrice'])
    return quotesWithReadableKey

def getQuotes(symbols):
    if type(symbols) == type('str'):
        symbols = [symbols]
    res = request(symbols)
    if not res == "FAIL":
        try:
            content = json.loads(res)
        except:
            print('FAIL: Cannot Get QUOTE: {}'.format(symbols)); return []
        return replaceKeys(content)
    return []

if __name__ == '__main__':
    try:
        symbols = sys.argv[1]
    except:
        symbols = "NSE%3ASBIN"

    symbols = symbols.split(',')
    print(json.dumps(getQuotes(symbols), indent=2))
