from flask import Flask, render_template, request
import RPi.GPIO as GPIO
from time import sleep
RGB_PINS = [11, 13, 15]
GPIO.setmode(GPIO.BOARD)
led = 8
INDEX = 0
isOn=False
buzzer = 8


# set pins as outputs
for i in RGB_PINS:
    GPIO.setup(i, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

def turnOff():
    global isOn
    isOn=False
    for i in RGB_PINS:
        GPIO.output(i, GPIO.LOW)

def white():
    for i in RGB_PINS:
        GPIO.output(i, GPIO.HIGH)

def red():
    GPIO.output(RGB_PINS[0], GPIO.HIGH)
    GPIO.output(RGB_PINS[1], GPIO.LOW)
    GPIO.output(RGB_PINS[2], GPIO.LOW)

def green():
    GPIO.output(RGB_PINS[0], GPIO.LOW)
    GPIO.output(RGB_PINS[1], GPIO.HIGH)
    GPIO.output(RGB_PINS[2], GPIO.LOW)

def blue():
    GPIO.output(RGB_PINS[0], GPIO.LOW)
    GPIO.output(RGB_PINS[1], GPIO.LOW)
    GPIO.output(RGB_PINS[2], GPIO.HIGH)

def yellow():
    GPIO.output(RGB_PINS[0], GPIO.HIGH)
    GPIO.output(RGB_PINS[1], GPIO.HIGH)
    GPIO.output(RGB_PINS[2], GPIO.LOW)

def purple():
    GPIO.output(RGB_PINS[0], GPIO.HIGH)
    GPIO.output(RGB_PINS[1], GPIO.LOW)
    GPIO.output(RGB_PINS[2], GPIO.HIGH)

def lightBlue():
    GPIO.output(RGB_PINS[0], GPIO.LOW)
    GPIO.output(RGB_PINS[1], GPIO.HIGH)
    GPIO.output(RGB_PINS[2], GPIO.HIGH)

pwm=GPIO.PWM(buzzer, 1000)
def beep():
    pwm.start(100)
    print('beeping')
    pwm.stop()

functions = [red, green, blue, yellow, purple, purple, lightBlue]

GPIO.setup(led, GPIO.OUT)

def on():
    GPIO.output(led, GPIO.HIGH)

def off():
    GPIO.output(led, GPIO.LOW)

app = Flask(__name__)
FLASK_GET = None


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/6d7bf9c4-33d1-4a18-a2d9-27fbe733e95b", methods=['GET'])
def getname():
    global FLASK_GET, INDEX, isOn
    FLASK_GET = name = request.args.get('name')

    match name:
        case 'Thumb_Up':
            if isOn==True:
                functions[INDEX % len(functions)]()
                INDEX += 1
            print(INDEX)

        case 'Open_Palm':
            isOn=True
            on()
            index = 0

        case 'Closed_Fist':
            turnOff()
            index = 0
            off()

    return f"<p>received:{name}</p>"


if __name__ == '__main__':

    app.run(host='0.0.0.0')
