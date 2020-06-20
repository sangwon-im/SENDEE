import RPi.GPIO as GPIO
from time import sleep


def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    #100Hz PWM control
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    return pwm

def setMotorControl(pwm, INA, INB, speed, stat):
    
    pwm.ChangeDutyCycle(speed)
    
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
        
    elif stat == BACKWARD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)
        
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)
        
def setMotor(ch, speed, stat):
    
    if ch == CH1:
        setMotorControl(pwmA, IN1, IN2, speed, stat)
    
    else:
        setMotorControl(pwmB, IN3, IN4, speed, stat)


def Rot(speed, time):

    if speed > 0:
        setMotor(CH1, speed, FORWARD)
        setMotor(CH2, speed, BACKWARD)
        sleep(time)

    elif speed < 0:    
        setMotor(CH1, speed, BACKWARD)
        setMotor(CH2, speed, FORWARD)
        sleep(time)

    else:    
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)
        sleep(time)
        
def Servo(error_Now, time, past_dc, error_Sum, error_Prev):
    
    global head_mindc
    global head_maxdc 
    global head_interval
    
    Kp = 1
    Ki = 0.1
    Kd = 0.01

    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/interval

    ctrlval = Kp*error + Ki*error_sum*interval + Kd*error_diff
    
    if abs(ctrlval) < 0.1:
        ctrlval = 0
    
    elif abs(ctrlval) > 5:
        ctrlval = 5
    
    head_duty = past_dc + head_interval * ctrlval
    
    head.ChangeDutyCycle(head_duty)
    
    return head_duty
    

def MPIDCtrl(error_Now, interval, error_Sum, error_Prev):          # While 문 돌아갈 때 변수선언 필요 - error_Sum은 현재까지 error 합, error_Prev은 이전 error

    # Gain Values
    Kp = 1
    Ki = 0.1
    Kd = 0.01

    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/interval

    speed = 100 * (Kp*error + Ki*error_sum*interval + Kd*error_diff)

    if speed > 100:
        speed = 100

    elif speed < -100:
        speed = -100

    elif abs(speed) < 20:
        speed = 0

    Rot(speed, interval)


#Motor Status
STOP = 0
FORWARD = 1
BACKWARD = 2

#Motor Channel
CH1 = 0
CH2 = 1

#Pin Setting
HIGH = 1
LOW = 0

#Pin Assign
#PWM
ENA = 26 #pin 37
ENB = 0  #pin 27
#GPIO
IN1 = 19 #pin 35
IN2 = 13 #pin 33
IN3 = 6  #pin 31
IN4 = 5  #pin 29

# servo bound
head_mindc = 3.3
head_maxdc = 16
head_interval = (head_maxdc - head_mindc)/20

        
GPIO.setmode(GPIO.BCM)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

GPIO.setup(24, GPIO.OUT)
head = GPIO.PWM(24, 50) #pin no 18 bcm24 head
head.start(head_mindc)




#Control example

setMotor(CH1, 80, FORWARD)
setMotor(CH2, 80, FORWARD)

sleep(5)

setMotor(CH1, 40, BACKWARD)
setMotor(CH2, 40, FORWARD)
sleep(5)

setMotor(CH1, 100, BACKWARD)
setMotor(CH2, 100, BACKWARD)
sleep(5)

setMotor(CH1, 40, STOP)
setMotor(CH2, 40, STOP)

GPIO.cleanup()
    


