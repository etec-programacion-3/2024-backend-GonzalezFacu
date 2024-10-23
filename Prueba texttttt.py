from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import random
import time

def obtener_productos_hello_fresh():
    options = Options()
    options.headless = True  # Opcional: ejecuta en segundo plano
    service = Service('ruta/al/chromedriver')  # Cambia esto a la ubicación de tu ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)

    url = 'https://www.hellofresh.com/recipes'
    driver.get(url)
    time.sleep(5)  # Espera que la página cargue

    productos = driver.find_elements(By.CLASS_NAME, 'some-product-class')  # Ajusta según el HTML real

    lista_productos = []
    for producto in productos[:25]:  # Limita a 25 productos
        nombre = producto.find_element(By.TAG_NAME, 'h2').text.strip()  # Ajusta según la etiqueta real
        descripcion = producto.find_element(By.TAG_NAME, 'p').text.strip()  # Ajusta según la etiqueta real
        precio = random.randint(15000, 45000) // 100 * 100  # Precio redondeado
        imagen = producto.find_element(By.TAG_NAME, 'img').get_attribute('src')  # Ajusta según la etiqueta real

        lista_productos.append({
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'imagen': imagen
        })

    driver.quit()
    return lista_productos

# Ejecutar la función y mostrar los productos
productos = obtener_productos_hello_fresh()
for producto in productos:
    print(producto)
