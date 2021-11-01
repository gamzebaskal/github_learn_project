import logging
import json

import requests
from bs4 import BeautifulSoup

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

def update_json(data, file, key="clue"):
    """
    Verilen json dosyadaki, istenilen anahtarın değerini, liste olarak gönderilen verileri ekleyerek günceller.
    :param data: Json dosyaya eklenecek verilerin listesi.
    :param file: Eklemenin yapılacağı json dosya.
    :param key: Json dosyasındaki güncelleme yapılmak istenen anahtar.
    :return: Geriye değer döndürmez.
    """
    file_data = json.load(file)

    file_data[key].extend(data)
    file.seek(0)
    json.dump(file_data, file, indent=4)


try:
    with open("clue.json", "r+") as f:
        update_json(clue["clue"], f)

except FileNotFoundError as e:
    logging.error(e)
    with open("clue.json", "w") as f:
        json.dump(clue, f, indent=4)

print(text)

