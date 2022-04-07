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

# Abrir el navegador con la URL
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)

# URL
URL = 'https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl'
URL_principal = 'https://www.youtube.com/'

#req_URL = requests.get(URL)
#req_URL_text = req_URL.text
#length_text = len(req_URL_text)


# Fichero robots.txt:
def robots(url):
    if url[-1] == "/":
        r_link = url
    else:
        r_link = os.path.join(url, "/")
    rst = requests.get(r_link + 'robots.txt')
    return rst.text

print(robots(URL_principal))

log_in = open('Login/Credentials.txt')
credentials = log_in.readlines()
user = credentials[0]
password = credentials[1]

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
#consent_button_xpath = "//button[@aria-label='Aceptar el uso de cookies y otros datos para las finalidades descritas']"
#consent = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, consent_button_xpath)))

#consent = driver.find_element_by_xpath(consent_button_xpath)
#consent.click()


#Apply delay
#driver.implicitly_wait(TimeOut)
#print(agent)

# Obtener los videos
elements = driver.find_elements_by_xpath("""//*[@id="thumbnail"]""")
videos = []
for element in elements:
    videos.append(element.get_attribute("href"))
   
    #time.sleep(1)

videos.pop(0)

   
# Obtener información de cada video
# diccionario = []
data = pd.DataFrame(columns = ["Url_Video", "Title", "Trending_Position", "Visualizations",
                               "Date", "Likes", "Subscribers", "Chanel", "Url_Chanel", "Comments",
                               "Type", "Length"])


time_video = sleep(random.uniform(3,3.5))

position = 0
for video in videos:
   
    driver.get(video)
    time_video
   
    # Pausar video
    video2 = driver.find_element_by_id('movie_player')
    video2.send_keys(Keys.SPACE) #hits space
   
    #time_video  
    path_titulo = '//*[@id="title"]/h1/yt-formatted-string'
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, path_titulo))).text

    title = driver.find_element(by=By.XPATH, value ="""//*[@id="title"]/h1/yt-formatted-string""").text
    #time_video
    position = position + 1
    #time_video
    visualizations = driver.find_element(by=By.XPATH, value ="""//*[@id="formatted-snippet-text"]/span[1]""").text
    #time_video
    date = driver.find_element(by=By.XPATH, value ="""//*[@id="formatted-snippet-text"]/span[3]""").text
    #time_video
    likes = driver.find_element(by=By.XPATH, value ="""/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]/a/yt-formatted-string""").get_attribute("aria-label")
    subscribers = driver.find_element(by=By.XPATH, value = """//*[@id="owner-sub-count"]""").text
    chanel = driver.find_element(by=By.XPATH, value ="""//*[@id="text"]/a""").text
    #time_video
    url_chanel = driver.find_element(by=By.XPATH, value ="""//*[@id="text"]/a""").get_attribute("href")
    #time_video
    comments = driver.find_element(by=By.XPATH, value ="""//*[@id="count"]""").text
    #time_video
    tipo = driver.find_element(by=By.XPATH, value ="""//*[@id="watch7-content"]/meta[16]""").get_attribute("content")
    #time_video
    length = driver.find_element(by=By.XPATH, value ="""//*[@id="watch7-content"]/meta[6]""").get_attribute("content")
    #time_video
    label = driver.find_element(by=By.XPATH, value ="""//*[@id="super-title"]/a""").text
   
    data = data.append({"Url_Video":video, "Title":title,
                        "Trending_Position":position, "Visualizations":visualizations,
                        "Date":date, "Likes":likes, "Subscribers": subscribers, "Chanel":chanel, "Url_Chanel":url_chanel,
                        "Comments":comments,"Type":tipo, "Length":length, "#Tag":label }
                       ,ignore_index=True)

   
data


# ,quotechar='|', quoting=csv.QUOTE_MINIMAL
import csv
with open('Dataset/youtube2.csv', 'w', newline='', encoding="utf16") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';')
   
    header = ["Url_Video", "Title", "Trending_Position", "Visualizations",
                               "Date", "Likes", "Subscribers", "Chanel", "Url_Chanel", "Comments",
                               "Type", "Length", "#Tag"]
    spamwriter.writerow(header)
    for row in range(len(data)):
       
        try:
            spamwriter.writerow(data.loc[row])
        except Exception:
            continue