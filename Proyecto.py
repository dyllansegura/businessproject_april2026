## Proyecto Business Plan Project
# Dyllan Segura
# Version 1 - 30/05/26

# Librerias
import numpy as np
import pandas as pd
import random
from datetime import datetime

# #################### EXPLICACIÓN DEL PROYECTO:
# 3 tablas:
# - orders
# - customers
# - products
#
# + datos realistas:
# - distribuciones
# - clientes repetidos
# - precios coherentes
# - fechas reales
#
# Tabla: orders (hechos principales)
# order_id
# customer_id
# order_date
# product_id
# quantity
# unit_price
# total_amount
# payment_method
# country
# year
# month
# day_of_week
# order_size
# customer_segment
#
# Tabla: customers
# customer_id
# customer_class
# age
# gender
# signup_date
# country
#
# Tabla: products
# product_id
# product_name
# category
# subcategory
# base_price
# price_range

## Distribuciones realistas:
# Cada columna tiene su propia descripción, algunas son más detalladas.
# Categorías y subcategorías divididas por precios.
# La mayoría compra 1–2 productos, pero hay clientes que llegan a comprar hasta 8 productos (es más raro).
# Variabilidad de precios
# Pocas órdenes grandes
# Rango: 2021–2025
# Más ventas en ciertos meses (mayo y diciembre)
# Un cliente debe aparecer varias veces en orders
# Métodos de pagos distribuidos por pesos.

##### Versión 1:
## Cambiar todo por múltiples productos en una sola orden
## Cambiar distribución de clientes (edades por productos específicos, o incluso género)
## Deba de hacer el merge mucho antes
## Deba de hacer el modelado de los dataframes diferente (customers lo hice muy después, al igual que products, me centré mucho en orders)
## Se deben crear los dataframes mucho más temprano y cada vez que se crea una columna se debe ir agregando a su respectivo dataframe,
# de esta manera, la creación de cada una de las siguientes columnas es mucho más fácil y no se batalla tanto con el código.
## El código se va haciendo cada vez más ameno, más legible, más corto y menos complicado mientras se va trabajando con Pandas.
## Realizar debug del código
## Siguen habiendo muchas columnas que deben ser arregladas
## El código puede ser más eficiente

########### Primera parte del código - Creación de datos
###### Serán 15000 datos
number_of_orders = 15000  # Cambiar por 15000 al final, 20 para funcionalidad, 1000 para distribución
random.seed(18)  # Semilla del proyecto, para que sea reproducible

##### customer_id (customers)
number_of_customers = int(number_of_orders * 0.4)  # 0.4 es lo más balanceado, los clientes se repiten lo suficiente en orders y no son tan pocos

customer_id = list()
for each_customer in range(1, number_of_customers + 1):
    customer_id.append(f"cust_{each_customer:04d}")

##### customer_id (orders), customer_class (customers)

all_customer_weight = list()
customer_class = list()
for each_customer_id_customers in customer_id:

    customer_probability = random.random()

    if customer_probability < 0.70:
        each_class = "Normal"
        each_customer_weight = random.randint(1, 2)
    elif customer_probability < 0.95:
        each_class = "Popular"
        each_customer_weight = random.randint(3, 5)
    else:
        each_class = "VIP"
        each_customer_weight = random.randint(6, 8)

    all_customer_weight.append(each_customer_weight)
    customer_class.append(each_class)

customer_id_orders = random.choices(customer_id, weights=all_customer_weight, k=number_of_orders)

##### orders_id (orders)
# Esta columna no importa si se genera de manera independiente

orders_id = []
for orders in range(1, number_of_orders + 1):
    orders_id.append(f"ord_{orders:05d}")

#####  order_date (orders)
extra_data = round(number_of_orders * 1.5)  # Se usará más adelante

# Rango de datos: 2021-2025.
# Más ventas en ciertos meses (mayo y diciembre).
# Fines de semana más ventas.
# Más ventas a lo largo del tiempo.
# Menos ventas al inicio.
# El dato final debe terminar como yyyy-mm-dd por facilidad de MySQL y PBI.

