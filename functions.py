from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class trending:

    # constructor
    def __init__(self, url):
        self.url = url

    def scraping_trending(self):

        # Accedemos al puglin de googlechrome
        s = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=s)
        browser.maximize_window()

        browser.get(self.url)
        # Asignamos un nombre de usario y una contraseña
        file = open('Resources/config.txt')
        lines = file.readlines()
        username = lines[0]
        password = lines[1]
        time.sleep(1)
        # Accedemos al elemento de nombre usuario
        elementID = browser.find_element(By.NAME, 'wpName')
        # Rellenamos el formulario
        elementID.send_keys(username)
        # Accedemos al elemento de la contraseña
        elementPW = browser.find_element(By.NAME, 'wpPassword')
        time.sleep(1)
        # Rellenamos el formulario
        elementPW.send_keys(password)
        # Accedemos a la parte de búsqueda y escribimos lo que queremos buscar
        elementS = browser.find_element(By.NAME, 'search')
        time.sleep(1)
        elementS.send_keys('List of countries by average yearly temperature')
        # Accedemos al botón de búsqueda y clicamos en el
        time.sleep(4)
        elementB = browser.find_element(By.ID, 'searchButton')
        elementB.click()
        url = browser.current_url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}
        temperature = requests.get(url, headers=headers)
        soup = BeautifulSoup(temperature.text, "html.parser")
        # Obtenemos la información de la tabla
        rows = soup.find('table').find('tbody').find_all('tr')
        colum = ["Country", "Temperature_1961_1990"]
        list = []
        final = []
        for row in rows:
            for item in row.find_all('td'):
                list.append(item.text.replace("\n", "").replace(u'\xa0',""))
            final.append(list)
            list = []

        datos = pd.DataFrame(final, columns=colum)
        time.sleep(1)
        browser.quit()

        data_clean = self.data_clean_temperature(datos)

        return data_clean


    def data_clean_temperature(self, datos):

        datos.drop(index=datos.index[0], axis=0, inplace=True)
        datos['Country'] = datos['Country'].str.upper()

        return datos

  