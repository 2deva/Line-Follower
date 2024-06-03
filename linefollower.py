import RPi.GPIO as GPIO
import time

# Set up GPIO mode and warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define onboard LED pin (assuming GPIO pin 25, check your Raspberry Pi's documentation)
led_pin = 25
GPIO.setup(led_pin, GPIO.OUT)

# Define motor control pins
left_motor_forward_pin = 17  # Controls left motor forward movement
left_motor_backward_pin = 18  # Controls left motor backward movement
right_motor_forward_pin = 22  # Controls right motor forward movement
right_motor_backward_pin = 21  # Controls right motor backward movement

# Define line sensor pins
left_sensor_pin = 14  # Reads left line sensor (white = 1, black = 0)
right_sensor_pin = 15  # Reads right line sensor (white = 1, black = 0)

# Set up motor control pins as output
GPIO.setup(left_motor_forward_pin, GPIO.OUT)
GPIO.setup(left_motor_backward_pin, GPIO.OUT)
GPIO.setup(right_motor_forward_pin, GPIO.OUT)
GPIO.setup(right_motor_backward_pin, GPIO.OUT)

# Set up line sensor pins as input
GPIO.setup(left_sensor_pin, GPIO.IN)
GPIO.setup(right_sensor_pin, GPIO.IN)

# Function to move the robot forward with LED on
def move_forward():
    GPIO.output(left_motor_forward_pin, GPIO.HIGH)
    GPIO.output(left_motor_backward_pin, GPIO.LOW)
    GPIO.output(right_motor_forward_pin, GPIO.HIGH)
    GPIO.output(right_motor_backward_pin, GPIO.LOW)
    GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
    print("Moving forward")

# Function to move the robot backward with LED on
def move_backward():
    GPIO.output(left_motor_forward_pin, GPIO.LOW)
    GPIO.output(left_motor_backward_pin, GPIO.HIGH)
    GPIO.output(right_motor_forward_pin, GPIO.LOW)
    GPIO.output(right_motor_backward_pin, GPIO.HIGH)
    GPIO.output(led_pin, GPIO.HIGH)  # Turn LED on
    print("Moving backward")

# Function to turn left with LED blinking
def turn_left():
    GPIO.output(left_motor_forward_pin, GPIO.LOW)
    GPIO.output(left_motor_backward_pin, GPIO.LOW)
    GPIO.output(right_motor_forward_pin, GPIO.HIGH)
    GPIO.output(right_motor_backward_pin, GPIO.LOW)
    for _ in range(2):  # Blink LED twice
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.1)
    print("Turning left")

# Function to turn right with LED blinking
def turn_right():
    GPIO.output(left_motor_forward_pin, GPIO.HIGH)
    GPIO.output(left_motor_backward_pin, GPIO.LOW)
    GPIO.output(right_motor_forward_pin, GPIO.LOW)
    GPIO.output(right_motor_backward_pin, GPIO.LOW)
    for _ in range(2):  # Blink LED twice
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(0.1)
    print("Turning right")

try:
    while True:
        # Read sensor values (1 = white, 0 = black)
        left_value = GPIO.input(left_sensor_pin)
        right_value = GPIO.input(right_sensor_pin)

        # Check sensor readings and take action (LED status adjusted)
        if left_value == 0 and right_value == 0:
            move_forward()
        elif left_value == 0 and right_value == 1:
            turn_right()
        elif left_value == 1 and right_value == 0:
            turn_left()
        else:
            move_backward()

        # Delay for stability
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up GPIO pins (set all to LOW)
    GPIO.output(led_pin, GPIO.LOW)
    GPIO.output(left_motor_forward_pin, GPIO.LOW)
    GPIO.output(left_motor_backward_pin, GPIO.LOW)
    GPIO.output(right_motor_forward_pin, GPIO.LOW)
    GPIO.output(right_motor_backward_pin, GPIO.LOW)
    GPIO.cleanup()
    print("Exiting program...")