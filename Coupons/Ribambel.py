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

url = "https://www.ribambel.com/bons-de-reduction"
driver.get(url)
data = []

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
    myCookies.click()
finally :
    ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'voucherGrid')))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    bons = soup.find(class_= 'voucherGrid')
    items = bons.find_all(class_='voucherContainer')
    for item in items :
        marque = item["data-name"]
        reduction = item["data-price"]
        description = item.find(class_= 'voucherDescription').text.replace("\xa0", "").replace("\n", "")
        nom = description
        imageCoupon = "https://www.ribambel.com" + item.find(class_= 'voucherLeftContainer').find("img")['src']
        imagesMarques = item.find(class_= 'voucherBrandIcon').find_all("img")
        imageMarque = ""
        for image in imagesMarques:
            imageMarque = "https://www.ribambel.com" + image['src'] + " + "
        date = item.find(class_= 'voucherOverlay').find(class_= 'pt-1').text.replace("Jusqu'au ", "")
        print([nom, reduction, description, marque, date, imageCoupon, imageMarque])
        data.append([nom, "", reduction, description, marque, date, imageCoupon, imageMarque, "Offre de remboursement + Coupon à imprimer", url])
    if not os.path.exists('CouponsResults'):
        os.makedirs('CouponsResults')
    
    workbook = xlsxwriter.Workbook('CouponsResults/Ribambel.xlsx')
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