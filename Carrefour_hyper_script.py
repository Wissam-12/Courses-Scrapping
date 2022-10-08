from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import xlsxwriter
import os


#Liste de codes postaux ========================================================================================

magasins = [
    "16000",
    "72015",
]


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

url = "https://www.carrefour.fr/r/" + categories[0] + "?filters%5BFacet_vendeurs%5D%5B0%5D=Carrefour&noRedirect=0"

#Set to -1 to make it unlimited ==========================================
nb_max_pages = 25
#Change to True to get all Carrefour products without price
all_products = True

driver.get(url)
first = True #Check if driver got first page
cpt = 0 #Check Progress in categories

#all_products don't have market
if all_products:
    magasins = [""]

try :
    myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-reject-all-handler')))
    myCookies.click()
finally :
    for index in range(len(magasins)):
        try:
            found_hyper = False
            if not(all_products):
                #Choosing Drive ===========================================================================================================================
                choose_drive = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'pill-group__action')))
                choose_drive.click()
                if id>0:
                    change_drive = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CSS_SELECTOR , '.pl-button-deprecated.drive-service-summary__action.pl-button-deprecated--tertiary')))
                    change_drive.click()
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
                for cat in categories:
                    if not(first):
                        url = "https://www.carrefour.fr/r/" + cat + "?filters%5BFacet_vendeurs%5D%5B0%5D=Carrefour&noRedirect=0"
                        driver.get(url)
                        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,'product-grid-item')))
                    else:
                        first = False

                    sameUrl = True
                    searching = True
                    nb_page_cpt = 1
                    nb_page = 0
                    data = []
                    while sameUrl:
                        if nb_page != 0:
                            driver.get(url+'&page='+str(nb_page+1))
                            WebDriverWait(driver,30).until(EC.presence_of_element_located((By.CLASS_NAME,'product-grid-item')))
                            searching = True
                        #Begin Searching ======================================================================================================================
                        if "&page=" in driver.current_url:
                            nb_page = int(driver.current_url.split('&page=',1)[1])
                        else:
                            nb_page = 1
                        while searching:
                            #To the next Page =======================================
                            try:
                                if nb_page>=nb_max_pages*nb_page_cpt:
                                    searching = False
                                    nb_page_cpt += 1
                                else:
                                    button_next = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"footer#data-voir-plus div.pagination__button-wrap button.pl-button-deprecated.pl-button-deprecated--primary")))
                                    button_next.click()
                                    sleep(1)
                                    if "&page=" in driver.current_url:
                                        nb_page = int(driver.current_url.split('&page=',1)[1])
                                    else:
                                        nb_page = 1
                            except:
                                searching = False
                                sameUrl = False

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
                        except:
                            pass
                            
                    #Save Data to Excel File ==================================================-=============================
                    #Create Folder if not exist
                    if not(all_products):
                        if not os.path.exists('Produits/Prix/Carrefour_hyper/Carrefour-'+magasins[index]):
                            os.makedirs('Produits/Prix/Carrefour_hyper/Carrefour-'+magasins[index])
                        
                        workbook = xlsxwriter.Workbook('Produits/Prix/Carrefour_hyper/Carrefour-'+magasins[index]+'/Carrefour-'+ cat +'.xlsx')
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
                        if not os.path.exists('Produits/Carrefour'):
                            os.makedirs('Produits/Carrefour')
                        
                        workbook = xlsxwriter.Workbook('Produits/Carrefour/Carrefour-'+ cat +'.xlsx')
                        worksheet = workbook.add_worksheet("Listing")

                        # Add a table to the worksheet.
                        worksheet.add_table('A1:D{0}'.format(len(data)), {'data': data,
                                                    'columns': [{'header': 'CODE_BAR'},
                                                                {'header': 'IMAGE'},
                                                                {'header': 'DESIGNATION'},
                                                                {'header': 'PRIX'},
                                                                ]})

                        workbook.close()

                    #Print Progress
                    cpt+=1
                    print(cpt*100/len(categories),"%")
                        
            else:
                print("Aucun Hyper pour ce code postal")  
        except:
            pass

driver.quit()        

print(" time : ", time.time() - start)