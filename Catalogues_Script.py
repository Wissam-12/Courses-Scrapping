import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import xlsxwriter
import os

 
PATH = "web Drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://www.carrefour.fr/catalogue"

start_time = time.time()
driver.get(url)
try:
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-reject-all-handler')))
    myCookies.click()
finally:
    try:
        WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.CLASS_NAME, 'paper-catalog')))
        data = []
        #Save the html page ==========================================
        html = driver.page_source
        #open the page with beautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        print("-------------------")
        items = soup.find_all(class_="paper-catalog")
        #iterate in catalogues
        for item in items:
            try:
                item = item.find(class_ = 'paper-catalog__box')
                img = item.find(class_='image')
                nom = item.find(class_='paper-catalog__title').text
                date = item.find(class_="paper-catalog__date--text").text.split()
                store = item['href'].split('/')[3].split('-')[0]
                start = date[1]
                end = date[-1]
                data.append([img['src'], nom, start, end, 'https://www.carrefour.fr' + item['href'], 'Carrefour ' + store])
                print("********************")
                print([img['src'], nom, start, end, 'https://www.carrefour.fr' + item['href'], 'Carrefour ' + store])
            finally:
                continue

        print("--- %s seconds ---" % (time.time() - start_time))
    finally:
        print("End")
        url = "https://catalogue.auchan.fr/"

        start_time = time.time()
        driver.get(url)

        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'cat-tile')))
            #Save the html page ==========================================
            html = driver.page_source
            #open the page with beautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            print("-------------------")
            items = soup.find_all(class_="cat-tile")
            #iterate in catalogues
            for item in items:
                img = item.find(id = 'couvImage')
                nom = item.find(id = 'catTitle').text
                start = item.find(id = 'startDate').text.split()[3]
                end = item.find(id = 'endDate').text.split()[3]
                data.append([img['src'], nom, start, end, item['href'], 'Auchan ' + item['data-store-type']])
                print("********************")
                print([img['src'], nom, start, end, item['href'], 'Auchan ' + item['data-store-type']])

            #Save Data to Excel File ===============================================================================
            #Create Folder if not exist
                if not os.path.exists('Produits'):
                    os.makedirs('Produits')
            
            workbook = xlsxwriter.Workbook('Produits/Catalogues.xlsx')
            worksheet = workbook.add_worksheet("Listing")

            # Add a table to the worksheet.
            worksheet.add_table('A1:F{0}'.format(len(data)), {'data': data,
                                        'columns': [{'header': 'IMAGE'},
                                                    {'header': 'NOM'},
                                                    {'header': 'START DATE'},
                                                    {'header': 'END DATE'},
                                                    {'header': 'LIEN'},
                                                    {'header': 'MAGASIN'},
                                                    ]})
            workbook.close()
            print("--- %s seconds ---" % (time.time() - start_time))
        finally:
            print(len(data))
            print("End")
            driver.quit()