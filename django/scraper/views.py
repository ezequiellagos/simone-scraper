#Eliminar
from django.shortcuts import render

from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
import urllib.request
import locale

response = []

class New:

    def __init__(self):
        self._institution = None
        self._url_base = None
        self._url_news = None
        self._title = None
        self._lead = None
        self._category = None
        self._url_new = None
        self._date = None
        self._img = None
        self._body = None
        self._body_full = None

    def saveNew(self):
        
        print("institution")
        print( self._institution)
        print("url_base")
        print( self._url_base)
        print("url_news")
        print( self._url_news)
        print("title")
        print( self._title)
        print("lead")
        print( self._lead)
        print("category")
        print( self._category)
        print("url_new")
        print( self._url_new)
        print("date")
        print( self._date)
        print("img")
        print( self._img)
        print("body")
        print( self._body)
        print("body_full")
        print( self._body_full)
        print("=================================")

    @property
    def institution(self):
        return self._institution

    @institution.setter
    def institution(self, value):
        self._institution = value

    @institution.deleter
    def institution(self):
        del self._institution

    @property
    def url_base(self):
        return self._url_base

    @url_base.setter
    def url_base(self, value):
        self._url_base = value

    @url_base.deleter
    def url_base(self):
        del self._url_base

    @property
    def url_news(self):
        return self._url_news

    @url_news.setter
    def url_news(self, value):
        self._url_news = value

    @url_news.deleter
    def url_news(self):
        del self._url_news

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @title.deleter
    def title(self):
        del self._title

    @property
    def lead(self):
        return self._lead

    @lead.setter
    def lead(self, value):
        self._lead = value

    @lead.deleter
    def lead(self):
        del self._lead

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @category.deleter
    def category(self):
        del self._category

    @property
    def url_new(self):
        return self._url_new

    @url_new.setter
    def url_new(self, value):
        self._url_new = value

    @url_new.deleter
    def url_new(self):
        del self._url_new

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @date.deleter
    def date(self):
        del self._date

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        self._img = value

    @img.deleter
    def img(self):
        del self._img
    
    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value

    @body.deleter
    def body(self):
        del self._body

    @property
    def body_full(self):
        return self._body_full

    @body_full.setter
    def body_full(self, value):
        self._body_full = value

    @body_full.deleter
    def body_full(self):
        del self._body_full
    

# Create your views here.
def home(request):
    # news = "a"s
    print(response)

    # Configuración 
    # locale.setlocale(locale.LC_ALL, 'es_CL')

    # intendenciaValparaiso()
    # seremiSalud()
    gob()

    return render(request, "scraper/home.html", {'response':response})

def getUrl(url):
    try:
        with urllib.request.urlopen(url) as response:
            return(response.read())
    except Exception as e:
        return e
        # print("=== ERROR ===")
        # print(e)
        # print("=== ERROR ===")


def openUrl(url):
    page = getUrl(url)
    bs = BeautifulSoup(page, "html.parser")
    return bs

# Noticias Ministerios
def gob():
    # Hay algo raro con obtener la pagina
    pass

def intendenciaValparaiso():
    n = New()
    n.institution = "Intendencia Valparaíso"
    n.url_base = "http://www.intendenciavalparaiso.gov.cl"
    n.url_news = n.url_base + "/noticias/"
    bs = openUrl(n.url_base)
    news = bs.find_all("div", class_="post tarjeta")
    for new in news:
        n.url_new = n.url_base + new.a["href"]
        bs_new = openUrl(n.url_new)
        
        locale.setlocale(locale.LC_ALL, 'es_CL')
        n.date = bs_new.find("span", class_="meta").text.strip()
        n.date = datetime.strptime(n.date, '%d de %B de %Y').date().strftime("%d-%m-%Y")

        n.img = n.url_base + bs_new.find("div", class_="pic").img.get('src')
        n.title = bs_new.find("h3", class_="title").text.strip()
        n.lead = "  PORNER LA BAJADA O PRIMER PARRAFO"
        n.body_full = bs_new.find("div", class_="contenido")
        n.body = bs_new.find("div", class_="contenido").text
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
        n.date = datetime.strptime(f['published'], '%a, %d %b %Y %H:%M:%S %z').date().strftime("%d-%m-%Y")
        n.url_new = f['link']
        
        bs_new = openUrl(n.url_new)
        n.img = n.url_base + bs_new.find("section", class_="body").p.a.img.get('src')
        n.body_full = bs_new.find("section", class_="body")
        n.body = bs_new.find("section", class_="body").text
        n.saveNew()    

def seremiMedioAmbiente():
    pass

def seremiCultura():
    pass

def seremiEducacion():
    pass

# Prensa Digital
def elMatutino():
    pass

def radioValparaiso():
    pass

def elInformador():
    pass

def soyChileValparaiso():
    pass

def soyChileQuillota():
    pass

def municipalidadQuilpue():
    pass

def municipalidadValparaiso():
    pass

def daem():
    pass

def municipalidadSanFelipe():
    pass

def municipalidadQuillota():
    pass

# Universidades
def upla():
    pass