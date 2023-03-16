from driver_configuration import Driver_configuration
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm
import pandas as pd
from datetime import datetime
from pytz import timezone


start = time.time()

chrome_driver =  Driver_configuration().create_driver()

chrome_driver.get('https://muebleschile.cl/')

# WebElement de las categorias (sofa,silla,comedor, etc...)
categorias_list = chrome_driver.find_elements(By.CLASS_NAME,"woo_category")

categorias_link = []
for categoria in categorias_list:
    # Lista que posee los links de cada categoria en particular
    categorias_link.append((categoria.find_element(By.TAG_NAME,'a')).get_attribute("href"))

productos_link = []
categoria_link_pd = []
for categoria_link in categorias_link:
    # Accedo una por una a las categorias
    print(categoria_link)
    chrome_driver.get(categoria_link)

    sigueinte = 1
    # Busco los productos en esa pagina de la categoria
    while sigueinte == 1:
        productos_class = chrome_driver.find_elements(By.XPATH,'.//*[contains(@class, "elab_woocommerce_content_image elab_woocoommerce_product_image")]')
        
        for producto_class in productos_class:
            # Obtengo los links a cada uno de los productos
            productos_link.append((producto_class.find_element(By.TAG_NAME,'a')).get_attribute("href"))
            categoria_link_pd.append((categoria_link))
        try:
            # Hacemos click en siguiente, en caso de no encontrarlo pasamos a la siguiente categoria
            siguiente_button = chrome_driver.find_element(By.XPATH,'.//*[contains(@class, "next page-numbers")]')
            chrome_driver.execute_script("arguments[0].click();", siguiente_button)
        except Exception as e:
            sigueinte = 0
        


print(len(productos_link))
print(len(categoria_link_pd))

productos_pd = pd.DataFrame(columns= ['name' , 'description','price','scrap_date','supplier', 'type_of_product','sub_type_product'])

today = datetime.now(timezone('America/Buenos_Aires')).strftime("%Y-%m-%d %H:%M:%S")

for producto_link in productos_link:
    print(producto_link)
    chrome_driver.get(producto_link)
    try:
        producto_nombre = chrome_driver.find_element(By.XPATH,'.//*[contains(@class, "product_title entry-title")]').text
        #print(producto_nombre)
    except:
        print('Fallo el nombre del producto cuyo link es:')
        print(producto_link)
        producto_nombre = None
    try:
        producto_description = chrome_driver.find_element(By.XPATH,'.//*[contains(@class, "woocommerce-product-details__short-description")]').text
        #print(producto_description)
    except:
        print('Fallo la descripcion del producto cuyo link es:')
        print(producto_link)
        producto_description = None
    try:
        producto_precio = chrome_driver.find_element(By.XPATH,'.//*[contains(@class, "price")]').text
        #print(producto_precio)
    except:
        print('Fallo el precio del producto cuyo link es:')
        print(producto_link)
        producto_precio = None
    
    productos_pd = productos_pd.append({'name':producto_nombre , 'description':producto_description , 'price':producto_precio,'product_link': producto_link,'scrap_date': today ,'supplier': 'https://muebleschile.cl/', 'type_of_product': None , 'sub_type_product': None}, ignore_index=True)
    

productos_pd.to_excel('productos_excel_2.xlsx')

end = time.time()
print(end - start)
# Falta realizar el correcto formato de un pandas para gaurdar toda esta informacion
