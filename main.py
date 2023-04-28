import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#  Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoTo:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)

    def getUrl(self, url):
        driver = self.browser
        if url.__contains__('https://'):
            driver.get(url)
            driver.maximize_window()
            time.sleep(10)

        else:
            driver.get(f'https://{url}')
            driver.maximize_window()
            time.sleep(10)


if __name__ == "__main__":
    GoTo().getUrl('google.com/')

