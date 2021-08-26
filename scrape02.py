import requests
from bs4 import BeautifulSoup

url = 'https://www.fatsecret.co.id/resep/51922050-sup-tahu-wortel/Default.aspx'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

numi = [n.text for n in soup.select('.nutrition_facts>.tRight')]
labels = [n.text for n in soup.select('.nutrition_facts>.left')]

if len(numi) == len(labels):
    # create your own csv
    for i in range(len(numi)):
        print(labels[i] + ": " + numi[i])
