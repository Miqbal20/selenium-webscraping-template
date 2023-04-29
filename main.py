import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
# send keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
# BS4
from bs4 import BeautifulSoup
# Json & Pandas}
import json
import pandas as pd


class Scrape:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        service = Service(ChromeDriverManager().install())
        self.browser = webdriver.Chrome(service=service, options=options)

    def start(self, url):
        driver = self.browser

        # Verify URL
        if url.__contains__('https://'):
            driver.get(url)
            driver.maximize_window()
        else:
            driver.get(f'https://{url}')
            driver.maximize_window()

        #  Waiting for URL
        timeout = WebDriverWait(driver, 10)
        try:
            timeout.until(ec.presence_of_element_located((By.CLASS_NAME, 'login_logo')))
        except ValueError:
            print(ValueError)
            driver.quit()

        # Login to Saucedemo
        username = 'standard_user'
        password = 'secret_sauce'
        driver.find_element(By.ID, 'user-name').send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.ID, 'login-button').click()
        timeout.until(ec.presence_of_element_located((By.CLASS_NAME, 'title')))

        # Get Data List
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        inventory_list = soup.find('div', 'inventory_list')
        itemList = []
        for item in inventory_list:
            title = item.findNext('div', 'inventory_item_name').text
            desc = item.findNext('div', 'inventory_item_desc').text
            price = item.findNext('div', 'inventory_item_price').text
            image = item.findNext('img', 'inventory_item_img')['src']

            saveItem = {
                'title' : title,
                'desc': desc,
                'price': price,
                'image': f'https://www.saucedemo.com{image}',
            }
            itemList.append(saveItem)

        # Json Result
        with open('result/data.json', 'w+') as json_data:
            json.dump(itemList, json_data)
            print('data.json Created')

            # Excel Result
        df = pd.DataFrame(itemList)
        df.to_csv('result/data.csv', index=False)
        print('data.csv Created')
        df.to_excel('result/data.xlsx', index=False)
        print('data.xlsx Created')


if __name__ == "__main__":
    Scrape().start('https://www.saucedemo.com/')
