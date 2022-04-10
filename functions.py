# Imports
from selenium import webdriver
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd
import random
import csv
import datetime as dt
import os
from bs4 import BeautifulSoup


# URL
URL = 'https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl'
URL_principal = 'https://www.youtube.com/'


# Fichero robots.txt:
def robots(url):
    if url[-1] == "/":
        r_link = url
    else:
        r_link = os.path.join(url, "/")
    rst = requests.get(r_link + 'robots.txt')
    return rst.text

# Lo imprimimos:
print(robots(URL_principal))


# Analizamos y visualizamos el sitemap:
sitemap = "https://www.youtube.com/trends/sitemap.xml"

response = requests.get(URL)
with open('./sitemap.xml', 'wb') as file:
    file.write(response.content)

xml_sm = "./sitemap.xml"

xml = BeautifulSoup(open(xml_sm, encoding="utf8"), "lxml")
xml_content = xml.prettify()
print(xml_content)

'''
import xml.dom.minidom

dom = xml.dom.minidom.parse(file='../sitemap.xml')
pretty_xml_as_string = dom.toprettyxml()
print(pretty_xml_as_string)'''

# Tecnología usada:
import builtwith

tech = builtwith.builtwith(URL_principal)
print(tech)


# Propietario de la página:
import whois

print(whois.whois("https://sullygnome.com/"))



# Credentials:
user = 'tipologia.uoc.2022@gmail.com'
password = 'TIPOPRA1'

# Abrir el navegador con la URL
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

driver.get(URL)
sleep(1)
driver.maximize_window()
sleep(2)

# Click en el botón de login:
driver.find_element_by_xpath("""//*[@id="yDmH0d"]/c-wiz/div/div/div/div[1]/div[1]/div/div/a""").click()
sleep(2)

# Inserción del nombre de usuario:
input_user = driver.find_element(By.XPATH, "//input[@aria-label='Correo electrónico o teléfono']")
input_user.send_keys(user)
sleep(2)

# Click en el botón de Siguiente:
next_button = driver.find_element_by_xpath("""//*[@id="identifierNext"]/div/button/span""")
next_button.click()
sleep(2)

# Insertamos el password:
input_pass = driver.find_element(By.XPATH, "//input[@aria-label='Introduce tu contraseña']")
input_pass.send_keys(password)
sleep(2)

# Click en el botón de Siguiente:
next_button = driver.find_element_by_xpath("""//*[@id="passwordNext"]/div/button/span""")
next_button.click()
sleep(5)

# Aceptar para dar consentimiento en el uso de cookies y datos:
# consent_button_xpath = "//button[@aria-label='Aceptar el uso de cookies y otros datos para las finalidades descritas']"
# consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath)))

# consent = driver.find_element_by_xpath(consent_button_xpath)
# consent.click()


# Apply delay
# driver.implicitly_wait(TimeOut)
# print(agent)

# Obtener los videos
elements = driver.find_elements_by_xpath("""//*[@id="thumbnail"]""")
videos = []
for element in elements:
    videos.append(element.get_attribute("href"))

    # time.sleep(1)

videos.pop(0)

# Obtener información de cada video
# diccionario = []
data = pd.DataFrame(columns=["Url_Video", "Title", "Trending_Position", "Visualizations",
                             "Date", "Likes", "Subscribers", "Channel", "Url_Channel", "Comments",
                             "Type", "Length"])

# Función para generación del dataset del top n de videos, por defecto top10:
def top_videos(n = 10):
    # Creamos el DataFrame donde guardaremos la información, declarando sus columnas:
    data = pd.DataFrame(columns=["Url_Video", "Title", "Trending_Position", "Visualizations",
                                 "Date", "Likes", "Subscribers", "Channel", "Url_Channel", "Comments",
                                 "Type", "Length"])
    time_video = sleep(random.uniform(3, 3.5))
    position = 0
    for video in videos[0:n]:
            # Accedemos al video y esperamos:
            driver.get(video)
            time_video

            # Pausar video:
            video2 = driver.find_element_by_id('movie_player')
            video2.send_keys(Keys.SPACE)  # hits space

            # time_video
            path_titulo = '//*[@id="title"]/h1/yt-formatted-string'
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, path_titulo))).text

            # Obtenemos el título:
            title = driver.find_element(by=By.XPATH, value="""//*[@id="title"]/h1/yt-formatted-string""").text

            position = position + 1
            visualizations = driver.find_element(by=By.XPATH, value="""//*[@id="formatted-snippet-text"]/span[1]""").text
            date = driver.find_element(by=By.XPATH, value="""//*[@id="formatted-snippet-text"]/span[3]""").text
            likes = driver.find_element(by=By.XPATH,
                                        value="""/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-formatted-string""").get_attribute(
                "aria-label")
            subscribers = driver.find_element(by=By.XPATH, value="""//*[@id="owner-sub-count"]""").text

            channel = driver.find_element(by=By.XPATH, value="""//*[@id="text"]/a""").text
            url_channel = driver.find_element(by=By.XPATH, value="""//*[@id="text"]/a""").get_attribute("href")
            comments = driver.find_element(by=By.XPATH, value="""//*[@id="count"]""").text
            tipo = driver.find_element(by=By.XPATH, value="""//*[@id="watch7-content"]/meta[16]""").get_attribute("content")
            length = driver.find_element(by=By.XPATH, value="""//*[@id="watch7-content"]/meta[6]""").get_attribute("content")
            label = driver.find_element(by=By.XPATH, value="""//*[@id="super-title"]/a""").text

            data = data.append({"Url_Video": video, "Title": title,
                                "Trending_Position": position, "Visualizations": visualizations,
                                "Date": date, "Likes": likes, "Subscribers": subscribers, "Channel": channel,
                                "Url_Channel": url_channel,
                                "Comments": comments, "Type": tipo, "Length": length, "#Tag": label}
                               , ignore_index=True)
    return data

# Ejecutamos la función, y encapsulamos su resultado en "data":
data = top_videos(50)


# Función para creación de CSV:
def csv_file(df):
    with open('Dataset/youtube'  + str(dt.date.today()) + '.csv', 'w', newline='', encoding="utf16") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')
        header = ["Url_Video", "Title", "Trending_Position", "Visualizations",
                  "Date", "Likes", "Subscribers", "Channel", "Url_Channel", "Comments",
                  "Type", "Length", "#Tag"]
        spamwriter.writerow(header)
        for row in range(len(data)):
            try:
                spamwriter.writerow(data.loc[row])
            except Exception:
                continue

# La ejecutamos:
csv_file(data)