dates = [
    tuple(str(year) for year in range(2021, 2026)),
    tuple(f"{month:02d}" for month in range(1, 13))
]

dates_weights = [
    (8, 12, 5, 17, 28),  # Los pesos para cada año van aumentando con el tiempo, caída en 2023, 2025 dominando
    (7, 7, 7, 7, 15, 7, 7, 7, 7, 7, 7, 15)  # 7% weight para los demás meses y 15% para mayo y diciembre
]

date_time = []
time = []
for dates_given, new_weights in zip(dates, dates_weights):  # Se separan año y mes, pero se juntan en una lista
    time += [random.choices(dates_given, weights=new_weights, k=extra_data)]

for timing in time:
    for index in range(extra_data):

        if len(date_time) == extra_data:
            date_time[index] += timing[index]
        else:
            date_time.append(timing[index])

order_date = [dates_not_completed[:4] + "-" + dates_not_completed[4:] + "-" for dates_not_completed in date_time]

day_of_week = random.choices([f"{each_day:02d}" for each_day in range(1, 32)], k=extra_data)

i = 0  # Contador
for day in day_of_week:
    if int(day) > 29 and int(order_date[i][:4]) % 4 == 0 and int(order_date[i][5:7]) == 2:  # Febrero en año bisiesto
        day = "29"
    elif int(day) > 28 and int(order_date[i][5:7]) == 2:  # Febrero en año no bisiesto
        day = "28"
    elif int(day) > 30 and int(order_date[i][5:7]) in (4, 6, 9, 11):  # Meses que no tienen 31 días
        day = "30"

    day_of_week[i] = day
    i += 1

i = 0  # Reiniciar contador
for not_completed_date, uncompleted_days in zip(order_date, day_of_week):  # Crear fechas aleatorias sin pesos en fines de semana + convertirlo a datetime
    order_date[i] = datetime.strptime(not_completed_date + uncompleted_days, "%Y-%m-%d")  # string parse time
    i += 1

# Pesos: (sábado 25%, domingo 20%, viernes: 15%, lunes a jueves: 10%)
# Técnica: Eliminar fechas que tengan menores pesos para simular esos pesos
# y para el caso del fin de semana no se eliminarán las fechas. Para el viernes se eliminarán menos fechas.

i = 0  # Reiniciar contador
final_order_date = []  # order_date final
for every_day in order_date:
    if (every_day.weekday() in (0, 1, 2, 3) and random.random() <= (1 / 4)) or (every_day.weekday() == 4 and random.random() <= (1 / 6)):  # Eliminar de vez en cuando Lu-Ju (25%) y Vi (16%)
        continue

    i += 1
    final_order_date.append(every_day)

del final_order_date[number_of_orders:]  # Eliminar exceso de elementos

