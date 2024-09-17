from flask import Flask, render_template, request, redirect, url_for, jsonify
import RPi.GPIO as GPIO
import threading
import time
import datetime
import dht11

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
DHT_PIN = 4
dht11_instance = dht11.DHT11(pin=DHT_PIN)

# Configuration option to enable or disable relay functionality
RELAY_ENABLED = False
RELAY_PIN = 17
active_hours = []

# Global variables to store previous readings
previous_humidity = None
previous_temperature = None

def read_dht11():
    global previous_humidity, previous_temperature

    # Ensure dht11_instance is defined and initialized
    try:
        result = dht11_instance.read()
        current_humidity, current_temperature = result.humidity, result.temperature

        if is_valid_reading(current_humidity, current_temperature):
            previous_humidity, previous_temperature = current_humidity, current_temperature
            return current_humidity, current_temperature
        else:
            # Log invalid reading to console
            print('Invalid reading detected.')
            # Return previous valid readings if current readings are invalid
            return None, None
    except Exception as e:
        # Handle any exceptions that occur during reading
        print(f"Error reading DHT11 sensor: {e}")
        # Return previous valid readings in case of an error
        return None, None

def is_valid_reading(current_humidity, current_temperature):
    global previous_humidity, previous_temperature

    if previous_humidity is None or previous_temperature is None:
        return True

    # Define thresholds for sudden jumps
    humidity_threshold = 10
    temperature_threshold = 5

    if abs(current_humidity - previous_humidity) > humidity_threshold or abs(current_temperature - previous_temperature) > temperature_threshold:
        return False

    return True

def control_relay(state):
    if RELAY_ENABLED:
        GPIO.output(RELAY_PIN, GPIO.HIGH if state else GPIO.LOW)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)