from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import xlsxwriter
import os

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

def checkIfMarket(name):
    return "Market" in name

categories = [
    # "bio-et-ecologie",
    "fruits-et-legumes",
    "viandes-et-poissons",
    "pains-et-patisseries",
    "frais",
    "surgeles",
    "boissons",
    "epicerie-salee",
    "epicerie-sucree",
    "produits-du-monde",
    "hygiene-et-beaute",
    "entretien-et-nettoyage",
    "bebe",
]

start = time.time()
PATH = "Web Drivers\chromedriver.exe"
adresse = "59000"

driver = webdriver.Chrome(PATH)
driver.maximize_window()

url = "https://www.carrefour.fr/r/" + categories[0] + "?filters%5BFacet_vendeurs%5D%5B0%5D=Carrefour&noRedirect=0"

#Set to -1 to make it unlimited ==========================================
nb_max_pages = -1
#Change to True to get all Carrefour products without price
all_products = False

driver.get(url)
first = True #Check if driver got first page
cpt = 0 #Check Progress in categories

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-reject-all-handler')))
    myCookies.click()
finally :
    try:
        if not(all_products):
            #Choosing Drive ===========================================================================================================================
            choose_drive = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'pill-group__action')))
            choose_drive.click()
            results = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'suggestions-input')))
            search = results.find_element(By.CLASS_NAME , 'pl-input-text__input--text')
            search.send_keys(adresse)
            search.click()
            sleep(1)
            search_choices = driver.find_elements(By.CSS_SELECTOR,'ul.suggestions-input__suggestions li')
            search_choices[1].click()
            sleep(1)
            search_ok = results.find_element(By.CLASS_NAME,"pl-input-text-group__append")
            search_ok.click()
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME , 'drive-service-list__list-item')))
            choices = driver.find_elements(By.CLASS_NAME,"drive-service-list__list-item")

            found_market = False

            for choice in choices:
                choice_button_cont = choice.find_element(By.CLASS_NAME,"store-card__info-item")
                choice_name = choice.find_element(By.CSS_SELECTOR,'.ds-title.ds-title--s').text
                if checkIfMarket(choice_name):
                    try:
                        choice_button = choice_button_cont.find_element(By.CLASS_NAME,"pl-button-deprecated")
                        choice_button.click()
                        found_market = True
                        break
                    except:
                        pass
            if found_market:
                sleep(5)

        if found_market:
            for cat in categories:
                nb_page = 1
                data = []
                if not(first):
                    url = "https://www.carrefour.fr/r/" + cat + "?filters%5BFacet_vendeurs%5D%5B0%5D=Carrefour&noRedirect=0"
                    driver.get(url)
                else:
                    first = False
                searching = True
                #Begin Searching ======================================================================================================================
                while searching:
                    if nb_page<nb_max_pages or nb_max_pages<0:
                        #To the next Page =======================================
                        try:
                            button_next = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.pagination__button-wrap button.pl-button-deprecated.pl-button-deprecated--primary")))
                            button_next.click()
                            nb_page += 1
                        except:
                            searching = False
                    else:
                        searching = False

                #Print Progress
                cpt+=1
                print(cpt*100/len(categories),"%")
                
                if nb_page>=nb_max_pages or nb_max_pages<0:
                    searching = False

                try:
                    sleep(5)
                    # WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME,"product-grid-item")))
                    # items = driver.find_elements(By.CLASS_NAME , 'product-grid-item')
                    # for item in items:
                    #     data.append(getArticleInfo(item))
                    # # pool = Pool(5)
                    # # data = pool.map(getArticleInfo, items)
                    # print("Data :",len(data))

                    #Save the html page ==========================================
                    html = driver.page_source
                    #open the page with beautifulSoup
                    soup = BeautifulSoup(html, "html.parser")
                    items = soup.find_all("li", class_="product-grid-item")
                    #iterate in products
                    for art in items:
                        try:
                            item = art.find(class_='ds-product-card-refonte')
                            id = item["id"]
                            image = item.find("img")["data-src"]
                            name = item.find(class_='ds-title')
                            price = item.find(class_='product-price__amount-value')
                            data.append([id,image,name.text,price.text])
                        except:
                            continue
                    
                    #Save Data to Excel File ===============================================================================
                    #Create Folder if not exist
                    if not os.path.exists('Produits/Carrefour_market'):
                        os.makedirs('Produits/Carrefour_market')
                    
                    workbook = xlsxwriter.Workbook('Produits/Carrefour_market/Carrefour-'+ cat +'.xlsx')
                    worksheet = workbook.add_worksheet("Listing")

                    # Add a table to the worksheet.
                    worksheet.add_table('A1:D{0}'.format(len(data)), {'data': data,
                                                'columns': [{'header': 'CODE_BAR'},
                                                            {'header': 'IMAGE'},
                                                            {'header': 'DESIGNATION'},
                                                            {'header': 'PRIX'},
                                                            ]})

                    workbook.close() 
                except:
                    pass  
        else:
            print("Aucun Market pour ce code postal")
    finally:
        driver.quit()
        

print(" time : ", time.time() - start)