##### product_name (products)
# Nombre único de cada uno de los productos
product_name = ["Samsung Galaxy S23 Ultra 5G", "Samsung 5G 6.7\"", "Redmi Note 11S 5G", "Samsung 50\" TV Crystal UHD",
                "Samsung Smart TV 40\" Full HD", "Smart TV Roku Aiwa",
                "Ninja Chef CT800 Blender", "Oster Blender", "T-Fal Power Mix Blender", "Apple Airpods 4",
                "Sony WH-CH720N Wireless Headphones", "Xiaomi Redmi Buds 6 Play Headphones",
                "Suevery 34\" Gamer Monitor", "Xiaomi A27i 2026 Monitor", "Xiaomi Monitor A24i", "Lora Jacket",
                "Vector Ski & Snowboard Jacket", "Columbia Glenbrook Bend Rain Jacket",
                "Dlo 1 \"Dossier\" Way of Wade Tennis", "DC Shoes", "Bruno Marc Shoes", "Zara Jeans Relaxed Barrel Fit",
                "Slim Straight Jeans", "Blue Jeans Fit Wide Leg",
                "Hoodie Stwd", "Boxy Hoodie", "Black Hoodie Essentials", "Classic Champion T-Shirt",
                "Stradivarius Short Sleeve", "Hang Ten T-Shirt",
                "Stuhrling Legacy Watch", "Seiko Essentials Watch", "9 Apple Watch", "Under Armour Triumph Backpack",
                "Cool Capital Backpack", "Lovevook Backpack",
                "Nano Anker Instacharger", "Apple USB-C Charger", "Xd Fast Charger 120W", "iPhone 17 Case",
                "General Phone Case", "Drop-proof Case",
                "Jonathan Y Ellis 295 Lamp", "Living Room Lamp RGB", "BLASVERK Lamp", "Alissa Capuccino Chairs",
                "White Office Ecochair", "White Folding Chair",
                "Ceramics Thyme & Table Dish Set", "Gibson Elite Dish Set", "Opal Glass Mainstays Dish Set",
                "SEDLIG Flatware 20-piece Set",
                "Verona Collection 20-piece Set", "ZLYSYCM 60-piece Silverware Set", "Brandtrendy Kit 6 Dumbbells in 1",
                "Corength Hexagonal Dumbbells 7.5kg",
                "SONGMICS Set of 2 Hexagonal Dumbbells", "Outdoor T-shirt Sportswear", "Nike Sportswear T-shirt",
                "H&M Deportive Leggings with SoftMove",
                "Adidas Mats 10mm", "Yoga Mat 10mm Athletic Works", "Pilates or Yoga Mats Non-Slip",
                "Hikeo Water Thermo 2L", "Hartplas Thermo Sport 32oz",
                "HydraPak Water Bottle 1.5L", "Rabanne Fame Perfume", "Eau de Parfum Carolina Herrera 80mL Perfume",
                "Coach Dreams Moonlight Perfume",
                "Kiehl's Dark Spot Solution", "Vacay All Day Skincare", "Centella de Madagascar Skincare",
                "Maybelline Lumi-matte Foundation", "NYX Bronzer Buttermelt",
                "Born This Way Eyeshadow Palette Natural Nudes", "Sephora Haircare Besties Kit", "Ava Hair Moisturizer",
                "Skala Watermelon Treatment for Hair",
                "A Thousand Wishes Body Lotion", "Eos Shea Better Vanilla Body Lotion", "Dove Corporal Serum"]

##### product_id (products)
# En la tabla products se van a identificar todos los products, a diferencia de la tabla orders, ahí no aparecerán todos los productos y además
# habrá productos duplicados, entonces esta columna puede ser generada de manera independiente

product_id = []
for products in range(1, len(product_name) + 1):
    product_id.append("prod_" + f"{products:02d}")

##### base_price (products)
# Precio base del producto (diferente a unit_price que varía el precio por inflación o promociones, etc.)
# Hacer a la par que product_name

base_price = [9750, 5499.99, 2499.99, 5455.55, 4150, 2500, 3980, 700, 600, 2985.55, 1990, 200, 4900, 2495.33, 1700,
              6400, 3100, 2499.99, 2250, 1899.99, 1350,
              1099.99, 780, 350, 850, 699.99, 450, 450, 250, 230, 6499.99, 6450, 4999.99, 1499.99, 1011, 719, 999.99,
              549, 299, 1399.99, 349.45, 214.22,
              3177.85, 761.66, 399.99, 1731, 1397, 449.99, 1199.99, 999.99, 549.45, 999.99, 959.20, 817.77, 979.99,
              699.99, 299.99, 1849.99, 999, 599.99,
              959.20, 299.99, 280, 378, 349.85, 299.99, 3805, 3690, 2490, 1500, 1465.55, 859.99, 254, 345.55, 1329,
              1020.20, 1430.77, 201, 429, 255.55, 200.51]

##### category (products)
# Categorías: Electronics (caro), Clothing, Sports, Beauty, Home (medio), Accessories (barato)
categories_repetitions = {"Electronics": 15, "Clothing": 15, "Accessories": 12, "Home": 12, "Sports": 12,
                          "Beauty": 15}  # Si después se quieren cambiar las repeticiones
category = []
for categories, repetitions in categories_repetitions.items():
    category += [*((categories + " ") * repetitions).split()]

