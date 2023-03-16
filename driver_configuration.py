from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class Driver_configuration:
    """Clase utilizada para configurar drivers. 
    Su metodo create_driver devuelve un driver con el url de la instancia"""

    def create_driver(self):
        """Devuelve un driver para su uso"""
        service = Service(executable_path=ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--incognito")
        #chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options,service=service)        
        return driver
