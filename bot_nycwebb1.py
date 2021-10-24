import requests
from bs4 import BeautifulSoup
import logging
import json

logging.basicConfig(filename='logs.log', filemode='a', format="%(asctime)s %(message)s",
                    encoding='utf-8', level=logging.DEBUG)

# Requests modülü ile web sitesine bağlanıp kodlarını aldığımız değişken.
connect = requests.get("https://www.nytimes.com/crosswords/game/mini")
logging.info(connect)

# BeatifulSoap sınıfına hangi veriyi parse edeceğimizi ve hangi method ile parse edeceğimizi söylüyoruz.
source = BeautifulSoup(connect.content, 'html5lib')

# Parse edilmiş veriler arasından ihtiyacımız olanları class özniteliğine göre filtre ediyoruz.
selected_items = source.find_all("div", attrs={"class": "ClueList-wrapper--3m-kd"})

text = ""

clues = {
    "clues": []
}

for i in selected_items:
    # erişitiğimiz metinleri istediğimiz biçime getirerek başlıklar halinde text değişkenine ekliyoruz.
    head = i.find('h3').text
    text += f"=== {head} ===\n"
    for number, txt in i.find_all("li"):
        """
        li tagleri arasında bulunan satırları seçerek başlıkların altına ekliyoruz.
        """
        text += f"{number.text}. {txt.text}\n"
        clues['clues'].append({"Group": head,
                               "Number": number.text,
                               "String": txt.text})

print(text)
with open("clues.json", "a") as f:
    print(json.dumps(clues), file=f)
