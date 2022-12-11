from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import xlsxwriter
import os

PATH = "Web Drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://www.enviedebienmanger.fr/bons-de-reduction"
driver.get(url)
data = []

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
    myCookies.click()
finally :
    try :
        compris = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'close-odr-popin')))
        compris.click()
    finally :
        ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'tout-bons-de-reduction')))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        bons = soup.find(class_= 'tout-bons-de-reduction')
        items = bons.find_all("li")
        for item in items :
            nom = item.find(class_='br-description').text.replace("\n", "")
            reduction = item.find(class_= 'amount').text.replace("€", "")
            description = item.find(class_= 'tooltip-text')['title']
            imageCoupon = "https://www.enviedebienmanger.fr/" + item.find(class_= 'visuel').find(class_= 'img-responsive')['src']
            imageMarque = "https://www.enviedebienmanger.fr/" + item.find(class_= 'marque-produit').find(class_= 'img-responsive')['src']
            marque = item.find(class_= 'marque-produit').find(class_= 'img-responsive')['alt']
            print([nom, marque])
            data.append([nom, "", reduction, description, marque, "", imageCoupon, imageMarque, "Coupon à imprimer", url])
        if not os.path.exists('CouponsResults'):
            os.makedirs('CouponsResults')
        
        workbook = xlsxwriter.Workbook('CouponsResults/EnvieDeBienManger.xlsx')
        worksheet = workbook.add_worksheet("Listing")

        # Add a table to the worksheet.
        worksheet.add_table('A1:J{0}'.format(len(data)), {'data': data,
                                    'columns': [{'header': 'NOM'},
                                            {'header': 'CODE_BAR'},
                                            {'header': 'REDUCTION'},
                                            {'header': 'DESCRIPTION'},
                                            {'header': 'MARQUE'},
                                            {'header': 'DATE_VALIDITE'},
                                            {'header': 'IMAGE_COUPON'},
                                            {'header': 'IMAGE_MARQUE'},
                                            {'header': 'TYPE_COUPON'},
                                            {'header': 'LIEN'}
                                                ]})

        workbook.close()

driver.quit() 