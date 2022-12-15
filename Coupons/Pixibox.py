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

url = "https://www.pixibox.com/"

data = []

driver.get(url)

try:
    products = WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.products__list.row div.col-xs-24.col-sm-12.col-lg-8')))

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select('.products__list.row div.col-xs-24.col-sm-12.col-lg-8')
    print("****************** ", len(items))
    for item in items :
        try:
            code = ""
            nom = item.find(class_ = 'product__title').text.replace('\n','')
            reduction = item.find(class_= 'product__ticket').text.replace("€", "").replace('\n','').replace(' ','').replace('deréduction','')
            description = ""
            imageCoupon = item.select_one('.product__pic a img')['src']
            imageMarque = ""
            marque = ""
            date = "" #peut être récupéré si on clique sur le produit récupère combien de jours restants et puis en l'ajoutant à la date actuelle
            link = "https://www.pixibox.com" + item.select_one('.product__pic a')['href']
            print([nom, code, reduction, description, marque, date, imageCoupon, imageMarque, "Coupon à imprimer", link])
            data.append([nom, code, reduction, description, marque, date, imageCoupon, imageMarque, "Coupon à imprimer", link])
        except Exception as e:
            print('Erreur:',e)   
except Exception as e:
    print("Erreur:",e)

if len(data) > 0 :
    if not os.path.exists('CouponsResults'):
        os.makedirs('CouponsResults')
        
    workbook = xlsxwriter.Workbook('CouponsResults/Pixibox.xlsx')
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