##### subcategory (products)
# Electronics es lo más caro, las demás categorías van de medio a barato, pero se quedan en medio todas, la más barata es accessories (tiene 2 artículos baratos)
# Electronics: (Smartphone muy alto, TV alto, blender, headphones, monitor medio), Clothing (Jackets alto, shoes, jeans, hoodie medio, T-shirt bajo),
# Accessories: (Watches alto, backpacks medio, chargers, phone cases bajo), Home: (Lamps, chairs medio, dish set, flatware set bajo),
# Sports: (Dumbbells, sportswear medio, yoga mats, water bottles bajo), Beauty (Perfume alto, skincare, makeup, haircare medio, body lotion bajo)
# El código de subcategory es muy parecido a category. En este caso no se realizó el diccionario con las repeticiones de cada subcategoría porque
# sabemos que cada subcategoría se repite 3 veces siempre y en caso de que eso cambie, se tendría que modificar toda la tabla products completa,
# no solamente esta sección, así que damos por obvio esta parte. En caso de ocupar cambiarlo, se hará un diccionario como en categories.

subcategories_wo_repetition = ["Smartphone", "TV", "Blender", "Headphones", "Monitor", "Jacket", "Shoes", "Jeans",
                               "Hoodie", "T-shirt", "Watch",
                               "Backpack", "Charger", "Phone Case", "Lamp", "Chair", "Dish Set", "Flatware Set",
                               "Dumbbells", "Sportswear",
                               "Yoga Mat", "Water Thermo", "Perfume", "Skincare", "Makeup", "Haircare", "Body Lotion"]

subcategory = []
for sub in subcategories_wo_repetition:
    subcategory += [sub] * 3

##### price_range (products)
# Para terminar la tabla products
# Viendo los precios de base_price:
# Low / Medium / High
# Very High >= 5000, 2000 <= High < 5000, 1000 <= Medium < 2000, Low < 1000
# Tomando en cuenta estos rangos, los que había puesto anteriormente solamente eran de borrador, pero estos ya son los oficiales.

price_range = list()
price_threshold = {"Low": 1000, "Medium": 2000, "High": 5000}
label = ""  # Se tiene que definir
for price_compared in base_price:

    for every_key, every_value in price_threshold.items():

        if price_compared > every_value and every_key == "High":
            label = "Very High"
        elif price_compared > every_value:
            continue
        else:
            label = every_key
            break

    price_range.append(label)

##### product_id (orders)
# products multiplicados varias veces
# Procedimiento:
# Pesos: Very High 1, High 3, Medium 6, Low 9
# Se encuentran los pesos para después ponerlo en choices junto con product_id (products)

each_weight_product_range = list()
price_range_weight = {"Very High": 1, "High": 3, "Medium": 6, "Low": 9}

for each_price_range in price_range:
    each_weight_product_range.append(price_range_weight[each_price_range])

product_id_orders = random.choices(product_id, weights=each_weight_product_range, k=number_of_orders)

##### quantity (orders)
# Cantidad de veces que compran un producto
# product_id_orders (orders) -> quantity (orders)
# Saber qué price_range tiene el product_id de orders y así generar quantity
# 1 si High o Very High, 2-3 Medium, 3-4 Low

price_related_variations = {"Very High": 0, "High": 0, "Medium": 1,
                            "Low": 2}  # Para agrupar los 3 grupos de productos. Very High y High se agrupan constantemente.

whole_product = dict()
##### Relación fuerte entre tablas
for each_product_id, each_price_range in zip(product_id, price_range):
    whole_product[each_product_id] = each_price_range

quantity = list()
for each_product_id_orders in product_id_orders:

    if price_related_variations[whole_product[
        each_product_id_orders]] == 0:  # Entre cada id de producto, busca su rango y además clasifícalo por grupo, aquí High/Very High
        number_multiplier = 1
    elif price_related_variations[whole_product[each_product_id_orders]] == 1:  # Medium
        number_multiplier = random.randint(2, 3)
    else:
        number_multiplier = random.randint(3, 4)  # Low

    quantity.append(number_multiplier)

########### Segunda parte del código - Manipulación de datos a partir de los creados
##### Creación de dataframes 1 - orders_df y products_df
orders = {"customer_id": customer_id_orders, "orders_id": orders_id, "order_date": final_order_date,
          "product_id": product_id_orders, "quantity": quantity}
