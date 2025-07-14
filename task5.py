from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)


API_KEY = ' ADD YOUR_OPENWEATHERMAP_API_KEY'

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f4f8; margin: 0; padding: 0; }
        .container { max-width: 400px; margin: 40px auto; background: #fff; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h2 { text-align: center; }
        #weather { margin-top: 20px; }
        .input-group { display: flex; }
        .input-group input { flex: 1; padding: 8px; }
        .input-group button { padding: 8px 12px; }
        .location-btn { margin-top: 10px; width: 100%; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Weather App</h2>
        <div class="input-group">
            <input type="text" id="cityInput" placeholder="Enter city name">
            <button onclick="getWeatherByCity()">Search</button>
        </div>
        <button class="location-btn" onclick="getWeatherByLocation()">Use My Location</button>
        <div id="weather"></div>
    </div>
    <script>
        function displayWeather(data) {
            if (data.error) {
                document.getElementById('weather').innerHTML = `<p style='color:red;'>${data.error}</p>`;
                return;
            }
            document.getElementById('weather').innerHTML = `
                <h3>${data.city}, ${data.country}</h3>
                <p><b>Condition:</b> ${data.weather}</p>
                <p><b>Temperature:</b> ${data.temp}°C</p>
                <p><b>Humidity:</b> ${data.humidity}%</p>
                <p><b>Wind Speed:</b> ${data.wind} m/s</p>
            `;
        }
        function getWeatherByCity() {
            const city = document.getElementById('cityInput').value;
            if (!city) return alert('Please enter a city name.');
            fetch(`/weather?city=${encodeURIComponent(city)}`)
                .then(res => res.json())
                .then(displayWeather);
        }
        function getWeatherByLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(pos => {
                    const lat = pos.coords.latitude;
                    const lon = pos.coords.longitude;
                    fetch(`/weather?lat=${lat}&lon=${lon}`)
                        .then(res => res.json())
                        .then(displayWeather);
                }, err => {
                    alert('Could not get your location.');
                });
            } else {
                alert('Geolocation is not supported by your browser.');
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/weather')
def weather():
    city = request.args.get('city')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if city:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    elif lat and lon:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    else:
        return jsonify({'error': 'No location provided.'})
    try:
        r = requests.get(url)
        data = r.json()
        if data.get('cod') != 200:
            return jsonify({'error': data.get('message', 'Error fetching weather.')})
        result = {
            'city': data['name'],
            'country': data['sys']['country'],
            'weather': data['weather'][0]['description'].title(),
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind': data['wind']['speed']
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)