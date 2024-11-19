import os
import random
import googlemaps
from flask import Flask, render_template
from datetime import datetime

from lib.database import Database
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY") # Your Google Maps API KEY
LOCATION = {'lat': 22.6235157, 'lng': 120.2837442}
gmaps = googlemaps.Client(key=API_KEY)

app = Flask(__name__, static_folder="assets")
db = Database('assets/website.db')

@app.route("/")
def index():
    food = random.choice(os.listdir('assets/img'))
    name = food.split('.')[0]
    places_result = gmaps.places_nearby(LOCATION, keyword=name, radius=500, language="zh-tw")

    data = []
    for place in places_result.get("results", []):
        search_name = place.get("name")
        
        field = []
        field.append("https://www.google.com/maps/search/"+search_name)
        field.append(f'地點名稱: {search_name}')
        field.append(f'地址: {place.get("vicinity")}')
        
        opening_hours = gmaps.place(place.get('place_id'), language='zh-tw').get("result", {}).get("opening_hours", {})
        
        if opening_hours.get("weekday_text"):
           field.append(f'營業時間(今日): {opening_hours["weekday_text"][datetime.utcnow().isoweekday()-1][4:]}')
           
        else:
            field.append('營業時間(今日): 無資訊')
            
        data.append(field)
        
    return render_template('index.html', food=food, name=name, details=db.get(name), data=data)

@app.route('/reset')
def reset():
    return index()

app.run()