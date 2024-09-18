import sqlite3
import time
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
import RPi.GPIO as GPIO
from datetime import datetime
import threading
import as scheduley
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Configuration option to enable or disable relay functionality
RELAY_ENABLED = False
RELAY_PIN = 17
active_hours = []

load_dotenv()

# Weather API configuration
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"
WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")  # Load from environment variable
LATITUDE = 55.53884677466315  # Replace with your actual latitude
LONGITUDE = 14.215951896226215  # Replace with your actual longitude

def read_dht11():
    try:
        result = dht11_instance.read()
        humidity, temperature = result.humidity, result.temperature
        return humidity, temperature
    except Exception as e:
        # Handle any exceptions that occur during reading
        print(f"Error reading DHT11 sensor: {e}")
        return None, None

def fetch_weather_data():
    try:
        response = requests.get(WEATHER_API_URL, params={
            'lat': LATITUDE,
            'lon': LONGITUDE,
            'units': 'metric',
            'appid': WEATHER_API_KEY
        })
        data = response.json()['list'][0]
        weather_temperature = data['main']['temp']
        weather_feels_like = data['main']['feels_like']
        weather_humidity = data['main']['humidity']
        return weather_temperature, weather_feels_like, weather_humidity
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None, None, None

def control_relay(state):
    if RELAY_ENABLED:
        GPIO.output(RELAY_PIN, GPIO.HIGH if state else GPIO.LOW)

def log_sensor_data():
    humidity, temperature = read_dht11()
    weather_temperature, weather_feels_like, weather_humidity = fetch_weather_data()
    # print all data to console
    print("log_sensor_data: ")
    print(f"Temperature: {temperature}, Humidity: {humidity}, Weather Temperature: {weather_temperature}, Weather Feels Like: {weather_feels_like}, Weather Humidity: {weather_humidity}")
    if humidity is not None and temperature is not None and weather_temperature is not None:
        current_time = datetime.now()
        date = current_time.strftime('%Y-%m-%d')
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect('sensor_data.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO sensor_data (date, timestamp, temperature, humidity, weather_temperature, weather_feels_like, weather_humidity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, timestamp, temperature, humidity, weather_temperature, weather_feels_like, weather_humidity))
        conn.commit()
        conn.close()

def schedule_logging():
    scheduley.every().hour.at(":00").do(log_sensor_data)
    scheduley.every().hour.at(":15").do(log_sensor_data)
    scheduley.every().hour.at(":30").do(log_sensor_data)
    scheduley.every().hour.at(":45").do(log_sensor_data)

    while True:
        scheduley.run_pending()
        time.sleep(1)

@app.route('/')
def index():
    humidity, temperature = read_dht11()
    relay_state = GPIO.input(RELAY_PIN) if RELAY_ENABLED else None
    return render_template('index.html', temperature=temperature, humidity=humidity, relay_state=relay_state, active_hours=active_hours, relay_enabled=RELAY_ENABLED)

@app.route('/control', methods=['POST'])
def control():
    if RELAY_ENABLED:
        action = request.form.get('action')
        if action == 'on':
            control_relay(True)
        elif action == 'off':
            control_relay(False)
    return ('', 204)

@app.route('/schedule', methods=['POST'])
def schedule():
    global active_hours
    hours = request.form.get('hours')
    active_hours = list(map(int, hours.split(',')))
    return redirect(url_for('index'))

@app.route('/api/temp_hum')
def api_temperature_humidity():
    humidity, temperature = read_dht11()
    if humidity is not None and temperature is not None:
        return jsonify({'temperature': temperature, 'humidity': humidity})
    else:
        return jsonify({'error': 'Invalid reading'}), 500
    
@app.route('/api/latest_entries')
def api_latest_entries():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10')
    data = c.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    # Start the logging thread
    threading.Thread(target=schedule_logging, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)