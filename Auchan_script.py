from email.errors import FirstHeaderLineIsContinuationDefect
from lib2to3.pgen2.driver import Driver
from os import link
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import concurrent.futures
import requests
import xlsxwriter

 
PATH = "web Drivers\chromedriver.exe"
driver = webdriver.Chrome(PATH)
 
urls = [
	"https://www.auchan.fr/oeufs-produits-laitiers/cremerie-oeufs-laits/ca-n0101",
	"https://www.auchan.fr/oeufs-produits-laitiers/yaourts-fromages-blancs/ca-n0102",
	"https://www.auchan.fr/oeufs-produits-laitiers/desserts-compotes/ca-n0103",
	"https://www.auchan.fr/oeufs-produits-laitiers/fromages-a-deguster-a-la-coupe/ca-n0108",
	"https://www.auchan.fr/oeufs-produits-laitiers/fromages-a-cuisiner-aperitifs-rapes/ca-n0106",
	"https://www.auchan.fr/oeufs-produits-laitiers/fromages-a-cuisiner-aperitifs-rapes/ca-n0106",
	"https://www.auchan.fr/boucherie-volaille-poissonnerie/boucherie-volaille-poisson-bio-et-label/ca-n0207",
	"https://www.auchan.fr/boucherie-volaille-poissonnerie/volaille-lapin/ca-n0202",
	"https://www.auchan.fr/boucherie-volaille-poissonnerie/boucherie/ca-n0201",
	"https://www.auchan.fr/boucherie-volaille-poissonnerie/poissons-crustaces/ca-n0203",
	"https://www.auchan.fr/boucherie-volaille-poissonnerie/traiteur-de-la-mer/ca-n0204",
	"https://www.auchan.fr/charcuterie-traiteur-pain/charcuterie/ca-n1201",
	"https://www.auchan.fr/charcuterie-traiteur-pain/traiteur/ca-n1202",
	"https://www.auchan.fr/charcuterie-traiteur-pain/snacking-salade-plats-cuisines/ca-n1204",
	"https://www.auchan.fr/charcuterie-traiteur-pain/traiteur-vegetal/ca-n120201",
	"https://www.auchan.fr/charcuterie-traiteur-pain/pain-patisserie/ca-n1203",
	"https://www.auchan.fr/fruits-legumes/fruits-legumes-bio/ca-n0307",
	"https://www.auchan.fr/fruits-legumes/fruits/ca-n0301",
	"https://www.auchan.fr/fruits-legumes/legumes/ca-n0302",
	"https://www.auchan.fr/fruits-legumes/fruits-legumes-pret-a-consommer/ca-n0304",
	"https://www.auchan.fr/fruits-legumes/jus-de-fruits-frais-gazpacho/ca-n0305",
	"https://www.auchan.fr/surgeles/aperitifs-pizzas-plats-cuisines/ca-n0401",
	"https://www.auchan.fr/surgeles/legumes/ca-n0404",
	"https://www.auchan.fr/surgeles/frites-pommes-de-terre/ca-n0403",
	"https://www.auchan.fr/surgeles/viandes-poissons/ca-n0406",
	"https://www.auchan.fr/surgeles/glaces-viennoiseries/ca-n0408",
	"https://www.auchan.fr/epicerie-sucree/cafes/ca-n0502",
	"https://www.auchan.fr/epicerie-sucree/petit-dejeuner-thes-chocolats-en-poudre/ca-n0503",
	"https://www.auchan.fr/epicerie-sucree/biscuits-gateaux/ca-n0505",
	"https://www.auchan.fr/epicerie-sucree/chocolats-confiseries/ca-n0507",
	"https://www.auchan.fr/epicerie-sucree/desserts-sucres-farines-dietetique/ca-n0511",
	"https://www.auchan.fr/epicerie-salee/aperitif/ca-n0601",
	"https://www.auchan.fr/epicerie-salee/huiles-sauces-aides-culinaires/ca-n0608",
	"https://www.auchan.fr/epicerie-salee/conserves-soupes/ca-n0607",
	"https://www.auchan.fr/epicerie-salee/pates-riz-legumes-secs/ca-n0605",
	"https://www.auchan.fr/epicerie-salee/plats-cuisines-produits-du-monde/ca-n0606",
	"https://www.auchan.fr/boissons-sans-alcool/eaux-laits/ca-n0701",
	"https://www.auchan.fr/boissons-sans-alcool/jus-de-fruits-jus-de-legumes/ca-n0704",
	"https://www.auchan.fr/boissons-sans-alcool/colas-boissons-gazeuses-energisantes/ca-n0706",
	"https://www.auchan.fr/boissons-sans-alcool/thes-boissons-plates-aux-fruits-sirops/ca-n0711",
	"https://www.auchan.fr/boissons-sans-alcool/bieres-vins-et-aperitifs-sans-alcool/ca-n071401",
	"https://www.auchan.fr/bebe/bebe-bio-ecologique/ca-n0804",
	"https://www.auchan.fr/bebe/laits-petits-dejeuners-de-bebe/ca-n0801",
	"https://www.auchan.fr/bebe/repas-desserts-gouters-de-bebe/ca-n0802",
	"https://www.auchan.fr/bebe/couches-toilette-de-bebe/ca-n0806",
	"https://www.auchan.fr/bebe/puericulture-vetements-bebe/ca-31032021170201",
	"https://www.auchan.fr/hygiene-beaute-parapharmacie/soins-du-visage-hygiene-dentaire-maquillage/ca-n0904",
	"https://www.auchan.fr/hygiene-beaute-parapharmacie/hygiene-soins-du-corps/ca-n0902",
	"https://www.auchan.fr/hygiene-beaute-parapharmacie/soins-des-cheveux/ca-n0903",
	"https://www.auchan.fr/hygiene-beaute-parapharmacie/hygiene-soins-homme/ca-n0908",
	"https://www.auchan.fr/hygiene-beaute-parapharmacie/mouchoirs-protections-hygieniques-petite-parapharmacie/ca-n0909",
	"https://www.auchan.fr/entretien-maison/papier-toilette-essuie-tout-mouchoir/ca-n1002",
	"https://www.auchan.fr/entretien-maison/soin-du-linge/ca-n1003",
	"https://www.auchan.fr/entretien-maison/produits-de-nettoyage-vaisselle/ca-n1004",
	"https://www.auchan.fr/entretien-maison/accessoires-menagers/ca-n1011",
	"https://www.auchan.fr/entretien-maison/bazar/ca-n21",
	"https://www.auchan.fr/animalerie/chat/ca-n1101",
	"https://www.auchan.fr/animalerie/chien/ca-n1102",
	"https://www.auchan.fr/animalerie/rongeurs-oiseaux-poissons/ca-n1103",
	"https://www.auchan.fr/animalerie/accessoires-animalerie/ca-n1104",
	"https://www.auchan.fr/produits-de-nos-regions-et-du-monde/asie/ca-b0801",
	"https://www.auchan.fr/produits-de-nos-regions-et-du-monde/amerique-tex-mex/ca-b0804",
	"https://www.auchan.fr/produits-de-nos-regions-et-du-monde/moyen-orient-halal/ca-b0805",
	"https://www.auchan.fr/produits-de-nos-regions-et-du-monde/mediterranee/ca-b0807",
	"https://www.auchan.fr/produits-de-nos-regions-et-du-monde/produits-de-nos-regions/ca-b18",
	"https://www.auchan.fr/snacking-plats-cuisines/snack-froid/ca-b1209",
	"https://www.auchan.fr/snacking-plats-cuisines/snack-chaud/ca-b1210",
	"https://www.auchan.fr/snacking-plats-cuisines/plats-cuisines/ca-b1204",
	"https://www.auchan.fr/snacking-plats-cuisines/boissons-desserts/ca-b1206",
	"https://www.auchan.fr/regimes-alimentaires-et-nutrition/vegetarien-vegetal/ca-b0201",
	"https://www.auchan.fr/regimes-alimentaires-et-nutrition/regimes-alimentaires-specifiques/ca-b0202",
	"https://www.auchan.fr/regimes-alimentaires-et-nutrition/bien-etre-minceur-complements-alimentaires/ca-b0203",
	"https://www.auchan.fr/produits-auchan/ca-b202209131609",
	"https://www.auchan.fr/jardin-auto-brico/jardin/ca-15400",
	"https://www.auchan.fr/jardin-auto-brico/bricolage/ca-7135356",
	"https://www.auchan.fr/jardin-auto-brico/auto-moto/ca-7290055",
    "https://www.auchan.fr/electromenager-cuisine/gros-electromenager/ca-8100",
    "https://www.auchan.fr/electromenager-cuisine/petits-appareils-de-cuisine/ca-7328305",
    "https://www.auchan.fr/electromenager-cuisine/cuisine-arts-de-la-table/ca-7173353",
    "https://www.auchan.fr/electromenager-cuisine/entretien-de-la-maison/ca-201612151001",
    "https://www.auchan.fr/electromenager-cuisine/entretien-du-linge/ca-201907091649",
    "https://www.auchan.fr/electromenager-cuisine/beaute-bien-etre/ca-9384653",
    "https://www.auchan.fr/electromenager-cuisine/climatisation-chauffage/ca-7328314",
    "https://www.auchan.fr/electromenager-cuisine/nouveautes-electromenager-cuisine/ca-888000008",
    "https://www.auchan.fr/meuble-deco-linge-de-maison/meubles-canapes/ca-2014110310",
    "https://www.auchan.fr/meuble-deco-linge-de-maison/literie/ca-7196510",
    "https://www.auchan.fr/meuble-deco-linge-de-maison/linge-de-maison/ca-7882903",
    "https://www.auchan.fr/meuble-deco-linge-de-maison/decoration/ca-201510271523",
]

