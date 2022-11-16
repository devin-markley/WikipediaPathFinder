import requests
from bs4 import BeautifulSoup

startLink = input("Enter starting wikipedia link: ")
endLink = input("Enter ending wikipedia link: ")

listLinks = []
#TODO set a limit to depth
#TODO if endlink is found function should exit the program
def linkfinder(listLinks, link):
    #Connecting to the webpage
    resp = requests.get(link)
    if resp.status_code == 200:
        print("Successfully opened the webpage")
        #Crawling through the webpage looking for links
        soup=BeautifulSoup(resp.text, 'html.parser')
        #Limiting the list to only links that lead to other wikipedia webpages
        for link in soup.find_all('a', href=True):
            if str(link["href"]).startswith("/wiki/"):
                newLink = link["href"]
                if not '/wiki/' in newLink:
                    if '#' in newLink:
                        indexOfHashtag = newLink.find('#')
                    newLink = newLink[:indexOfHashtag]
                    if ':' in newLink:
                        continue
                listLinks.append("https://en.wikipedia.org" + newLink)
                #TODO Check if endlink is on page called by link
                #if endLink in childernLinkList:
                #print(f"A link too {endLink} is on the page {startLink}")
    else:
        print("error")

childernLinkList = []
linkfinder(childernLinkList, startLink)

    #for links in  childernLinkList:
        #TODO find all links contained on childernLink pages
        #TODO save them in an array named after there parent link