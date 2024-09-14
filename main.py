import RPi.GPIO as GPIO
import dht11
from flask import Flask, render_template, request, redirect, url_for
import threading
import time
import datetime

# GPIO setup
RELAY_PIN = 17
DHT_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

# Initialize DHT11 instance
dht11_instance = dht11.DHT11(pin=DHT_PIN)

app = Flask(__name__)

# Store active hours in a list
active_hours = []

# Function to control relay
def control_relay(state):
    GPIO.output(RELAY_PIN, GPIO.HIGH if state else GPIO.LOW)

# Function to read DHT11 sensor
def read_dht11():
    result = dht11_instance.read()
    if result.is_valid():
        return result.humidity, result.temperature
    else:
        return None, None

# Function to schedule relay control
def schedule_relay():
    while True:
        now = datetime.datetime.now()
        if now.hour in active_hours:
            control_relay(True)
        else:
            control_relay(False)
        time.sleep(60)  # Check every minute

# Start scheduling in a separate thread
threading.Thread(target=schedule_relay, daemon=True).start()

# Flask routes
@app.route('/')
def index():
    humidity, temperature = read_dht11()
    relay_state = GPIO.input(RELAY_PIN)
    return render_template('index.html', temperature=temperature, humidity=humidity, relay_state=relay_state, active_hours=active_hours)

@app.route('/control', methods=['POST'])
def control():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)