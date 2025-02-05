class Logging:
    loggerFolder = "logs/"
    loggerPathTemplate = "runtime.{}.log"


class Generation:
    searchPath = "Sections/*"
    buildNumberLocation = "build number"

    publicFolderImageLocation = "Resources/PageImages/folder-sharp.svg"
    publicFolderOpenImageLocation = "Resources/PageImages/folder-open-sharp.svg"
    publicFileImageLocation = "Resources/PageImages/document-text-sharp.svg"
    publicBackImageLocation = "Resources/PageImages/arrow-back-sharp.svg"

    buildLocation = "PublicAccess/"

    MainPage = buildLocation + "index.html"
    MinimumPage = buildLocation + "bare.html"
    DownloadPage = buildLocation + "lukasz-baldyga.html"


class Verification:  # Replace with flags
    verify = False
    verifyMainPage = verify and True
    verifyMinimumPage = verify and True
    verifyDownloadPage = verify and True


class Behavior:
    autoOpenSection = "Welcome"  # What section to automatically open upon load

class Cache:
    maxAge = 7
