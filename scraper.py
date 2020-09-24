
from bs4 import BeautifulSoup
from datetime import datetime
from new import New
import feedparser
import ssl
import requests
import locale
import re

# Create your views here.
def main():

    # gob() # Tiene errores

    # intendenciaValparaiso()
    # seremiSalud()
    # seremiMedioAmbiente() # Tiene errores
    # seremiCultura()
    # seremiEducacion()
    # elMatutino() # Tiene errores
    # radioValparaiso()
    # elInformador()
    # soyChileValparaiso()
    # soyChileQuillota()
    # municipalidadQuilpue()

    # municipalidadValparaiso()
    # daem()
    # municipalidadSanFelipe()
    # municipalidadQuillota()
    # upla()

def getUrl(url, ssl=True):
    try:
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        response =  requests.get(url, headers=headers, verify=ssl).text
        # El problema se debe a que falta un certificado valido, con False hace un bypass pero se requiere dejarlo en true y asignarle un certificado ssl.pem como ruta al mismo
        return( response )
    except Exception as e:
        print("=== ERROR ===")
        print(e)
        print("=== ERROR ===")
        return e

def openUrl(url, ssl=True):
    page = getUrl(url, ssl)
    bs = BeautifulSoup(page, "html.parser")
    return bs

def formatTime(time, format):
    date_format = "%Y-%m-%d %H:%M:%S"
    date_time = datetime.strptime(time, format).strftime( date_format )
    return date_time

# Noticias Ministerios
def gob():
    # Hay algo raro con obtener la pagina
    pass

def intendenciaValparaiso():
    n = New()
    n.institution = "Intendencia Valparaíso"
    n.url_base = "http://www.intendenciavalparaiso.gov.cl"
    n.url_news = n.url_base + "/noticias/"
    bs = openUrl(n.url_news)
    news = bs.find_all("div", class_="post tarjeta")
    for new in news:
        n.url_new = n.url_base + new.a["href"]
        bs_new = openUrl(n.url_new)
        
        locale.setlocale(locale.LC_ALL, 'es_CL')
        n.date = bs_new.find("span", class_="meta").text.strip()
        n.date = formatTime(n.date, "%d de %B de %Y")

        n.img = n.url_base + bs_new.find("div", class_="pic").img.get('src')
        n.title = bs_new.find("h3", class_="title").text.strip()
        n.lead = "  PORNER LA BAJADA O PRIMER PARRAFO"
        n.body_full = bs_new.find("div", class_="contenido").prettify()
        n.body = bs_new.find("div", class_="contenido").text.strip()
        n.saveNew()

# Seremis
def seremiSalud():
    n = New()
    n.institution = "Seremi de Salud"
    n.url_base = "http://seremi5.redsalud.gob.cl/"
    n.url_news = n.url_base + "?feed=rss2"
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        n.category = f['category']
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%a, %d %b %Y %H:%M:%S %z")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)
        try:
            n.img = n.url_base + bs_new.find("section", class_="body").p.a.img.get('src')
        except Exception as e:
            n.img = None
        n.body_full = bs_new.find("section", class_="body").prettify().strip()
        n.body = bs_new.find("section", class_="body").text.strip()
        n.saveNew()

def seremiMedioAmbiente():
    n = New()
    n.institution = "Seremi Medio Ambiente"
    n.url_base = "https://mma.gob.cl/category/region-de-valparaiso/"
    n.url_news = n.url_base + "feed/"
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        n.category = f['category']
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%a, %d %b %Y %H:%M:%S %z")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new, ssl=False)
        n.img = bs_new.find("div", class_="entry-thumbnail").img.get('data-src')
        n.body_full = bs_new.find("div", class_="entry-content").prettify().strip()
        n.body = bs_new.find("div", class_="entry-content").text.strip()
        n.saveNew()

