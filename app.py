from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
WEATHER_API_KEY = '9d08841fb334f501656cf35139431582'

def getVisitorIp():
    return request.remote_addr

def get_Visitor_location_temp(ip_addr):
    try:
        # Get the visitor location
        location = f'https://ipapi.co/{ip_addr}/json/'
        response = requests.get(location)
        location_info = response.json()
        region = location_info.get('region', 'Unknown')
        latitude = location_info.get('latitude')
        longitude = location_info.get('longitude')

        # Check if latitude and longitude are available
        if not latitude or not longitude:
            return "NULL", "NULL"

        # Get the temperature information
        weatherReq = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={WEATHER_API_KEY}&units=metric'
        weather_response = requests.get(weatherReq)
        weather_info = weather_response.json()
        temp = weather_info['main']['temp'] if 'main' in weather_info else "Not Available"
        
        location = f'{region}'
        return location, temp
    except Exception as e:
        print(f"Error fetching data: {e}")
        return "Unknown", "Not available"

@app.route('/api/hello', methods=['GET'])
def home():
    visitor_name = request.args.get('visitor_name')
    client_ip = getVisitorIp()
    location, temperature = get_Visitor_location_temp(client_ip)
    
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    
    response = {
        "client_ip": client_ip,
        "location": location,
        "greeting": greeting
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
