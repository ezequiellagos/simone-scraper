import mysql.connector
from mysql.connector import Error
from datetime import datetime

class New:
    def __init__(self):
        self._institution = None
        self._url_base = None
        self._url_news = None
        self._title = None
        self._lead = ""
        self._category = 'sin categoría'
        self._url_new = None
        self._date = None
        self._img = None
        self._body = ""
        self._body_full = ""

    def saveNew(self):
        try:
            connection = mysql.connector.connect(host='localhost', database='simone', user='root', password='')
            cursor = connection.cursor(buffered=True)

            # Check if exist the record
            mysql_check_query = """SELECT title, COUNT(*) FROM wp_scraper WHERE title = %s AND institution = %s GROUP BY title"""
            record = (self._title, self._institution)
            cursor.execute(mysql_check_query, record)
            row_count = cursor.rowcount

            if row_count == 0:
                mysql_insert_query = """INSERT INTO wp_scraper 
                                        (institution, url_base, url_news, url_new, title, lead, category, date, img, body, body_full) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
                recordTuple = (self._institution, self._url_base, self._url_news, self._url_new, self._title, self._lead, self._category, self._date, self._img, self._body, self._body_full)
                cursor.execute(mysql_insert_query, recordTuple)
                connection.commit()

        except mysql.connector.Error as error:
            print("Failed to insert: {}".format(error))

        finally:
            if ( connection.is_connected() ):
                cursor.close()
                connection.close()
        
        # print("institution")
        # print( self._institution)
        # print("url_base")
        # print( self._url_base)
        # print("url_news")
        # print( self._url_news)
        # print("title")
        # print( self._title)
        # print("lead")
        # print( self._lead)
        # print("category")
        # print( self._category)
        # print("url_new")
        print( self._url_new)
        # print("date")
        # print( self._date)
        # print("img")
        # print( self._img)
        # print("body")
        # print( self._body)
        # print("body_full")
        # print( self._body_full)
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
   