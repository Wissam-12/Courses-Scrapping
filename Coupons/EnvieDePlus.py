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

url = "https://www.enviedeplus.com/offres-en-cours"
driver.get(url)
data = []

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
    myCookies.click()
finally :
    ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'Styled__StyledColumns-sc-986rxf-0')))
    ToutBons = driver.find_element(By.CLASS_NAME,"Styled__StyledColumns-sc-986rxf-0").find_elements(By.TAG_NAME , 'li')
    print("*************************")
    print(len(ToutBons))
    for bon in ToutBons:
        buttonInfo = bon.find_element(By.CLASS_NAME,"sc-fznWOq").find_element(By.TAG_NAME, 'button')
        buttonInfo.click()
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    bons = soup.find(class_= 'Styled__StyledColumns-sc-986rxf-0')
    items = bons.find_all("li")
    for item in items :
        reduction = item.find(class_= 'sc-fzoNJl').text.replace("€", "").replace("\xa0", "")
        description = item.find(class_= 'sc-fzpkJw').text.split("à valoir sur")[1]
        nom = description
        imageCoupon = item.find(class_= 'sc-fznWqX').find("img")['src']
        date = item.find(class_= 'sc-fzpkJw').text.split("à valoir sur")[0].replace("Valide jusqu’au\xa0", "")
        imageMarque = ""
        marque = ""
        print([nom, reduction])
        data.append([nom, "", reduction, description, marque, date, imageCoupon, imageMarque, "Offre de remboursement", url])
    if not os.path.exists('CouponsResults'):
        os.makedirs('CouponsResults')
    
    workbook = xlsxwriter.Workbook('CouponsResults/EnvieDePlus.xlsx')
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