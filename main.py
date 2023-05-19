import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import tkinter as tk
from tkinter import filedialog
import atexit
import csv
import sys

""""
seleccionar_fichero = input("¿Quiere seleccionar un fichero con resultados anteriores (S para sí)?\n")
if seleccionar_fichero.upper() == "S":
    file_path = filedialog.askopenfilename()
    print("Ruta del archivo seleccionado:", file_path)
"""

historico_mas_barato=[]

with open("historico.csv", newline="\n") as fichero_historico:
    reader = csv.reader(fichero_historico, delimiter=";")
    for juego in reader:
        historico_mas_barato.append(juego)

with open("historico.csv", "w", newline="\n") as fichero_historico:
    writer = csv.writer(fichero_historico, delimiter=";")
    writer.writerow(("JUEGO","PRECIO MINIMO","TIENDA MINIMA"))

driver = webdriver.Chrome()

class Juego:
    url=""
    nombre=""
    precio=0.0
    tienda='Ninguna'

    def __init__(self, url, nombre, precio, tienda='Ninguna'):
        self.url=url
        self.nombre=nombre
        self.precio=precio

    def __str__(self):
        return "-->Nombre: {}\n-URL: {}\n-Precio:  {}\n-Tienda donde está más barato: {}\n\n".format(self.nombre, self.url, self.precio, self.tienda)
    
    def obtiene_soup(self):
        driver.get(self.url)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, 'offers_table')))
        time.sleep(1)
        html = driver.page_source

        soup = BeautifulSoup(html, features="html.parser")

        return soup
    
    def setTienda(self, tienda):
        self.tienda=tienda

    def setPrecio(self, precio):
        self.precio=precio


def cierra_webdriver():
    print("Cerrando ChromeWebdriver")
    driver.close()

atexit.register(cierra_webdriver)

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
    try:
        soup_juego = juego.obtiene_soup()
    except TimeoutException:
        print("Ha fallado el get para:")
        print(juego)
        print("Volviendo a intentar....")
        soup_juego = juego.obtiene_soup()

    tabla_tiendas = soup_juego.select("#offers_table .offers-table-row.x-offer")

    for tienda in tabla_tiendas:
        #print("Analizando {}\n{}".format(juego.nombre, juego.url))
        nombre_tienda=tienda.select(".x-offer-merchant-name.offers-merchant-name")[0].getText()
        plataforma_steam=len(tienda.select(".x-offer-platform-logo.sprite.sprite-30-steam"))
        precio_tienda=tienda.select(".x-offer-buy-btn-in-stock.text-left")[0].getText()[:-1]
        #print(nombre_tienda, plataforma_steam, precio_tienda)

        if plataforma_steam == 1 and nombre_tienda != "G2A Plus":
            juego.setTienda(nombre_tienda)
            tiendas_mas_baratas.setdefault(nombre_tienda, [])
            tiendas_mas_baratas[nombre_tienda].append(juego)
            break
    '''PARA PRUEBAS
    if nombre_tienda == "HRK":
        break'''

lista_tuplada=[]

for tienda in tiendas_mas_baratas.keys():
    for juego in tiendas_mas_baratas[tienda]:
        print(juego)
        encontrado = False
        for juego_historico in historico_mas_barato:
            if juego.nombre == juego_historico[0]:
                #print("El juego", juego.nombre, "tambien estaba en el historico:", juego_historico[0])
                if float(juego.precio) < float(juego_historico[1]):
                    #print("Ademas, es mas barato porque en la web tiene", juego.precio, "y en el historico", juego_historico[1])
                    lista_tuplada.append((juego.nombre, juego.precio, tienda, juego_historico[1], juego_historico[2], "NUEVO MÁS BARATO"))
                    with open("historico.csv", "a", newline="\n") as fichero_historico:
                        writer = csv.writer(fichero_historico, delimiter=";")
                        writer.writerow((juego.nombre, juego.precio, tienda))
                else:
                    #print("Pero el historico, que tiene precio", juego_historico[1], "sigue siendo mas barato que la web", juego.precio)
                    lista_tuplada.append((juego.nombre, juego.precio, tienda, juego_historico[1], juego_historico[2], "El histórico es {}€ más barato".format(float(juego_historico[1]) - float(juego.precio))))
                    with open("historico.csv", "a", newline="\n") as fichero_historico:
                        writer = csv.writer(fichero_historico, delimiter=";")
                        writer.writerow((juego.nombre, juego_historico[1], juego_historico[2]))
                encontrado=True
                break

        if not encontrado:
            lista_tuplada.append((juego.nombre, juego.precio, tienda, "NUEVA ALTA"))
            with open("historico.csv", "a", newline="\n") as fichero_historico:
                writer = csv.writer(fichero_historico, delimiter=";")
                writer.writerow((juego.nombre, juego.precio, tienda))

with open("tiendas.csv", "w", newline="\n") as fichero_tiendas:
    writer = csv.writer(fichero_tiendas, delimiter=";")
    writer.writerow(("JUEGO", "PRECIO MAS BARATO", "TIENDA MAS BARATA", "PRECIO HISTORICO MAS BAJO", "TIENDA HISTORICA MAS BAJA", "COMENTARIO"))
    for juego in lista_tuplada:
        writer.writerow(juego)



    #print(soup_juego.select("div")[1])

#hola