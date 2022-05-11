import requests
import lxml
from bs4 import BeautifulSoup
import re

url = "https://www.olx.ro/d/piese-auto/?currency=RON&page=1"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}
f = requests.get(url)
soup = BeautifulSoup(f.content,'lxml')
title = soup.findAll('h6', attrs={'class':'css-v3vynn-Text eu5v0x0'})

titles=[]

for x in title:
    titles.append(x.get_text())

x=2

while title is not None and x<25:
    url ="https://www.olx.ro/d/piese-auto/?currency=RON&page="+str(x)
    f = requests.get(url)
    soup = BeautifulSoup(f.content,'lxml')
    title = soup.findAll('h6', attrs={'class':'css-v3vynn-Text eu5v0x0'})
    for d in title:
        titles.append(d.get_text())
    x=x+1

print("Subcategorii:")
print("1. Roti - Jante - Anvelope")
print("2. Consumabile - Accesorii")
print("3. Caroserie - Interior")
print("4. Mecanica - Electrica")
print("5. Alimentare")
print("6. Distributie - Transmisie")
print("7. Directie")
print("8. Esapament")
print("9. Articulatie roata")
print("10. Sistem racire")

x=input("Introdu subcategoria: ")

regex=[r"roti|roata|jenti|janta|jante|anvelope|anvelopa|cauc|cauciucuri",
       r"ulei de motor|ulei lant|bare transversale|spoiler|carlig|cotiera|covorase|covoare",
       r"capota|geam|geamuri|usa|usi|schimbator|emblema|sigla|grila|bara|far|faruri|oglinda|oglinzi|lampa|lampi|stop|stopuri|volan|centuri|centura|bancheta|parasolar|parasolare|airbag|airbaguri|scaun|scaune|nuca|scrumiera|torpedou|torpedo",
       r"etrier|etrieri|compresor|ambreiaj|alternator|suspensie|motor|radiator|releu|contact|cutie de viteze|cutie viteze|injector|injectoare|abs|instalatie electrica|calculator",
       r"combustibil|alimentare|AKF|senzor apa",
       r"distributie|transmisie|arbore",
       r"directie|burduf|servodirectie|radiator ulei|radiator de ulei|bracaj",
       r"esapament|injector|catalizator|evacuare|filtru particule|filtru de particule|turbosuflanta|toba|lambda",
       r"planetara|planetare|rulment|stabilizator|ax|bara stabilizatoare",
       r"termostat|modul racire|electroventilator|senzor temperatura"]

categories = {1:"", 2:"", 3:"", 4:"", 5:"", 6:"", 7:"", 8:"", 9:"", 10:""}
for i in range(0,10):
    pat = re.compile(regex[i], re.IGNORECASE)
    results = list(filter(pat.search, titles))
    categories[i]=results

for i in categories[int(x)-1]:
    print(i)


with open("olx_crawler.html", 'w', encoding="utf-8") as html:
    html.write("<!DOCTYPE html>\n")
    html.write('<html lang="en">\n')
    html.write('<head>\n')
    html.write('<meta charset="UTF-8" />\n')
    html.write('<meta name="viewport" content="width=device-width, initial-scale=1.0" />\n')
    html.write('<meta http-equiv="X-UA-Compatible" content="ie=edge" />\n')
    html.write('<title>Olx Crawler</title>\n')
    html.write('</head>\n')
    html.write('<body>\n')
    for i in categories[int(x)-1]:
        html.write(f'<h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{i}</h3>\n')
    html.write('</body>\n')
    html.write('</html>\n')