orders_df = pd.DataFrame(orders, columns=["customer_id", "orders_id", "order_date", "product_id", "quantity"])

products = {"product_id": product_id, "product_name": product_name, "base_price": base_price, "category": category,
            "subcategory": subcategory, "price_range": price_range}
products_df = pd.DataFrame(products, columns=["product_id", "product_name", "base_price", "category", "subcategory",
                                              "price_range"])

##### unit_price (orders)
# Las variaciones están separadas y bien explicadas por el diccionario new_variations_combinations. Además, también se separan por el price_range.

# Refinar esto después para que esta variación solo aplique para productos caros y muy caros.

orders_merged_products = orders_df.merge(
    products_df[["product_id", "base_price", "price_range", "category"]],
    on="product_id",
    how="left"
)

price_endings = [.99, .90, .80, .95, .55, .33, .59, .66]

new_variations_combinations = {
    ("Very High", "high_season"):(-0.25, 0.25),
    ("High", "high_season"):(-0.25, 0.25),
    ("Medium", "high_season"):(-0.20, 0.20),
    ("Low", "high_season"):(-0.15, 0.15),
    ("Very High", "low_season"):(-0.15, 0.15),
    ("High", "low_season"):(-0.15, 0.15),
    ("Medium", "low_season"):(-0.10, 0.10),
    ("Low", "low_season"):(-0.05, 0.05),
}

orders_merged_products["season"] = np.where(
    orders_merged_products["order_date"].dt.month.isin([5,12]), # Filtrar por temporada alta o baja
    "high_season",
    "low_season"
)

orders_merged_products["key"] = list(zip(orders_merged_products["price_range"], orders_merged_products["season"]))
orders_merged_products["range_of_variation"] = orders_merged_products["key"].map(new_variations_combinations)
orders_merged_products["variation"] = orders_merged_products["range_of_variation"].apply(
    lambda x: (1 + random.uniform(*x))
)
orders_merged_products["unit_price"] = np.trunc(orders_merged_products["base_price"] * orders_merged_products["variation"]) # Truncar precio para hacer lo siguiente
orders_df["unit_price"] = orders_merged_products["unit_price"].apply( # Agregar a orders_df
    lambda x: x + price_endings[random.randint(0, 7)] # Agregar una terminación de un precio real
)

##### total_amount (orders)
# Cantidad total (total amount = unit_price * quantity)

orders_df["total_amount"] = np.trunc(orders_df["unit_price"] * orders_df["quantity"])
orders_df["total_amount"] = orders_df["total_amount"].apply(
    lambda x: x + price_endings[random.randint(0, 7)] # Agregar una terminación de un precio real
)
orders_merged_products["total_amount"] = orders_df["total_amount"] # Para uso posterior

##### payment_method (orders)
# Compras grandes (Credit Card 55%, Bank Transfer 25%, PayPal 20%)
# Compras no grandes:
# -Productos caros (Credit Card 50%, PayPal 25%, Digital Wallet 15%, Cash 5%, Bank Transfer 5%)
# -Productos medios (Debit Card 35%, Credit Card 30%, Digital Wallet 20%, PayPal 15%)
# -Productos baratos (Cash 45%, Debit Card 30%, Digital Wallet 25%)

# Categorías: Electronics "Clothing": "Accessories":, "Home": , "Sports": "Beauty":
# Compra grande depende de la categoría y se considera cuando:
# Electrónica > 5000
# Clothing > 2000
# Accessories > 1200
# Home > 2500
# Sports > 2000
# Beauty > 1200

# Grupo 0: Compras grandes
# Grupo 1: Compras no grandes

category_threshold = {"Electronics": 5000, "Clothing": 2000, "Accessories": 1000, "Home": 6000, "Sports": 3000,
                      "Beauty": 1500}