adresse = "01600"

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
for url in urls:
    start_time = time.time()
    driver.get(url)

    try :
        if first:
            myCookies = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID , 'onetrust-accept-btn-handler')))
            myCookies.click()
    finally:
        try:
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
            while searching:
                try:
                    button_next = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a.pagination-adjacent__link i.icon-arrowRight")))
                    footer = driver.find_element(By.ID,"cms-slot-footerSlot")
                    driver.execute_script("window.scrollTo(0, {0})".format(footer.location["y"]-600))
                except Exception as e:
                    searching = False

            #Iterating in products ==============================================================================================================
            #Save the html page ==========================================
            WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".list__item .product-thumbnail__picture img")))
            WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".list__item .product-thumbnail__details-wrapper")))
            WebDriverWait(driver,20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,".list__item .product-thumbnail__description")))
            html = driver.page_source
            #open the page with beautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            items = soup.find_all(class_="list__item")
            links = []
            infos = []
            #iterate in products
            cpt = 0
            for item in items:
                try:
                    id_link = "https://www.auchan.fr"+item.find(class_="product-thumbnail__details-wrapper")["href"]
                    img_wrapper = item.find(class_="product-thumbnail__picture")
                    img_elem = img_wrapper.find("img")
                    image = ""
                    if 'srcset' in img_elem.attrs:
                        image = img_elem['srcset']
                    elif 'data-srcset' in img_elem.attrs:
                        image = img_elem['data-srcset']
                    name = item.find(class_='product-thumbnail__description')
                    price = item.find(class_='product-price')
                    cpt+=1
                    infos.append([name.text.replace('\n','').replace('\t',''), image, price.text])
                    links.append(id_link)
                except:
                    pass
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                id_product = executor.map(get_link, links)
            id_product=list(id_product)
            print(len(id_product),len(infos),len(links))
            for i in range(0, len(id_product)):
                infos[i].append(id_product[i][0])

            #Save Data to Excel File ===============================================================================
            workbook = xlsxwriter.Workbook('Produits/Auchan/Auchan_' + url.split("/")[-3] + '_' + url.split("/")[-2] + '.xlsx')
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
        except:
            pass
print("End")
driver.quit()