def seremiCultura():
    # https://www.cultura.gob.cl/valparaiso/
    n = New()
    n.institution = "Seremi de Cultura"
    n.url_base = "https://www.cultura.gob.cl/"
    n.url_news = n.url_base + "valparaiso/noticias/"
    bs = openUrl(n.url_news)
    news = bs.find_all("div", class_="list")

    for new in news:
        locale.setlocale(locale.LC_ALL, 'es_CL')
        n.date = new.find("span", class_="list-date").text.strip()
        n.date = formatTime(n.date, "%A %d de %B de %Y")

        n.url_new = new.a["href"]
        bs_new = openUrl(n.url_new)

        n.img = bs_new.find("div", id="img-top").img.get('src')
        n.title = bs_new.find("span", class_="t2").text.strip()
        n.lead = bs_new.find("strong").text.strip()
        n.body_full = bs_new.find("div", id="cont-izq-in").prettify()
        n.body = bs_new.find("div", id="cont-izq-in").text.strip()
        n.saveNew()

def seremiEducacion():
    # https://valparaiso.mineduc.cl/
    n = New()
    n.institution = "Seremi de Educación"
    n.url_base = "https://valparaiso.mineduc.cl/"
    n.url_news = n.url_base + "feed/"
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        n.category = f['category']
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%a, %d %b %Y %H:%M:%S %z")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)
        n.img = bs_new.find("div", class_="imgDest").img.get('src')
        n.body_full = bs_new.find("div", class_="content").prettify().strip()
        n.body = bs_new.find("div", class_="content").text.strip()
        n.saveNew()

# Prensa Digital
def elMatutino():
    # http://www.elmartutino.cl/
    n = New()
    n.institution = "El Matutino"
    n.url_base = "http://www.elmartutino.cl/"
    n.url_news = n.url_base + "rss/noticias/local"
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%a, %d %b %Y %H:%M:%S %z")
        n.url_new = f['link']
        n.img = f['links'][1]['href']
        
        bs_new = openUrl(n.url_new)
        n.body_full = bs_new.find("div", class_="panel-pane pane-node-body").div.prettify().strip()
        n.body = bs_new.find("div", class_="panel-pane pane-node-body").div.text.strip()
        n.saveNew()

def radioValparaiso():
    # http://www.radiovalparaiso.cl/ciudades/valparaiso/
    n = New()
    n.institution = "Radio Valparaíso"
    n.url_base = "http://www.radiovalparaiso.cl/ciudades/valparaiso/"
    n.url_news = n.url_base + "feed/"
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        n.lead = BeautifulSoup(n.lead, "html.parser").p.text.strip()
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%a, %d %b %Y %H:%M:%S %z")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)
        n.img = bs_new.find("div", class_="featured-big-image news").img.get('src')
        n.body_full = bs_new.find("div", class_="textContent").prettify().strip()
        n.body = bs_new.find("div", class_="textContent").text.strip()
        n.saveNew()

def elInformador():
    # https://www.elinformador.cl
    n = New()
    n.institution = "El Informador"
    n.url_base = "https://www.elinformador.cl/"
    n.url_news = n.url_base + "feed/"
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        n.lead = BeautifulSoup(n.lead, "html.parser").p.text.strip()
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%a, %d %b %Y %H:%M:%S %z")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)
        n.img = bs_new.find("div", class_="td-post-featured-image").a.img.get('src')
        n.body_full = bs_new.find("div", class_="td-post-content").prettify().strip()
        n.body = bs_new.find("div", class_="td-post-content").text.strip()
        n.saveNew()

def soyChileValparaiso():
    # https://www.soychile.cl/Valparaiso/
    n = New()
    n.institution = "Soy Valparaíso - Valparaíso"
    n.url_base = "http://feeds.feedburner.com/soyvalparaisocl-todas"
    n.url_news = n.url_base + ""
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%d %b %Y %H:%M:%S:%f")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)

        try:
            n.img = bs_new.find("div", class_="gallery-item").a.img.get('src')
        except:
            n.img = bs_new.find("div", class_="gallery-item gallery-item--1").img.get('src')

        n.body_full = bs_new.find("div", class_="note-inner-text").prettify().strip()
        n.body = bs_new.find("div", class_="note-inner-text").text.strip()
        n.saveNew()

