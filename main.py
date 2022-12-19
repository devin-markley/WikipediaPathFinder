import requests
from bs4 import BeautifulSoup

startLink = "https://en.wikipedia.org/wiki/Coffee"
endLink = "/wiki/Seattle"

def linkfinder(listLinks, webpageToSearch, parentList):
    #Connecting to the webpage
    #TODO Make sure Linkfinder doesn't search the same link twice
    resp = requests.get(webpageToSearch)
    if resp.status_code == 200:
        print("Successfully opened the webpage")
        #Crawling through the webpage looking for links
        soup=BeautifulSoup(resp.text, 'html.parser')
        #Limiting the list to only links that lead to other wikipedia webpages
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
                newParentList = [webpageToSearch] + parentList
                if len(newParentList) < 3:
                    listLinks.append(("https://en.wikipedia.org" + newLink, newParentList))
                #TODO format endlink here
                if (newLink == endLink):
                    return True
    else:
        print("error")
        
    return False

explorationQueue = [(startLink, [])]

while(explorationQueue):
    #TODO Keeping track of depth
    i = explorationQueue.pop(0)
    if(linkfinder(explorationQueue, i[0], i[1])):
        print("this was the path to the endlink" + " " + str(i[0])+ " " + str(i[1]))
        break  
quit()