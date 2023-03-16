import pandas as pd

data = pd.read_excel('productos_excel_2.xlsx',engine='openpyxl')

#print(data['product_link'])
data['product_link'] = data['product_link'].replace(to_replace='https://muebleschile.cl/shop/', value='', regex=True)

type_and_subtypes_products = data['product_link'].str.split("/",n = 3 ,expand=True)

print(type_and_subtypes_products[0])

data['type_of_product'] = type_and_subtypes_products[0]

data['sub_type_product'] = type_and_subtypes_products[1]


print(data['type_of_product'] )

print(data['sub_type_product'])

data.to_excel('productos_excel_clean.xlsx')

#print(data['type_of_product'])