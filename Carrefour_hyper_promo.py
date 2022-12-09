from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import xlsxwriter
import os
import math


#Liste de codes postaux ========================================================================================

magasins = [
    "16000",
    "59160",
]

def chunks(l, n):
    """Yield n number of striped chunks from l."""
    for i in range(0, n):
        yield l[i::n]

def getArticleInfo(art):
    try:
        item = art.find_element(By.CLASS_NAME, 'ds-product-card-refonte')
        id = item.get_attribute("id")
        image = item.find_element(By.TAG_NAME,"img").get_attribute("data-src")
        name = item.find_element(By.CLASS_NAME , 'ds-title')
        price = item.find_element(By.CLASS_NAME , 'product-price__amount-value')
        print([id,image,name.text,price.text])
        return [id,image,name.text,price.text]
    except:
        return []

def checkIfHyper(name):
    return not("Market" in name) and not("City " in name) and not("Express " in name) and not("Contact " in name) and not("Bio " in name) and not("Montagne " in name)


start = time.time()
PATH = "Web Drivers\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.maximize_window()

url = "https://www.carrefour.fr/"

#Set to -1 to make it unlimited ==========================================
nb_max_pages = 5
nb_page_cpt = 1
#Change to True to get all Carrefour products without price
all_products = False

driver.get(url)
first = True #Check if driver got first page
cpt = 0 #Check Progress in categories

#all_products don't have market
if all_products:
    magasins = [""]

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-reject-all-handler')))
    myCookies.click()
    rayonsButton = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME , 'mainbar__nav-toggle-icon')))
    rayonsButton.click()
    promotionsButton = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME , 'nav-item__link--promotion')))
    promotionsButton.click()
finally:
    for index in range(len(magasins)):
        try:
            print(magasins)
            print(index)
            found_hyper = False
            if not(all_products):
                if index>0:
                     driver.execute_script("window.scrollTo(0, 0)")
                #Choosing Drive ===========================================================================================================================
                choose_drive = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'pill-group__action')))
                choose_drive.click()
                # else:
                #     print("immmm")
                if index>0:
                    change_drive = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR , '.pl-button-deprecated.drive-service-summary__action.pl-button-deprecated--tertiary')))
                    change_drive.click()
                print("*****************")
                results = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'suggestions-input')))
                search = results.find_element(By.CLASS_NAME , 'pl-input-text__input--text')
                search.send_keys(magasins[index])
                search.click()
                sleep(1)
                search_choices = []
                while len(search_choices)<2:
                    search_choices = driver.find_elements(By.CSS_SELECTOR,'ul.suggestions-input__suggestions li')
                    sleep(1)
                search_choices[1].click()
                sleep(1)
                search_ok = results.find_element(By.CLASS_NAME,"pl-input-text-group__append")
                search_ok.click()
                WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME , 'drive-service-list__list-item')))
                choices = driver.find_elements(By.CLASS_NAME,"drive-service-list__list-item")
                for choice in choices:
                    choice_button_cont = choice.find_element(By.CLASS_NAME,"store-card__info-item")
                    choice_name = choice.find_element(By.CSS_SELECTOR,'.ds-title.ds-title--s').text

                    if checkIfHyper(choice_name):
                        try:
                            choice_button = choice_button_cont.find_element(By.CLASS_NAME,"pl-button-deprecated")
                            choice_button.click()
                            found_hyper = True
                            break
                        except:
                            pass
                if found_hyper:
                    sleep(5)

            if found_hyper or all_products:
                # ------------------------------ Nombre de pages ----------------------------------
                WebDriverWait(driver,60).until(EC.presence_of_element_located((By.CLASS_NAME , 'search-results-count--promotion')))
                promonb = driver.find_element(By.CLASS_NAME,"search-results-count--promotion").text
                NBpromoPage = math.ceil(int(promonb.split()[0])/30)
                # -----------------------------------------------------------------------------------
                searching = True
                sameUrl = True
                nb_page = 0
                data = []
                while sameUrl:
                    if nb_page != 0:
                        if(nb_page <= NBpromoPage):
                            nb_page += 1
                            driver.get(url+'?page='+str(nb_page))
                            searching = True
                    while searching:
                        try:
                            footer = driver.find_element(By.ID,"colophon")
                            driver.execute_script("window.scrollTo(0, {0})".format(footer.location["y"]-600))
                            if "page=" in driver.current_url:
                                nb_page = int(driver.current_url.split('page=',1)[1])
                            else:
                                nb_page = 1
                            print("-----------------------------------")
                            if(( nb_page >= nb_max_pages*nb_page_cpt) or (nb_page >= NBpromoPage)):
                                searching = False
                                nb_page_cpt += 1
                        except Exception as e:
                            searching = False
                            sameUrl = False
                            
                    #Iterating in products ==============================================================================================================
                    #Save the html page ==========================================
                    print("save data")
                    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-price__amounts')))
                    html = driver.page_source
                    #open the page with beautifulSoup
                    soup = BeautifulSoup(html, "html.parser")
                    print("-------------------")
                    items = soup.find_all(class_="product-grid-item")
                    print(len(items))
                    #iterate in products
                    cpt = 0
                    for item in items:
                        try:
                            print("*****************************")
                            promoRef = []
                            promo = ""
                            # product-thumbnail__commercials
                            try :
                                promoRef = item.find_all(class_='promotion-description__labels')
                            finally :
                                try :
                                    for onePromo in promoRef:
                                        promo += onePromo.text + " | "
                                    print(promo)
                                finally:
                                    price = item.find(class_='product-price__amount-value').text
                                    code = item.find(class_='ds-product-card-refonte')["id"]
                                    data.append([code, promo, price])
                                    print([code, promo, price])
                        except:
                            print("probleeeeeeeme")
                            continue
                    
                
                #Save Data to Excel File ==================================================-=============================
                #Create Folder if not exist
                if not(all_products):
                    if not os.path.exists('Promotions/Carrefour_hyper'):
                        os.makedirs('Promotions/Carrefour_hyper')
                    
                    workbook = xlsxwriter.Workbook('Promotions/Carrefour_hyper/Carrefour-'+magasins[index]+'.xlsx')
                    worksheet = workbook.add_worksheet("Listing")

                    # Add a table to the worksheet.
                    worksheet.add_table('A1:D{0}'.format(len(data)), {'data': data,
                                                'columns': [{'header': 'CODE_BAR'},
                                                            {'header': 'PROMOTION'},
                                                            {'header': 'PRIX'},
                                                            ]})
                    workbook.close()
                else:
                    if not os.path.exists('Promotions/Carrefour'):
                        os.makedirs('Promotions/Carrefour')
                    
                    workbook = xlsxwriter.Workbook('Produits/Carrefour/Carrefour.xlsx')
                    worksheet = workbook.add_worksheet("Listing")

                    # Add a table to the worksheet.
                    worksheet.add_table('A1:D{0}'.format(len(data)), {'data': data,
                                                'columns': [{'header': 'CODE_BAR'},
                                                            {'header': 'IMAGE'},
                                                            {'header': 'DESIGNATION'},
                                                            {'header': 'PRIX'},
                                                            ]})

                    workbook.close()
                    
            else:
                print("Aucun Hyper pour ce code postal")  
        except:
            pass
        #Print Progress
        cpt+=1
        print(cpt*100/len(magasins),"%")

driver.quit()        

print(" time : ", time.time() - start)