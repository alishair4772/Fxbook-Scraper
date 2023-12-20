import time
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd


class MyFxBook:
    def launchChrome(self, headless):
        options = Options()
        if headless:
            options.add_argument('---headless')
        print("LAUNCHING CHROME")
        self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),options=options)

    def getUrl(self, url):
        print(f"GETTING URL: {url}")
        self.driver.get(url)

    def quitBrowser(self):
        print("CLOSING BROWSER")
        self.driver.close()

    def scrapeHistory(self):
        history = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@name="history"]')))
        self.driver.execute_script("arguments[0].click();", history)
        time.sleep(3)
        self.driver.execute_script("arguments[0].click();", history)

        lastPage = int(WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//a[@lastpage="true"]'))).text)

        for i in range(1, lastPage + 1):
            dataDict = {'open_date': [], 'close_date': [], 'Symbol': [], 'Action': [], 'Lots': [],
                        'open_price': [], 'close_price': [],
                        'pips': [], 'profit': [], 'duration': [], 'change': []}

            print(f"SCRAPING PAGE {i}")
            openDate = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[2]')))
            for i in openDate:
                dataDict['open_date'].append(i.text)
            closeDate = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[4]')))
            for i in closeDate:
                dataDict['close_date'].append(i.text)
            symbol = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[6]')))
            for i in symbol:
                dataDict['Symbol'].append(i.text)
            action = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[7]')))
            for i in action:
                dataDict['Action'].append(i.text)
            lots = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[8]')))
            for i in lots:
                dataDict['Lots'].append(i.text)

            openPrice = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[9]')))
            for i in openPrice:
                dataDict['open_price'].append(i.text)
            closePrice = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[10]')))
            for i in closePrice:
                dataDict['close_price'].append(i.text)
            pips = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[11]')))
            for i in pips:
                dataDict['pips'].append(i.text)
            profit = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[12]')))
            for i in profit:
                dataDict['profit'].append(i.text)
            duration = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[13]')))
            for i in duration:
                dataDict['duration'].append(i.text)
            change = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//table[@id="tradingHistoryTable"]/tbody/tr/td[14]/span')))
            for i in change:
                dataDict['change'].append(i.text)

            path = os.listdir()
            if 'data.csv' in path:
                df = pd.DataFrame(dataDict, columns=list(dataDict.keys()))
                df.to_csv(f'data.csv', mode='a', index=False, header=False)
            else:
                df = pd.DataFrame(dataDict, columns=list(dataDict.keys()))
                df.to_csv(f'data.csv', mode='a', index=False, header=True)

            nextPage = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@title="Next"]')))
            self.driver.execute_script("arguments[0].click();", nextPage)
            time.sleep(3)

if __name__ == "__main__":
    scrape_url = "https://www.myfxbook.com/members/MaxCrypto/maxcrypto-bot-for-mff/9797415"
    scraper = MyFxBook()
    scraper.launchChrome(headless=False)
    scraper.getUrl(url=scrape_url)
    scraper.scrapeHistory()
    scraper.quitBrowser()
