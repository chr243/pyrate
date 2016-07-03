import urllib2
from bs4 import BeautifulSoup
import android

droid = android.Android()
isbn = '9788375067293'

def skanuj():
    '''Korzystajac z androidowego modulu skanuje kod kreskowy i zwraca numer
    isbn'''
    kodkreskowy = droid.scanBarcode()
    isbn = int(kodkreskowy['result']['SCAN_RESULT'])
    return isbn

def szukajnagooglu(tytul):
    '''Pyta googla o ksiazke na chomikuj.pi zwraca do niej url'''
    headers = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request('https://www.google.pl/search?q=chomikuj+' + tytul.encode('utf-8') + '+pdf&ie=&oe=', None, headers)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')
    chomik = soup.find_all('a')
    link = str(chomik[35])
    a = link.split('=')
    link = a[2]
    return link

def znajdz_tytul(isbn):
    '''Bierze podany numer isbn i na jego podstawie szuka ksiazki w bazie
    biblioteki narodowej, nastepnie wydobywa z html'a tytul i nazwisko autora'''
    html = urllib2.urlopen('http://alpha.bn.org.pl/search~S5*pol/?searchtype=i&searcharg=' + isbn + '&searchscope=5&SORT=D&extended=0&SUBMIT=Szukaj&searchlimits=&searchorigarg=t' + isbn)
    soup = BeautifulSoup(html, 'lxml')
    calosc = soup.find('strong').contents[0]
    tytul = calosc.split(';')[0].replace('/','')
    return tytul.replace(' ','+').replace('++', '+')
