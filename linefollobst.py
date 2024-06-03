import RPi.GPIO as GPIO
import time

# Set up GPIO mode and warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define motor control pins
motor_a1_pin = 17  # Left Motor forward
motor_a2_pin = 18  # Left Motor backward
motor_b1_pin = 22  # Right Motor forward
motor_b2_pin = 21  # Right Motor backward

# Define ultrasonic sensor pins
echo_pin = 11
trigger_pin = 12

# Define line sensor pins
left_sensor_pin = 14
right_sensor_pin = 15

# Set up motor control pins as output
GPIO.setup(motor_a1_pin, GPIO.OUT)
GPIO.setup(motor_a2_pin, GPIO.OUT)
GPIO.setup(motor_b1_pin, GPIO.OUT)
GPIO.setup(motor_b2_pin, GPIO.OUT)

# Set up ultrasonic sensor pins
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(trigger_pin, GPIO.OUT)

# Set up line sensor pins as input
GPIO.setup(left_sensor_pin, GPIO.IN)
GPIO.setup(right_sensor_pin, GPIO.IN)

# Function to get distance from the ultrasonic sensor
def get_distance():
    GPIO.output(trigger_pin, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.05)
    GPIO.output(trigger_pin, GPIO.LOW)
    
    pulse_start = time.time()
    pulse_end = time.time()
    
    while GPIO.input(echo_pin) == GPIO.LOW:
        pulse_start = time.time()
        if (pulse_start - pulse_end) > 0.01:
            break
    
    while GPIO.input(echo_pin) == GPIO.HIGH:
        pulse_end = time.time()
        if (pulse_end - pulse_start) > 0.01:
            break
    
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 34300) / 2
    if distance < 0:
        return -1
    return distance

# Motor control functions
def forward():
    GPIO.output(motor_a1_pin, GPIO.HIGH)
    GPIO.output(motor_a2_pin, GPIO.LOW)
    GPIO.output(motor_b1_pin, GPIO.HIGH)
    GPIO.output(motor_b2_pin, GPIO.LOW)
    print("Moving forward")

def backward():
    GPIO.output(motor_a1_pin, GPIO.LOW)
    GPIO.output(motor_a2_pin, GPIO.HIGH)
    GPIO.output(motor_b1_pin, GPIO.LOW)
    GPIO.output(motor_b2_pin, GPIO.HIGH)
    print("Moving backward")

def left():
    GPIO.output(motor_a1_pin, GPIO.LOW)
    GPIO.output(motor_a2_pin, GPIO.LOW)
    GPIO.output(motor_b1_pin, GPIO.HIGH)
    GPIO.output(motor_b2_pin, GPIO.LOW)
    print("Turning left")

def right():
    GPIO.output(motor_a1_pin, GPIO.HIGH)
    GPIO.output(motor_a2_pin, GPIO.LOW)
    GPIO.output(motor_b1_pin, GPIO.LOW)
    GPIO.output(motor_b2_pin, GPIO.HIGH)
    print("Turning right")

def stop():
    GPIO.output(motor_a1_pin, GPIO.LOW)
    GPIO.output(motor_a2_pin, GPIO.LOW)
    GPIO.output(motor_b1_pin, GPIO.LOW)
    GPIO.output(motor_b2_pin, GPIO.LOW)
    print("Stopping")

# Main loop combining line following and obstacle detection
try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance} cm")
        
        left_sensor = GPIO.input(left_sensor_pin)
        right_sensor = GPIO.input(right_sensor_pin)

        if distance <= 15 and distance != -1:
            print("Obstacle ahead. Moving back and attempting to turn!")
            backward()
            time.sleep(0.5)
            stop()
            time.sleep(0.2)
            distance_right = get_distance()
            right()
            time.sleep(0.5)
            stop()
            time.sleep(0.2)
            distance_left = get_distance()
            left()
            time.sleep(0.5)
            stop()
            time.sleep(0.2)
            if distance_left < distance_right:
                print("Turning right!")
                right()
                time.sleep(0.5)
                forward()
            else:
                print("Turning left!")
                left()
                time.sleep(0.5)
                forward()
        else:
            if left_sensor == 0 and right_sensor == 0:
                forward()
            elif left_sensor == 1 and right_sensor == 0:
                right()
            elif left_sensor == 0 and right_sensor == 1:
                left()
            else:
                stop()
        time.sleep(0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting program...")
