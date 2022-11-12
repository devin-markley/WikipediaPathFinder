import requests
from bs4 import BeautifulSoup

startLink = input("Enter starting wikipedia link: ")
endLink = input("Enter ending wikipedia link: ")
listLinks = []

def linkfinder(listLinks, link):
    #Connecting to the webpage
    resp = requests.get(link)
    if resp.status_code == 200:
        print("Successfully opened the webpage")
        #Crawling through the webpage looking for links
        soup=BeautifulSoup(resp.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            listLinks.append(link["href"])
    else:
        print("error")

startLinkList = []
linkfinder(startLinkList, startLink)

print(startLinkList)
