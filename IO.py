from HelperFunctions import getLogger
from urllib import request
from time import time
import sqlite3
import Settings

localLogger = getLogger()

def getTextFile(path):
    with open(path) as f:
        return f.read()


localLogger.debug("init cache")
cache = sqlite3.connect("Cache/Cache.db")
cacheCursor = cache.cursor()

# SQL
cacheInit = getTextFile("Cache/_init.sql")
cacheGet = getTextFile("Cache/_get.sql")
cacheAdd = getTextFile("Cache/_add.sql")
cacheRem = getTextFile("Cache/_rem.sql")

cacheCursor.execute(cacheInit)

# current time in days
currentTime = time() / (60 * 60 * 24)

def getURLContent(url):
    localLogger.debug("looking at cache")
    cursor = cacheCursor.execute(cacheGet, (url, ))

    cachedResult = cursor.fetchone()
    if cachedResult is not None:
        if float(cachedResult[2]) > currentTime + Settings.Cache.maxAge:
            # Cache is stale
            localLogger.warn("Current cache is older than max age")
            cursor.execute(cacheRem, (url, ))
            cache.commit()
        
        else:
            # Found data
            return cachedResult[1]

    localLogger.debug("Getting content from: " + url)
    WebPage = request.urlopen(url)
    Data = WebPage.read()
    WebPage.close()

    # cache and save result
    cacheCursor.execute(cacheAdd, (url, Data, str(currentTime) ))
    cache.commit()
    
    return Data

def getHTMLContent(url):
    InnerHTML = getURLContent(url)

    try:
        InnerHTML = InnerHTML.decode()

    except UnicodeDecodeError:
        localLogger.warning("Returning bytes, can't decode: '{}' request".format(url))

    return InnerHTML
