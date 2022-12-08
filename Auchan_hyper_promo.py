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

magasins = [
    "02500"
]
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

def checkIfHyper(name):
    return not("Supermarché" in name)

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
    for index in range(len(magasins)):
        found_magasin = False
        first = True
        try:
            if not(all_products):
                if first:
                    #Choosing Drive =======================================================================================================
                    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , 'context-header__button')))
                    button.click()
                    search = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME , 'journey__search-input')))
                    search.send_keys(magasins[index])
                    suggestions= WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID , 'search_suggests')))
                    elem = suggestions.find_element(By.TAG_NAME , 'li')
                    elem.click()
                    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME , 'btnJourneySubmit')))
                    choices = driver.find_elements(By.CLASS_NAME , 'journey-offering-context__wrapper')
                    time.sleep(5)

                    choice = None
                    for i in range(len(choices)):
                        name = choices[i].find_element(By.CLASS_NAME,'journey-offering-context__name').text
                        if(checkIfHyper(name)):
                            choice = choices[i].find_element(By.CLASS_NAME,'btnJourneySubmit')
                            found_magasin = True
                            break
                    
                    if found_magasin:
                        choice.click()
                    time.sleep(5)
                    first = False
                if found_magasin:
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-price')))
            if found_magasin:
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
                    # print("-------------------")
                    items = soup.find_all(class_="list__item")
                    # print(len(items))
                    links = []
                    infos = []
                    #iterate in products
                    cpt = 0
                    for item in items:
                        try:
                            #print("*****************************")
                            id_link = "https://www.auchan.fr"+item.find(class_="product-thumbnail__details-wrapper")["href"]
                            promoRef = []
                            promo = ""
                            productHeader = "vide"
                            # product-thumbnail__commercials
                            try :
                                promoRef = item.find_all(class_='product-discount-label')
                            finally :
                                try :
                                    promoRef += item.find_all(class_='product-discount')
                                    for onePromo in promoRef:
                                        promo += onePromo.text + " | "
                                    # print(promo)
                                finally:
                                    try :
                                        productHeader = item.find(class_='product-thumbnail__header').text
                                    finally:
                                        price = item.find(class_='product-price').text
                                        cpt+=1
                                        infos.append([productHeader, promo, price])
                                        print(cpt ,[productHeader, promo, price])
                                        links.append(id_link)
                        except:
                            # print("probleeeeeeeme")
                            continue

                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        id_product = executor.map(get_link, links)
                    id_product=list(id_product)
                    # print(len(id_product),len(infos),len(links))
                    for i in range(0, len(id_product)):
                        infos[i].append(id_product[i][0])
                    data += infos

                # Save Data to Excel File ===============================================================================
                # Create Folder if not exist
                    if not os.path.exists('Promotions/Auchan_hyper'):
                        os.makedirs('Promotions/Auchan_hyper')
                
                workbook = xlsxwriter.Workbook('Promotions/Auchan_hyper/Auchan_' + magasins[index] + '.xlsx')
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
        except Exception as e:
            print(e)
            pass
print("End")
# driver.quit()