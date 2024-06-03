from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import subprocess
import os
import signal
import time

app = Flask(__name__)

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_pins = {
    "left_motor_forward": 17,
    "left_motor_backward": 18,
    "right_motor_forward": 22,
    "right_motor_backward": 21
}

for pin in motor_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Ensure all pins are low initially

# Store subprocesses
running_processes = []

# Define motor control functions
def forward():
    GPIO.output(motor_pins["left_motor_forward"], GPIO.HIGH)
    GPIO.output(motor_pins["left_motor_backward"], GPIO.LOW)
    GPIO.output(motor_pins["right_motor_forward"], GPIO.HIGH)
    GPIO.output(motor_pins["right_motor_backward"], GPIO.LOW)
    print("Moving forward")

def backward():
    GPIO.output(motor_pins["left_motor_forward"], GPIO.LOW)
    GPIO.output(motor_pins["left_motor_backward"], GPIO.HIGH)
    GPIO.output(motor_pins["right_motor_forward"], GPIO.LOW)
    GPIO.output(motor_pins["right_motor_backward"], GPIO.HIGH)
    print("Moving backward")

def left():
    GPIO.output(motor_pins["left_motor_forward"], GPIO.LOW)
    GPIO.output(motor_pins["left_motor_backward"], GPIO.HIGH)
    GPIO.output(motor_pins["right_motor_forward"], GPIO.HIGH)
    GPIO.output(motor_pins["right_motor_backward"], GPIO.LOW)
    print("Turning left")

def right():
    GPIO.output(motor_pins["left_motor_forward"], GPIO.HIGH)
    GPIO.output(motor_pins["left_motor_backward"], GPIO.LOW)
    GPIO.output(motor_pins["right_motor_forward"], GPIO.LOW)
    GPIO.output(motor_pins["right_motor_backward"], GPIO.HIGH)
    print("Turning right")

def stop():
    GPIO.output(motor_pins["left_motor_forward"], GPIO.LOW)
    GPIO.output(motor_pins["left_motor_backward"], GPIO.LOW)
    GPIO.output(motor_pins["right_motor_forward"], GPIO.LOW)
    GPIO.output(motor_pins["right_motor_backward"], GPIO.LOW)
    print("Stopping")
    stop_all_processes()

def stop_all_processes():
    global running_processes
    for process in running_processes:
        if process.poll() is None:  # Process is still running
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    running_processes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def control():
    data = request.get_json()
    direction = data['direction']
    print(f"Received direction: {direction}")  # Log the direction to the console

    if direction == 'forward':
        forward()
    elif direction == 'backward':
        backward()
    elif direction == 'left':
        left()
    elif direction == 'right':
        right()
    elif direction == 'stop':
        stop()

    return jsonify({"status": "success"}), 200

@app.route('/run_line_following_robot')
def run_line_following_robot():
    stop_all_processes()
    process = subprocess.Popen(["python", "linefollower.py"], preexec_fn=os.setsid)
    running_processes.append(process)
    return 'Line Following Robot code is running'

@app.route('/run_curve_line_following_robot')
def run_curve_line_following_robot():
    stop_all_processes()
    process = subprocess.Popen(["python", "linefollower.py"], preexec_fn=os.setsid)
    running_processes.append(process)
    return 'Curve Line Following Robot code is running'

@app.route('/run_obstacle_playaround')
def run_obstacle_playaround():
    stop_all_processes()
    process = subprocess.Popen(["python", "ObstaclePlay.py"], preexec_fn=os.setsid)
    running_processes.append(process)
    return 'Obstacle Playaround code is running'

@app.route('/run_line_following_with_obstacle_detection')
def run_line_following_with_obstacle_detection():
    stop_all_processes()
    process = subprocess.Popen(["python", "linefollobst.py"], preexec_fn=os.setsid)
    running_processes.append(process)
    return 'Line Following with Obstacle Detection code is running'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
