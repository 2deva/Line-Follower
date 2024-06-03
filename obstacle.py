import utime
from machine import Pin, time_pulse_us

motor_a1 = Pin(0, Pin.OUT)
motor_a2 = Pin(1, Pin.OUT)
motor_b1 = Pin(2, Pin.OUT)
motor_b2 = Pin(3, Pin.OUT)

echo = Pin(14, mode=Pin.IN, pull=None)
trigger = Pin(15, mode=Pin.OUT, pull=None)


def get_distance():
    echo_timeout = 3000
    trigger.value(0)

    utime.sleep(0.05)
    trigger.value(1)

    utime.sleep(0.05)
    trigger.value(0)

    pulse_time = time_pulse_us(echo, 1, echo_timeout)
    cms = (pulse_time / 2) / 29.1
    if cms > 0:
        return cms
    return -1


def forward():
    motor_a1.low()
    motor_a2.high()
    motor_b1.low()
    motor_b2.high()


def right():
    motor_a1.low()
    motor_a2.high()
    motor_b1.high()
    motor_b2.low()


def left():
    motor_a1.high()
    motor_a2.low()
    motor_b1.low()
    motor_b2.high()


def back():
    motor_a1.high()
    motor_a2.low()
    motor_b1.high()
    motor_b2.low()


while True:
    distance = get_distance()
    print(distance)
    if distance <= 15 and distance != -1:
        print("Obstacle ahead. turning back and taking right!")
        back()
        utime.sleep(0.1)
        right()
        utime.sleep(0.1)
    else:
        print("forward")
        forward()

    utime.sleep(0.01)
