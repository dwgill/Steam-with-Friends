
def parseUrl(url):
    urlList = url.split('/')
    idDetector = urlList[len(urlList) - 2]
    idName = urlList[len(urlList) - 1]
    return idDetector ,idName


