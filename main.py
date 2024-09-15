from flask import Flask, render_template, request, redirect, url_for
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuration option to enable or disable relay functionality
RELAY_ENABLED = False
RELAY_PIN = 17
active_hours = []

# Global variables to store previous readings
previous_humidity = None
previous_temperature = None

def read_dht11():
    global previous_humidity, previous_temperature

    # Dummy function for reading DHT11 sensor
    current_humidity, current_temperature = 50, 25

    if is_valid_reading(current_humidity, current_temperature):
        previous_humidity, previous_temperature = current_humidity, current_temperature
        return current_humidity, current_temperature
    else:
        # Return previous valid readings if current readings are invalid
        # return previous_humidity, previous_temperature
        print('Invalid reading detected.')
        return current_humidity, current_temperature

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)