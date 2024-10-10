# utils.py
import requests
from bs4 import BeautifulSoup
from flask import url_for
from urllib.parse import urljoin

def extraer_informacion_enlace(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer título
        titulo = ""
        # Buscamos en og:title, name="og:title" o simplemente el <title>
        meta_og_title = soup.find('meta', property='og:title') or soup.find('meta', attrs={'name': 'og:title'})
        if meta_og_title:
            titulo = meta_og_title.get('content', '')
        else:
            titulo = soup.title.string if soup.title else "Sin título"

        # Extraer descripción
        descripcion = ""
        # Buscamos en og:description, name="og:description" o description
        meta_og_description = soup.find('meta', property='og:description') or soup.find('meta', attrs={'name': 'og:description'})
        if meta_og_description:
            descripcion = meta_og_description.get('content', '')
        else:
            meta_description = soup.find('meta', attrs={'name': 'description'})
            descripcion = meta_description.get('content', '') if meta_description else "Descripción no disponible"

        # Extraer imagen y asegurar que sea una URL absoluta
        imagen = ""
        meta_og_image = soup.find('meta', property='og:image') or soup.find('meta', attrs={'name': 'og:image'})
        if meta_og_image:
            imagen = meta_og_image.get('content', '')
            # Si la URL de la imagen es relativa, la convertimos en absoluta
            imagen = urljoin(url, imagen)  # Asegurarse de que la URL de la imagen sea absoluta
        else:
            imagen = url_for('static', filename='images/default_img.png')

        return titulo, descripcion, imagen

    except requests.exceptions.RequestException as e:
        print(f"Error al procesar el enlace: {e}")
        return "Error al extraer datos", "Descripción no disponible", url_for('static', filename='images/default_img.png')
