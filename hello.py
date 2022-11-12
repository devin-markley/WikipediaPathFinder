import requests
from bs4 import BeautifulSoup

startLink = input("Enter starting wikipedia link: ")
#endLink = input("Enter ending wikipedia link: ")

def link(link):
    resp = requests.get(link)
    if resp.status_code == 200:
        print("Successfully opened the webpage")
        print("These are all the hypertext links on the page")

        soup=BeautifulSoup(resp.text, 'html.parser')
        #Code could be improved here by removing some of the areas it searchs for links
        for link in soup.find_all('a'):
            #instead of printing store the data in an array
            print(link.get('href'))
    else:
        print("error")

link(startLink)