from bs4 import BeautifulSoup
import grequests
import time
from pymongo import MongoClient

client = MongoClient()
db = client["mydatabase"]

cache_collection = db["cache"]

def get_data_from_cache(key):
    cache_entry = cache_collection.find_one({"key": key})
    if cache_entry is not None:
        return cache_entry["data"]
    return None

def store_data_in_cache(key, data):
    cache_entry = {"key": key, "data": data}
    cache_collection.insert_one(cache_entry)

startLink = "https://en.wikipedia.org/wiki/Latte"
endLink = "/wiki/Merienda"

def LinkFinder(listLinks, webpageToSearch, parentList): 
    batches = 20
    page = grequests.get(webpageToSearch)
    response = grequests.map([page], size=batches)
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
                if "https://en.wikipedia.org" + newLink in alreadySearched or [item for item in listLinks if item[0] =="https://en.wikipedia.org" + newLink]:
                    continue
                newParentList = [webpageToSearch] + parentList
                if len(newParentList) < 5:
                    print(newLink)
                    listLinks.append(("https://en.wikipedia.org" + newLink, newParentList))
                    store_data_in_cache(newLink, listLinks[-1:])    
                else:
                    print("Path could not be found")
                    print(listLinks)
                    quit()
                if (newLink == endLink):
                    return True
    return False

explorationQueue = [(startLink, [])]
alreadySearched = []
startTime= time.time()

data = get_data_from_cache(endLink)
if data is not None:
    print(data)
else:
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