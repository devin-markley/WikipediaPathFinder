from bs4 import BeautifulSoup
import grequests
import time

startLink = "https://en.wikipedia.org/wiki/Latte"
endLink = "/wiki/United"

def asyncLinkFinder(listLinks, webpageToSearch, parentList):
    #Connecting to the webpage
    #TODO Make sure Linkfinder doesn't search the same link twice
    batches = 20
    page = grequests.get(webpageToSearch)
    response = grequests.map([page], size=batches)
    for res in response:
        try:
            soup=BeautifulSoup(res.text, 'html.parser')
        except AttributeError:
            continue
        #TODO Limit links searched by linkfinder to a greater degree
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

while(explorationQueue):
    i = explorationQueue.pop(0)
    if(asyncLinkFinder(explorationQueue, i[0], i[1])):
        endTime = time.time()
        elapsedTime = endTime - startTime
        print(elapsedTime)
        print("this was the path to the endlink" + " " + str(i[0])+ " " + str(i[1]))
        break  
    alreadySearched.append(i[0])
quit()