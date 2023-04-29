import requests
from bs4 import BeautifulSoup

class Juego:
    url=""
    nombre=""
    precio=0.0

    def __init__(self, url, nombre, precio):
        self.url=url
        self.nombre=nombre
        self.precio=precio

    def __str__(self):
        return "Nombre:{}\nURL:{}\nPrecio:{}\n\n".format(self.nombre, self.url, self.precio)
    
    def obtiene_soup(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.text, features="html.parser")

        return soup


url_base="https://www.allkeyshop.com/blog/list/Juan-Mendez2/336592/"

req = requests.get(url_base)
soup = BeautifulSoup(req.text, features="html.parser")

filas_wl = soup.select(".akswl-list-display tr a")

lista_juegos=[]

url=""
nombre=""
precio=0.0

print(lista_juegos)

for i,fila in enumerate(filas_wl):
    if i == 1 or (i-1)%3 == 0:
        nombre=fila.getText().strip()
        url=fila['href']
    if i-1 == 1 or (i-2)%3 == 0:
        precio=fila.getText().strip()[:-1]
        lista_juegos.append(Juego(url,nombre,precio))

for juego in lista_juegos:
    soup_juego = juego.obtiene_soup()
    tabla_tiendas = soup.select("table")
    print(tabla_tiendas)
    break

#hola