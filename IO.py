from HelperFunctions import getLogger
from urllib import request
from time import time
import sqlite3
import Settings

localLogger = getLogger()

# Local IO
def Read(path):
    with open(path) as f:
        return f.read()

def Save(path, text):
    with open(path, "w") as f:
        f.write(text)


localLogger.debug("init cache")
cache = sqlite3.connect("Cache/PageGenCache/_Cache.db")
cacheCursor = cache.cursor()

# SQL for cache
cacheInit = Read("Cache/PageGenCache/init.sql")
cacheGet = Read("Cache/PageGenCache/get.sql")
cacheAdd = Read("Cache/PageGenCache/add.sql")
cacheRem = Read("Cache/PageGenCache/rem.sql")

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
