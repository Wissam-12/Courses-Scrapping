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

urls = ["https://www.mavieencouleurs.fr/a-rembourser", "https://www.mavieencouleurs.fr/bons-de-reduction", "https://www.mavieencouleurs.fr/operation-cora"]
types = ["Coupon sur Application", "Coupon à imprimer", "Offre de remboursement"]
data = []
first = True
for i in range(3):
    print(urls[i])
    driver.get(urls[i])
    try :
        if first:
            myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
            myCookies.click()
    finally :
        try :
            if first:
                close = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.ID , 'popin_recrut_close')))
                close.click()
        except:
            print("problem")
        finally :
            first = False
            scroll = True
            driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
            ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'grid-cards')))
            last_height = ToutBons.size['height']
            print("size : ", ToutBons.size['height'])
            while scroll :
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'grid-cards')))
                new_height = ToutBons.size['height']
                print("size : ", ToutBons.size['height'])
                sc = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'ajax-infinite-scroll-feed')))
                footer = driver.find_element(By.ID, 'page-content').find_element(By.TAG_NAME, 'footer')
                if(sc.get_attribute("style") == "display: none;") and (last_height == new_height):
                    scroll = False
                else:
                    last_height = new_height
            ToutBons = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'grid-cards')))
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            bons = soup.find(class_= 'grid-cards')
            items = bons.find_all(class_= "masonry-grid-cards")
            print("****************** ", len(items))
            for item in items :
                try :
                    code = item.find(class_ = 'discount-coupon')['data-code-coupon']
                    nom = item.find(class_ = 'discount-coupon')['data-title']
                    reduction = item.find(class_= 'price-container').find(class_ = 'coupon-price').text.replace("-", "").replace("€", "")
                    description = item.find(class_= 'brand-corner-color').find(class_ = 'br-center-txt').find("div").text
                    imageCoupon = "https://www.mavieencouleurs.fr" + item.find(class_= 'price-container').find(class_ = 'image').find('img')['src']
                    imageMarque = "https://www.mavieencouleurs.fr" + item.find(class_= 'brand-info').find('img')['src']
                    marque = item.find(class_= 'brand-info').find("span").text
                    date = item.find(class_= 'br-center-txt').find(class_ = 'br-legal').text.replace("\n", "").replace("Jusqu’au", "").replace(" ", "")
                    data.append([nom, code, reduction, description, marque, date, imageCoupon, imageMarque, types[i], urls[i]])
                finally:
                    print("**********")
                    continue

if len(data) > 0 :
    if not os.path.exists('CouponsResults'):
        os.makedirs('CouponsResults')
        
    workbook = xlsxwriter.Workbook('CouponsResults/MaVieEnCouleurs.xlsx')
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