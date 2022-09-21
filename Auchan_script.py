from os import link
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import concurrent.futures
import requests
 
PATH = "Web Drivers/chromedriver.exe"
driver = webdriver.Chrome(PATH)
 
url = "https://www.auchan.fr/boissons-sans-alcool/eaux-laits/ca-n0701"
adresse = "95000"

def get_link(link):
    ids = []
    page = requests.get(link)
    temp_soup = BeautifulSoup(page.content,"html.parser")
    features = temp_soup.find_all(class_="product-description__feature-wrapper")
    id = features[len(features)-1].find(class_="product-description__feature-values").text.replace('\n','').replace('\t','')
    # print(id)
    ids.append(id)
    return ids

start_time = time.time()
driver.get(url)

print("before")
print(driver.title)
try :
    myCookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
    myCookies.click()
finally:
    try:
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
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME , 'product-price')))
        #Navigating pages =======================================================================================================
        searching = True
        while searching:
            try:
                button_next = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a.pagination-adjacent__link i.icon-arrowRight")))
                footer = driver.find_element(By.ID,"cms-slot-footerSlot")
                driver.execute_script("window.scrollTo(0, {0})".format(footer.location["y"]))
            except Exception as e:
                searching = False
            print(searching)

        #Iterating in products ==============================================================================================================
        #Save the html page ==========================================
        html = driver.page_source
        #open the page with beautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        items = soup.find_all(class_="list__item")
        links = []
        infos = []
        #iterate in products
        print("*******************************")
        cpt = 0
        index = 0
        while index<len(items):
            try:
                item = items[index]
                id_link = "https://www.auchan.fr"+item.find(class_="product-thumbnail__details-wrapper")["href"]
                # print(id_link)
                links.append(id_link)
                img_wrapper = item.find(class_="product-thumbnail__picture")
                image = img_wrapper.find("img")["srcset"]
                name = item.find(class_='product-thumbnail__description')
                price = item.find(class_='product-price')
                cpt+=1
                infos.append([name.text.replace('\n','').replace('\t',''), image, price.text])
                index += 1
            except:
                pass
        with concurrent.futures.ThreadPoolExecutor() as executor:
            id_product = executor.map(get_link, links)
        print("*************************")
        id_product=list(id_product) 
        for i in range(0, len(id_product)):
            infos[i].append(id_product[i][0])
        print("*************************")
        print(infos)
    finally:
        print("End")
        driver.quit()

#Save Data to Excel File ===============================================================================
import xlsxwriter

workbook = xlsxwriter.Workbook('Auchan.xlsx')
worksheet = workbook.add_worksheet("Listing")

# Add a table to the worksheet.
worksheet.add_table('A1:D{0}'.format(len(infos)), {'data': infos,
                               'columns': [{'header': 'DESIGNATION'},
                                           {'header': 'IMAGE'},
                                           {'header': 'PRIX'},
                                           {'header': 'CODE_BAR'},
                                           ]})

workbook.close() 
print("--- %s seconds ---" % (time.time() - start_time))