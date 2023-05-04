import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
        driver = webdriver.Chrome()
        driver.get(self.url)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'offers_table')))
        html = driver.page_source
        driver.close()

        soup = BeautifulSoup(html, features="html.parser")

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
    tabla_tiendas = soup_juego.select("#offers_table .offers-table-row.x-offer")

    for tienda in tabla_tiendas:
        nombre_tienda=tienda.select(".x-offer-merchant-name.offers-merchant-name")[0].getText()
        plataforma_steam=len(tienda.select(".x-offer-platform-logo.sprite.sprite-30-steam"))
        precio_tienda=tienda.select(".x-offer-buy-btn-in-stock.text-left")[0].getText()[:-1]
        print(nombre_tienda,plataforma_steam,precio_tienda)

    #print(soup_juego.select("div")[1])
    break

#hola