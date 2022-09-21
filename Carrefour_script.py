from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

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

categories = [
    "bio-et-ecologie",
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
adresse = "75012"

for cat in categories:
    data = []

    driver = webdriver.Chrome(PATH)

    url = "https://www.carrefour.fr/r/" + cat + "?filters%5BFacet_vendeurs%5D%5B0%5D=Carrefour&noRedirect=0"
    nb_page = 1

    #Set to -1 to make it unlimited ==========================================
    nb_max_pages = 10

    searching = True

    driver.get(url)

    try :
        input()
        myCookies = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID , 'onetrust-reject-all-handler')))
        myCookies.click()
    finally :
        try:
            #Choosing Drive ===========================================================================================================================
            choose_drive = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'pill-group__action')))
            choose_drive.click()
            results = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME , 'suggestions-input')))
            search = results.find_element(By.CLASS_NAME , 'pl-input-text__input--text')
            search.send_keys(adresse+'\n')
            sleep(2)
            search_ok = results.find_element(By.CLASS_NAME,"pl-input-text-group__append")
            search_ok.click()
            WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.CLASS_NAME , 'drive-service-list__list-item')))
            choices = driver.find_elements(By.CLASS_NAME,"drive-service-list__list-item")
            if len(choices)>0:
                choice_button_cont = choices[0].find_element(By.CLASS_NAME,"store-card__info-item")
                choice_button = choice_button_cont.find_element(By.CLASS_NAME,"pl-button")
                choice_button.click()
            sleep(5)

            #Begin Searching ======================================================================================================================
            while searching:
                if nb_page<nb_max_pages or nb_max_pages<0:
                    # items = driver.find_elements(By.CLASS_NAME , 'product-grid-item')
                    # items_arr = items[num:]
                    # for art in items_arr:
                    #     try:
                    #         item = art.find_element(By.CLASS_NAME, 'ds-product-card-refonte')
                    #         id = item.get_attribute("id")
                    #         image = item.find_element(By.TAG_NAME,"img").get_attribute("data-src")
                    #         name = item.find_element(By.CLASS_NAME , 'ds-title')
                    #         price = item.find_element(By.CLASS_NAME , 'product-price__amount-value')
                    #         print(num,[id,image,name.text,price.text])
                    #         data.append([id,image,name.text,price.text])
                    #         num += 1
                    #     except:
                    #         num += 1
                    #         continue

                    
                    #To the next Page =======================================
                    #Print Progress
                    if nb_max_pages>0:
                        print((nb_page/nb_max_pages)*100,"%")
                    else:
                        print((nb_page*60/534731)*100,"%")
                    
                    try:
                        button_next = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.pagination__button-wrap button.pl-button.pl-button--primary")))
                        button_next.click()
                        nb_page += 1
                    except:
                        searching = False
                else:
                    searching = False

            #Print Progress
            if nb_max_pages>0:
                print((nb_page/nb_max_pages)*100,"%")
            else:
                print((nb_page*60/534731)*100,"%")
            
            if nb_page>=nb_max_pages or nb_max_pages<0:
                searching = False
        finally:
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
            finally:
                driver.quit()

    #Save Data to Excel File ===============================================================================
    import xlsxwriter

    workbook = xlsxwriter.Workbook('Produits/75012/Carrefour'+ cat +'.xlsx')
    worksheet = workbook.add_worksheet("Listing")

    # Add a table to the worksheet.
    worksheet.add_table('A1:D{0}'.format(len(data)), {'data': data,
                                'columns': [{'header': 'CODE_BAR'},
                                            {'header': 'IMAGE'},
                                            {'header': 'DESIGNATION'},
                                            {'header': 'PRIX'},
                                            ]})

    workbook.close() 

print(" time : ", time.time() - start)