from flask import Flask, request, jsonify
import requests
# from dotenv import load_dotenv
# import os

# load_dotenv()
WEATHER_API_KEY='9d08841fb334f501656cf35139431582'
app = Flask(__name__)

def get_client_location_temp(ip_addr):
    # Get the visitor's location
    location = f'https://ipapi.co/{ip_addr}/json/'
    location_response = requests.get(location)
    location_info = location_response.json()

    city = location_info.get('city', 'Unknown')
    latitude = location_info.get('latitude')
    longitude = location_info.get('longitude')

    if latitude and longitude:
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
        weather_info = weather_response.json()
        temp = weather_info['main']['temp'] if 'main' in weather_info else "Not available"
    else:
        temp = "Couldnt get Temp"
    return city, temp

@app.route('/api/hello', methods=['GET'])
def home():
    visitor_name = request.args.get('visitor_name')
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)#'X-Forwarded-For' header is useful for the real client IP in production

    location, temperature = get_client_location_temp(client_ip)

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
