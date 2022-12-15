from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json
from datetime import datetime
import xlsxwriter
import os

PATH = "Web Drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

url = "https://fr.igraal.com/coupon-imprimer/"
driver.get(url)
data = []

try :
    myCookies = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID , 'cookies-banner-btn-accept')))
    myCookies.click()
finally :
    ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'grid-resp-two')))
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    bons = soup.find(class_= 'grid-resp-two')
    items = bons.find_all(class_ = 'widget--coupon-cai')
    for item in items :
        # nom = item.find(class_='br-description').text.replace("\n", "")
        # reduction = item.find(class_= 'widget--coupon-price').text.replace("€", "")
        # description = item.find(class_= 'widget--coupon-overlay-txt').find(class_= 'tooltip-inner').text
        # imageMarque = "https://www.enviedebienmanger.fr/" + item.find(class_= 'marque-produit').find(class_= 'img-responsive')['src']
        # marque = item.find(class_= 'widget--coupon-left').find(class_= 'widget--coupon-title').text
        imageCoupon = item.find(class_= 'widget--coupon-img-wrapper').find("img")['src']
        Coupondata = item.find(class_ = 'widget--coupon-right').find(attrs={"data-ig-coupon-block": "coupon"})["data-ig-coupon-json"]

        jData = json.loads(Coupondata)
        date = datetime.fromtimestamp(int(jData["validity"])//1000).strftime('%d/%m/20%y')
        print([jData["title"], "", jData["amount"], jData["title"], jData["brandName"], date, imageCoupon, "", "Coupon à imprimer", url])
        data.append([jData["title"], "", jData["amount"], jData["title"], jData["brandName"], date, imageCoupon, "", "Coupon à imprimer", url])
    if not os.path.exists('CouponsResults'):
        os.makedirs('CouponsResults')
    
    workbook = xlsxwriter.Workbook('CouponsResults/iGraal.xlsx')
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