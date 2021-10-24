import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='logs.log', filemode='a',format="%(asctime)s %(message)s",
                    encoding='utf-8', level=logging.DEBUG)

# Requests modülü ile web sitesine bağlanıp kodlarını aldığımız değişken.
connect = requests.get("https://www.nytimes.com/crosswords/game/mini")
logging.info(connect)

# BeatifulSoap sınıfına hangi veriyi parse edeceğimizi ve hangi method ile parse edeceğimizi söylüyoruz.
source = BeautifulSoup(connect.content, 'html5lib')