from email import header
from email.errors import FirstHeaderLineIsContinuationDefect
from lib2to3.pgen2.driver import Driver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import concurrent.futures
import requests
import xlsxwriter
import os

 
PATH = "web Drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)

nb_page = 0

#Changez ce paramètres selon la mémoire de votre machine
nb_max_pages = 3
 
url = "https://www.auchan.fr/boutique/promos"

adresse = "33300"
all_products = False

def get_link(link):
    ids = []
    page = requests.get(link)
    temp_soup = BeautifulSoup(page.content,"html.parser")
    features = temp_soup.find_all(class_="product-description__feature-wrapper")
    id = features[len(features)-1].find(class_="product-description__feature-values").text.replace('\n','').replace('\t','')
    # print(id)
    ids.append(id)
    return ids

first = True
start_time = time.time()
driver.get(url)

try :
    if first:
        myCookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
        myCookies.click()
        if all_products:
            first = False
finally:
    try:
        if not(all_products):
            if first:
                #Choosing Drive =======================================================================================================
                button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , 'context-header__button')))
                button.click()
                search = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME , 'journey__search-input')))
                search.send_keys(adresse)
                suggestions= WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID , 'search_suggests')))
                elem = suggestions.find_element(By.TAG_NAME , 'li')
                elem.click()
                WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME , 'btnJourneySubmit')))
                choices = driver.find_elements(By.CLASS_NAME , 'btnJourneySubmit')
                if len(choices) > 1:
                    choice = choices[1]
                else:
                    choice = choices[0]
                choice.click()
                first = False
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-price')))
        #Navigating pages =======================================================================================================
        searching = True
        sameUrl = True
        nb_page = 0
        nb_page_cpt = 1
        data = []

        while sameUrl:
            if nb_page != 0:
                driver.get(url+'?page='+str(nb_page+1))
                searching = True
            while searching:
                try:
                    button_next = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"nav.pagination-main__container a.pagination-adjacent__link i.icon-arrowRight")))
                    footer = driver.find_element(By.ID,"cms-slot-footerSlot")
                    driver.execute_script("window.scrollTo(0, {0})".format(footer.location["y"]-600))
                    if "?page=" in driver.current_url:
                        nb_page = int(driver.current_url.split('?page=',1)[1])
                    else:
                        nb_page = 1
                    if nb_page>=nb_max_pages*nb_page_cpt:
                        searching = False
                        nb_page_cpt += 1
                except Exception as e:
                    searching = False
                    sameUrl = False
                    
            #Iterating in products ==============================================================================================================
            #Save the html page ==========================================
            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-price')))
            html = driver.page_source
            #open the page with beautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            print("-------------------")
            items = soup.find_all(class_="list__item")
            print(len(items))
            links = []
            infos = []
            #iterate in products
            cpt = 0
            for item in items:
                try:
                    id_link = "https://www.auchan.fr"+item.find(class_="product-thumbnail__details-wrapper")["href"]
                    promo = "vide"
                    productHeader = "vide"
                    try :
                        promo = item.find(class_='product-discount').text
                    except:
                        continue
                    try :
                        productHeader = item.find(class_='product-thumbnail__header').text
                    except:
                        continue
                    price = item.find(class_='product-price').text
                    cpt+=1
                    infos.append([productHeader, promo, price])
                    print([productHeader, promo, price])
                    links.append(id_link)
                except:
                    pass

            with concurrent.futures.ThreadPoolExecutor() as executor:
                id_product = executor.map(get_link, links)
            id_product=list(id_product)
            print(len(id_product),len(infos),len(links))
            for i in range(0, len(id_product)):
                infos[i].append(id_product[i][0])
            data += infos

        # Save Data to Excel File ===============================================================================
        # Create Folder if not exist
            if not os.path.exists('Produits/Auchan'):
                os.makedirs('Produits/Auchan')
        
        workbook = xlsxwriter.Workbook('Produits/Auchan/Auchan_Promotion_' + adresse + '.xlsx')
        worksheet = workbook.add_worksheet("Listing")

        # Add a table to the worksheet.
        worksheet.add_table('A1:D{0}'.format(len(data)), {'data': data,
                                    'columns': [{'header': 'PRODUCT_HEADER'},
                                                {'header': 'PROMO'},
                                                {'header': 'PRIX'},
                                                {'header': 'CODE_BAR'},
                                                ]})
        workbook.close()
        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        pass
print("End")
driver.quit()