import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog

seleccionar_fichero = input("¿Quiere seleccionar un fichero con resultados anteriores (S para sí)?\n")
if seleccionar_fichero.upper() == "S":
    file_path = filedialog.askopenfilename()
    print("Ruta del archivo seleccionado:", file_path)

class Juego:
    url=""
    nombre=""
    precio=0.0

    def __init__(self, url, nombre, precio, tienda='Ninguna'):
        self.url=url
        self.nombre=nombre
        self.precio=precio

    def __str__(self):
        return "-->Nombre: {}\n-URL: {}\n-Precio:  {}\n-Tienda donde está más barato: {}\n\n".format(self.nombre, self.url, self.precio, self.tienda)
    
    def obtiene_soup(self):
        driver = webdriver.Chrome()
        driver.get(self.url)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'offers_table')))
        html = driver.page_source
        driver.close()

        soup = BeautifulSoup(html, features="html.parser")

        return soup
    
    def setTienda(self, tienda):
        self.tienda=tienda

    def setPrecio(self, precio):
        self.precio=precio


url_base="https://www.allkeyshop.com/blog/list/Juan-Mendez2/336592/"

req = requests.get(url_base)
soup = BeautifulSoup(req.text, features="html.parser")

filas_wl = soup.select(".akswl-list-display tr a")

lista_juegos=[]
tiendas_mas_baratas={
    'ficticia':[]
}

url=""
nombre=""
precio=0.0

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
        #print("Analizando {}\n{}".format(juego.nombre, juego.url))
        print("diccionario:",tiendas_mas_baratas)
        nombre_tienda=tienda.select(".x-offer-merchant-name.offers-merchant-name")[0].getText()
        plataforma_steam=len(tienda.select(".x-offer-platform-logo.sprite.sprite-30-steam"))
        precio_tienda=tienda.select(".x-offer-buy-btn-in-stock.text-left")[0].getText()[:-1]
        #print(nombre_tienda, plataforma_steam, precio_tienda)

        if plataforma_steam == 1 and nombre_tienda != "G2A Plus":
            juego.setTienda(nombre_tienda)
            tiendas_mas_baratas.setdefault(nombre_tienda, [])
            tiendas_mas_baratas[nombre_tienda].append(juego)
            break

        

    #print(soup_juego.select("div")[1])

#hola