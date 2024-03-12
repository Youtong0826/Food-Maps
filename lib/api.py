import googlemaps
import requests

from dotenv import load_dotenv
load_dotenv()

API_KEY = ""
LOCATION = {'lat': 22.6235157, 'lng': 120.2837442}

def place_details(api_key, place_id, language="zh-TW"):
    """
    使用 Google Places API 的 place_details 函數取得指定地點的詳細資訊，包括營業時間。

    :param api_key: 你的 Google Cloud Platform API 金鑰
    :param place_id: 地點的唯一標識符
    :param language: 回傳結果的語言，預設為繁體中文 "zh-TW"
    :return: 回傳 API 的 JSON 回應
    """
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "key": api_key,
        "place_id": place_id,
        "language": language,
    }

    response = requests.get(base_url, params=params)
    result = response.json()

    return result