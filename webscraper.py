from bs4 import BeautifulSoup
import requests


session_object = requests.Session() # create a session to process multiple requests
url = "https://realpython.github.io/fake-jobs/"
website_page = session_object.get(url)
soup = BeautifulSoup(website_page.content, "html.parser")


links = soup.find_all('a', text = 'Apply')
urls = []

for a in links:
    urls.append(a.get('href'))

descriptions = []

for url in urls:
    desc_page = session_object.get(url)
    desc_soup = BeautifulSoup(desc_page.content, "html.parser")
    descriptions.append(desc_soup.find('div', class_ = 'content').text)