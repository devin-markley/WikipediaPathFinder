from bs4 import BeautifulSoup
import grequests
import time
from pymongo import MongoClient

client = MongoClient()
db = client["mydatabase"]

knownPathCollection = db["endLinkPaths"]
webpageLinkCollection = db["webpageLinks"]

def storingEndlinkPaths(endLink, path, startLink):
    knownPathCollection.update_one({"key": endLink}, {"$set": {startLink: path}}, upsert= True)
    
def gettingEndLinkPaths(endLinkKey, startLinkKey):
    cache_entry = knownPathCollection.find_one({"Path": endLinkKey})
    if cache_entry is not None:
        try:
            return cache_entry[startLinkKey]
        except KeyError:
            return None
    return None

def accessingCachedLinksOn(webpage):
    cache_entry = webpageLinkCollection.find_one({"key": webpage})
    if cache_entry is not None:
        return cache_entry["data"]
    return None

def cacheLinksConatinedOn(webpage, linksOn):
    webpageLinkCollection.insert_one({"key": webpage, "data": linksOn})

startLink = "/wiki/Pizza"
endLink = "/wiki/Food"

def LinkFinder(listLinks, webpageToSearch, parentList):
    pathFoundFlag = 0 
    knownLinks = accessingCachedLinksOn(webpageToSearch)
    if knownLinks is not None:
        if len(parentList) < 5:
            newParentList = [webpageToSearch] + parentList
            for link in knownLinks:
                listLinks.append((link, newParentList)) 
        else:
            print("Path could not be found")
            quit()  
    else:
        batches = 20
        page = grequests.get("https://en.wikipedia.org" + webpageToSearch)
        response = grequests.map([page], size=batches)
        linksOnWebpageToSearch = []
        for res in response:
            try:
                soup=BeautifulSoup(res.text, 'html.parser')
            except AttributeError:
                continue
            for link in soup.find_all('a', href=True):
                if str(link["href"]).startswith("/wiki/"):
                    newLink = link["href"]
                    if not '/wiki/' in newLink:
                        if '#' in newLink:
                            indexOfHashtag = newLink.find('#')
                        newLink = newLink[:indexOfHashtag]
                    if ':' in newLink:
                        continue
                    if 'Main_Page' in newLink:
                        continue
                    if 'identifier' in newLink:
                        continue
                    linksOnWebpageToSearch.append(newLink)
                    if newLink in alreadySearched or [item for item in listLinks if item[0] ==  newLink]:
                        continue
                    newParentList = [webpageToSearch] + parentList
                    if len(newParentList) < 5:
                        listLinks.append((newLink, newParentList))
                        storingEndlinkPaths(newLink, listLinks[-1:], startLink)    
                    else:
                        print("Path could not be found")
                        quit()
                    if (newLink == endLink):
                        pathFoundFlag = 1
        cacheLinksConatinedOn(webpageToSearch, linksOnWebpageToSearch)
        linksOnWebpageToSearch.clear()
        if (pathFoundFlag == 1):
            return True
    return False

explorationQueue = [(startLink, [])]
alreadySearched = []
startTime= time.time()

knownPath = gettingEndLinkPaths(endLink, startLink)
if knownPath is not None:
    print("This is a known path!")
    print(knownPath)
else:
    print("No known paths currently searching")
    while(explorationQueue):
        i = explorationQueue.pop(0)
        if(LinkFinder(explorationQueue, i[0], i[1])):
            endTime = time.time()
            elapsedTime = endTime - startTime
            print(elapsedTime)
            print("this was the path to the endlink" + " " + str(i[0])+ " " + str(i[1]))
            break  
        alreadySearched.append(i[0])
    quit()