order_big_not = {("Big", "No Matter"): [("Credit Card", 55), ("Bank Transfer", 25), ("PayPal", 20)],
                 ("Low", "Very High"): [("Credit Card", 50), ("PayPal", 25), ("Digital Wallet", 15), ("Cash", 5), ("Bank Transfer", 5)],
                 ("Low", "High"): [("Credit Card", 50), ("PayPal", 25), ("Digital Wallet", 15), ("Cash", 5), ("Bank Transfer", 5)],
                 ("Low", "Medium"): [("Debit Card", 35), ("Credit Card", 30), ("Digital Wallet", 20), ("PayPal", 15)],
                 ("Low", "Low"): [("Cash", 45), ("Debit Card", 30), ("Digital Wallet", 25)]} # Grupos y pesos de métodos de pago

compare_columns = orders_merged_products.groupby(["customer_id", "category"])["total_amount"].transform("sum")
orders_merged_products["category_threshold"] = np.where(
    compare_columns >= orders_merged_products["category"].map(category_threshold), # Separar por Big y Low
    "Big",
    "Low"
)

orders_merged_products["none_or_range"] = np.where(
    orders_merged_products["category_threshold"] == "Big", # Hacer que todos los Big no importen qué range tengan
    "No Matter",
    orders_merged_products["price_range"]
)

orders_merged_products["pair_dict"] = list(zip(orders_merged_products["category_threshold"], orders_merged_products["none_or_range"]))

def choose_payment_method(buy_and_range): # Cada método de pago
    methods_and_weights = order_big_not[buy_and_range]
    pay_method, pay_weight = zip(*methods_and_weights)
    return random.choices(pay_method, weights=pay_weight, k=1)[0]

orders_merged_products["payment_method"] = orders_merged_products["pair_dict"].apply(
    lambda x: choose_payment_method(x)
)

orders_df["payment_method"] = orders_merged_products["payment_method"]  # Agregado a orders_df

##### country (customers)
# Clientes en customers. Cada cliente relacionado con un solo país.
# Paises con probabilidades de aparición por cliente:
# (Mexico 35%, USA 20%, Canada 10%, Spain 10%, France 5%, Germany 10%, Brazil 10%)

countries_and_weights = [("Mexico", 35), ("USA", 20), ("Canada", 10), ("Spain", 10), ("France", 5), ("Germany", 10),
                         ("Brazil", 10)]
countries, weights_of_countries = zip(*countries_and_weights)
country = random.choices(countries, weights=weights_of_countries, k=number_of_customers)

##### year (orders), month (orders), day_of_week (orders)
orders_df["year"] = orders_df["order_date"].dt.year
orders_df["month"] = orders_df["order_date"].dt.month
orders_df["day"] = orders_df["order_date"].dt.day

##### order_size (orders)
# Small / Medium / Large
# Se establecieron anteriormente los threshold.
# < 0.5 es Small
# Entre 0.5 y 1 del threshold es Medium
# Mayor o igual a 1 del threshold es Large
# Todo respectivo a su categoría

orders_df["order_size"] = np.select(
    [ # Condiciones if
        orders_merged_products["total_amount"] < (orders_merged_products["category"].map(category_threshold))*0.5,
        orders_merged_products["total_amount"] < (orders_merged_products["category"].map(category_threshold))
    ],
    [ # Resultado
        "Small",
        "Medium"
    ], # Else
        default="Large"
)

##### Creación de dataframes 2 - customers_df
customers = {"customer_id": customer_id, "customer_class": customer_class, "country": country}
customers_df = pd.DataFrame(customers, columns=["customer_id", "customer_class", "country"])

##### gender (customers)
# Male, Female, Other. Other tiene menor peso que Male y Female porque es mucho menos común.

gender_options = ["M", "F", "Other"]
gender_weights = [47.5, 47.5, 5]
gender = random.choices(gender_options, weights=gender_weights, k=number_of_customers)

customers_df["gender"] = gender  # Agregado a customers_df

##### age (customers)
# Los pesos son los siguientes:
# 18-25: 25%
# 26-35: 35%
# 36-50: 25%
# 51-65: 10%
# 66+: 5%

