import requests
import json
from googletrans import Translator
translator = Translator()


city_name = '大阪' # 主要な都市名はいけるっぽい。
trans = translator.translate(city_name,dest='ja', src='en')
# city_name.append(dst.text)
print(trans)

API_KEY = "1d6ea2750cd6e958153b8995b195109f" # xxxに自分のAPI Keyを入力。
api = "http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={key}"


url = api.format(city = city_name, key = API_KEY)
response = requests.get(url)
data = response.json()
print(data)
# print(data["weather"][0]["description"])
