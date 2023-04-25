import requests
from bs4 import BeautifulSoup

url_base="https://www.allkeyshop.com/blog/list/Juan-Mendez2/336592/"

req = requests.get(url_base)
soup = BeautifulSoup(req.text, features="html.parser")

filas_wl = soup.select(".akswl-list-display tr a")

lista_nombres=[]

for i,fila in enumerate(filas_wl):
    if i == 1 or (i-1)%3 == 0:
        lista_nombres.append(fila.getText().strip())

print(lista_nombres)