age_threshold = {0.25: (18, 25), 0.6: (26, 35), 0.85: (36, 50), 0.95: (51, 65)}
age = list()
age_label = None
for every_customer_id in customer_id:

    age_random_num = random.random()

    for age_keys, age_values in age_threshold.items():

        if age_random_num < age_keys:
            age_label = random.randint(*age_values)  # Todos los casos anteriores
            break
        elif age_random_num > 0.95:
            age_label = random.randint(66, 75)  # 66+
        else:
            continue

    age.append(age_label)

customers_df["age"] = age  # Agregado a customers_df

##### signup_date (customers)
# La fecha signup_date debe ser anterior a la fecha orders_date. La fecha de ingreso del cliente debe ser antes que la de su primera orden.
# Los clientes se registran esta cantidad de días antes dependiendo de qué tipo de clientes son:
# VIP: 300 a 1000 días antes de su primera compra
# Popular: 100 a 700 dias antes de su primera compra
# Normal: 1 a 300 dias antes de su primera compra

# Merge orders y customers
orders_df_merged_customers = orders_df.merge(
    customers_df[["customer_id", "customer_class", "country"]],
    on="customer_id",
    how="left"
)

cust_class_dates = orders_df_merged_customers.groupby(["customer_id", "customer_class"])["order_date"].min().to_dict()
signup_threshold = {"VIP": (300, 1000), "Popular": (100, 700), "Normal": (1, 300)}
signup_date = list()

for each_key, each_date_of_customer in cust_class_dates.items():
    each_customer, each_customer_class = each_key
    days_before = random.randint(*signup_threshold[each_customer_class])
    signup_date.append(each_date_of_customer - pd.to_timedelta(days_before, unit="D"))

##### country (orders)
# Se extraen datos del order_df_merged para saber cuáles son las nacionalidades de cada customer.
# Se adjuntan al df original.

country_map = orders_df_merged_customers.drop_duplicates("customer_id").set_index("customer_id")["country"] # Cada indice no duplicado a cada cliente y por tanto a cada pais
orders_df["country"] = orders_df["customer_id"].map(country_map)

##### customer_segment (orders)
# Clasificados por:
# Low Spender / Medium Spender / High Spender.
# High Spender es el top 33% de los clientes con mayores gastos
# Medium Spender son los que le siguen top 66% gastos (Percentil 66)
# Low Spender son los clientes que quedan (Percentil 33)

orders_merged_products["total_sum_of_buy"] = orders_df.groupby("customer_id")["total_amount"].transform("sum")
o33_percentile = orders_merged_products["total_sum_of_buy"].quantile(1/3) # Cuartil 33
o66_percentile = orders_merged_products["total_sum_of_buy"].quantile(2/3) # Cuartil 66
orders_merged_products_sorted = orders_merged_products.sort_values(["customer_id", "order_date"]) # custom_id, order_date sorted de compra más vieja a actual
orders_merged_products_sorted["accumulated_total_amount"] = orders_merged_products_sorted.groupby("customer_id")["total_amount"].cumsum() # Suma acumulada de cada cliente
orders_merged_products_sorted["customer_segment"] = np.select( # Filtrar cuartiles y asignar spender
    [
        orders_merged_products_sorted["accumulated_total_amount"] < o33_percentile,
        orders_merged_products_sorted["accumulated_total_amount"] < o66_percentile
    ],
    [
        "Low Spender",
        "Medium Spender"
    ],
    default="High Spender"
)

orders_df["customer_segment"] = orders_merged_products_sorted["customer_segment"] # Agregado a orders_df

# Parte 2 order_date (orders)
rand_hour = np.random.randint(8,20, size=number_of_orders)
rand_min = np.random.randint(0,59, size=number_of_orders)
rand_sec = np.random.randint(0,59, size=number_of_orders)

hours_min_sec = pd.to_timedelta(rand_hour, unit="h") + pd.to_timedelta(rand_min, unit="m") + pd.to_timedelta(rand_sec, unit="s")
orders_df["order_date"] = orders_df["order_date"] + hours_min_sec

########### Tercera parte del código - Exportación de datos
with pd.ExcelWriter("business_plan_project.xlsx") as writer:
     orders_df.to_excel(writer, sheet_name="orders")
     products_df.to_excel(writer, sheet_name="products")
     customers_df.to_excel(writer, sheet_name="customers")