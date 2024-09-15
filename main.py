from flask import Flask, render_template, request, redirect, url_for
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configuration option to enable or disable relay functionality
RELAY_ENABLED = False
RELAY_PIN = 17
active_hours = []

def read_dht11():
    # Dummy function for reading DHT11 sensor
    return 50, 25

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