def soyChileQuillota():
    # https://www.soychile.cl/quillota/
    n = New()
    n.institution = "Soy Valparaíso - Quillota"
    n.url_base = "http://feeds.feedburner.com/soyquillotacl-todas"
    n.url_news = n.url_base + ""
    feed = feedparser.parse( n.url_news )

    for f in feed['items']:
        n.title = f['title']
        n.lead = f['summary'].replace('[&#8230;]', '')
        locale.setlocale(locale.LC_ALL, 'en_US')
        n.date = formatTime(f['published'], "%d %b %Y %H:%M:%S:%f")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)

        try:
            n.img = bs_new.find("div", class_="gallery-item").a.img.get('src')
        except:
            n.img = bs_new.find("div", class_="gallery-item gallery-item--1").img.get('src')

        n.body_full = bs_new.find("div", class_="note-inner-text").prettify().strip()
        n.body = bs_new.find("div", class_="note-inner-text").text.strip()
        n.saveNew()

# No tiene página unica
def municipalidadQuilpue():
    # https://www.quilpue.cl/
    n = New()
    n.institution = "Municipalidad Quilpue"
    n.url_base = "https://www.quilpue.cl/"
    n.url_news = n.url_base + "articulos/1/0/municipio.html"
    bs = openUrl(n.url_news)
    news = bs.find_all("a", class_="noti-c")

    for new in news:
        locale.setlocale(locale.LC_ALL, 'es_CL')
        n.date = new.find("div", class_="meta-fecha").text.strip()
        n.date = formatTime(n.date, "%d de %B, %Y")

        n.title = new['title'].strip()
        n.img = new.figure.img.get('src')
        n.lead = new.find("div", class_="txt-intro").p.text.strip()

        n.url_new = new["href"]
        bs_new = openUrl(n.url_new)
        
        n.category = bs_new.find("a", class_="noti-tag").text.strip()
        n.body_full = bs_new.find("div", id="texto").prettify()
        n.body = bs_new.find("div", id="texto").text.strip()
        n.saveNew()

def municipalidadValparaiso():
    # https://www.municipalidaddevalparaiso.cl/
    n = New()
    n.institution = "Seremi de Cultura"
    n.url_base = "https://www.municipalidaddevalparaiso.cl/"
    n.url_news = n.url_base + "HistoricoNoticias.aspx"
    bs = openUrl("https://www.municipalidaddevalparaiso.cl/HistoricoNoticias.aspx")
    news = bs.find_all("div", class_="box cargador")

    # for new in news:
        # locale.setlocale(locale.LC_ALL, 'es_CL')
        # n.date = new.find("span", class_="list-date").text.strip()
        # n.date = formatTime(n.date, "%A %d de %B de %Y")

        # n.url_new = new.a["href"]
        # bs_new = openUrl(n.url_new)

        # n.img = bs_new.find("div", id="img-top").img.get('src')
        # n.title = bs_new.find("span", class_="t2").text.strip()
        # n.lead = bs_new.find("strong").text.strip()
        # n.body_full = bs_new.find("div", id="cont-izq-in").prettify()
        # n.body = bs_new.find("div", id="cont-izq-in").text.strip()
        # n.saveNew()

def daem():
    # https://www.daem.cl/
    pass

def municipalidadSanFelipe():
    # http://www.munisanfelipe.cl/
    pass

def municipalidadQuillota():
    # https://www.quillota.cl/
    pass

# Universidades
def upla():
    # https://www.upla.cl/noticias/
    pass


if __name__ == '__main__':
    main()
