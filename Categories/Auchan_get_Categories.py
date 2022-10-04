import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

def cleanString(s):
    #Tout espace initial n'est pas contabilisé c'est pour cela que cpt=2
    cpt = 2
    r = ''
    for i in range(len(s)):
        if s[i] == ' ':
            cpt += 1
        else:
            if cpt == 1:
                r += ' '
            r += s[i]
            cpt = 0
    return r

def getAuchanCategories():
    PATH = "Web Drivers\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    url = "https://www.auchan.fr/"
    driver.get(url)

    categories = []
    souscategories = []
    links = []

    try :
        myCookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
        myCookies.click()
    finally:
        try:
            #Clicker sur le button Rayons =========================================
            rayons_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID , 'navigation')))
            rayons_button.click()

            #Lister les catégories ===================================================
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select('.navigation-layer__link')

            print("Extraction des catégories supérieures ...")

            for i in range(len(items)):
                item = items[i]
                name = item.find(class_='navigation-node__title').text.replace('\n','')
                name = cleanString(name)
                img_elem = item.select_one('.navigation-node__picture img')
                image = ""
                if 'srcset' in img_elem.attrs:
                    image = "https://auchan.fr"+img_elem['srcset']
                elif 'data-srcset' in img_elem.attrs:
                    image = "https://auchan.fr"+img_elem['data-srcset']
                elif 'src' in img_elem.attrs:
                    image = "https://auchan.fr"+img_elem['src']
                
                link = "https://www.auchan.fr"+item['href']
                link_split = link.split('/')
                categorie_id = name
                if len(link_split)>=2:
                    categorie_id = link_split[-2]
                
                links.append(categorie_id)

                categories.append({
                    "CATEGORIE_ID":categorie_id,
                    "CATEGORIE_NOM":name,
                    "IMAGE":image,
                })

            print("Extraction des sous-catégories ...")

            for i in range(len(links)):
                print("Progrès: "+str(i*100/len(links))+"%")
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.navigation-layer__link')))
                items_sel = driver.find_elements(By.CSS_SELECTOR,'.navigation-layer__link')
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.navigation-layer__link')))
                try:
                    name = items_sel[i].find_element(By.CLASS_NAME,'navigation-node__title').text.replace('\n','')
                    name = cleanString(name)
                    link = items_sel[i].get_attribute('href')
                    link_split = link.split('/')
                    categorie_id = name
                    if len(link_split)>=2:
                        categorie_id = link_split[-2]
                    
                    items_sel[i].click()
                    try:
                        button_back = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button.sublevel-head__back')))
                        time.sleep(3)
                        html = driver.page_source
                        soup = BeautifulSoup(html, "html.parser")
                        items = soup.select('div.sub-navigation.navigation-block.navigationBlock')
                        for item in items:
                            name = item.select_one('.navigation-block__title span').text.replace('\n','')
                            name = cleanString(name)
                            img_elem = item.select_one('.navigation-block__picture img')
                            image = ""
                            if 'srcset' in img_elem.attrs:
                                image = "https://auchan.fr"+img_elem['srcset']
                            elif 'data-srcset' in img_elem.attrs:
                                image = "https://auchan.fr"+img_elem['data-srcset']
                            elif 'src' in img_elem.attrs:
                                image = "https://auchan.fr"+img_elem['src']
                            
                            link = item.find(class_='navigation-block__head')['href']
                            link_split = link.split('/')
                            souscategorie_id = name
                            if len(link_split)>2:
                                souscategorie_id = link_split[-2]

                            souscategories.append({
                                "CATEGORIE_ID":categorie_id,
                                "SOUS_CATEGORIE_ID":souscategorie_id,
                                "SOUS_CATEGORIE_NOM":name,
                                "IMAGE":image,
                            })
                        button_back.click()
                    except:
                        driver.get(url)
                        #Clicker sur le button Rayons =========================================
                        rayons_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID , 'navigation')))
                        rayons_button.click()
                except Exception as e:
                    print(e)
                    pass
        finally:
            driver.quit()
    return categories,souscategories