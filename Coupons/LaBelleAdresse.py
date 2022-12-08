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

data = []
driver.get("https://www.labelleadresse.com/economies/bon-reduction")

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
    myCookies.click()
finally :
    urls = ["https://www.labelleadresse.com/economies/bon-reduction", "https://www.labelleadresse.com/economies/remboursement"]
    passe = False
    for url in urls :
        if passe :
            driver.get(url)
            passe = True
        ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'c-listProducts__list')))
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        bons = soup.find(class_= 'c-listProducts__list')
        items = bons.find_all(class_='c-product')
        for item in items :
            reduction = item.find(class_= 'c-product__price').text
            description = item.find(class_= 'c-product__desc').text
            imageCoupon = item.find(class_= 'c-product__img').find("img")['src']
            nom = item.find(class_= 'c-product__img').find("img")['alt']
            imagesMarques = item.find(class_= 'c-product__logo').find_all("img")
            imageMarque = ""
            marque = ""
            for image in imagesMarques:
                imageMarque = imageMarque + image['src'] + " + "
                marque = marque + image["alt"]
            couponType = item.find(class_='c-product__actions-type').text.replace("Pour remboursement", "Offre de remboursement").replace("Pour impression", "Coupon à imprimer")
            date = ""
            print([nom, reduction, description, marque, date, imageCoupon, imageMarque, couponType])
            data.append([nom, reduction, description, marque, date, imageCoupon, imageMarque, couponType])
    if not os.path.exists('CouponsResults'):
        os.makedirs('CouponsResults')
    
    workbook = xlsxwriter.Workbook('CouponsResults/Ribambel.xlsx')
    worksheet = workbook.add_worksheet("Listing")

    # Add a table to the worksheet.
    worksheet.add_table('A1:G{0}'.format(len(data)), {'data': data,
                                'columns': [{'header': 'NOM'},
                                            {'header': 'REDUCTION'},
                                            {'header': 'DESCRIPTION'},
                                            {'header': 'MARQUE'},
                                            {'header': 'DATE_VALIDITE'},
                                            {'header': 'IMAGE_COUPON'},
                                            {'header': 'IMAGE_MARQUE'},
                                            {'header': 'TYPE_COUPON'}
                                            ]})

    workbook.close()

driver.quit() 