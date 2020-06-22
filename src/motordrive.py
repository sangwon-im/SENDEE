import RPi.GPIO as GPIO
from time import sleep
#import serial


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
        print('move head leftward')
        setMotor(CH1, speed, FORWARD)
        setMotor(CH2, speed, BACKWARD)
        sleep(time)

    elif speed < 0:
        print('move head rightward')
        setMotor(CH1, -speed, BACKWARD)
        setMotor(CH2, -speed, FORWARD)
        sleep(time)

    else:    
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)
        sleep(time)
        
    setMotor(CH1, 0, STOP)
    setMotor(CH2, 0, STOP)
#    sleep(time*0.5)

def Go(speed, time):

    if speed > 0:
        print('move head leftward')
        setMotor(CH1, speed, FORWARD)
        setMotor(CH2, speed, FORWARD)
        sleep(time)

    elif speed < 0:
        print('move head rightward')
        setMotor(CH1, -speed, BACKWARD)
        setMotor(CH2, -speed, BACKWARD)
        sleep(time)

    else:    
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)
        sleep(time)
        
    setMotor(CH1, 0, STOP)
    setMotor(CH2, 0, STOP)
    sleep(time*0.5)
        
def Servo(error_Now, time, past_dc, error_Sum, error_Prev):
    
    global head_mindc
    global head_maxdc 
    global head_interval
    
    Kp = 1
    Ki = 0
    Kd = 0

    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/time

    ctrlval = -(Kp*error + Ki*error_sum*time + Kd*error_diff)
    
    if abs(ctrlval) < 0.25:
        ctrlval = 0
    
    elif abs(ctrlval) > 2:
        ctrlval = 2
        
    if ctrlval > 0:
        print('move head upward')
    elif ctrlval < 0:
        print('move head downward')
        
#    ctrlval = round(ctrlval)
            
    head_duty = past_dc - head_interval * ctrlval
    
    if head_duty < head_mindc:
        head_duty = head_mindc
        
    elif head_duty > head_maxdc:
        head_duty = head_maxdc
        
    print(head_duty)
    
    if head_duty == past_dc:
        print('steady')
    else:
        head.ChangeDutyCycle(head_duty)
    
    return head_duty
    

def MPIDCtrl(error_Now, interval, error_Sum, error_Prev):          # While 문 돌아갈 때 변수선언 필요 - error_Sum은 현재까지 error 합, error_Prev은 이전 error

    # Gain Values
    Kp = 0.6
    Ki = 0
    Kd = 0.05

    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/interval

    speed = -100 * (Kp*error + Ki*error_sum*interval + Kd*error_diff)

    if speed > 100:
        speed = 100

    elif speed < -100:
        speed = -100
        
    elif 10 < speed < 40:
        speed = 40
        
    elif -40 < speed < -10:
        speed = -40

    if abs(speed) < 10:
        speed = 0
    
    Rot(speed, interval)

# def Angry():
#     ser.write(b"Angry\n")
#     #Angry 해당되는 motion
# 
# def Sad():
#     ser.write(b"Sad\n")
#     #Sad 해당되는 motion
# 
# def Happy():
#     ser.write(b"Happy\n")
#     #Angry 해당되는 motion
# 
# def Disgust():
#     ser.write(b"Disgust\n")
#     #Sad 해당되는 motion
# 
# def Fear():
#     ser.write(b"Fear\n")
#     #Angry 해당되는 motion
# 
# def Surprised():
#     ser.write(b"Surprised\n")
#     #Sad 해당되는 motion
# 
# def Neutral():
#     ser.write(b"Neutral\n")
#     #Angry 해당되는 motion
# 
# def Sad():
#     ser.write(b"Sad\n")
#     #Sad 해당되는 motion

    


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
head_mindc = 1
head_maxdc = 5
head_interval = (head_maxdc - head_mindc)/10

        
GPIO.setmode(GPIO.BCM)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

GPIO.setup(24, GPIO.OUT)
head = GPIO.PWM(24, 50) #pin no 18 bcm24 head
head.start(head_mindc)
print('ready')


#ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1) #Port 확인, TIMEOUT 수정
#ser.flush()


#Control example
# 
# setMotor(CH1, 80, FORWARD)
# setMotor(CH2, 80, FORWARD)
# 
# sleep(5)
# 
# setMotor(CH1, 40, BACKWARD)
# setMotor(CH2, 40, FORWARD)
# sleep(5)
# 
# setMotor(CH1, 100, BACKWARD)
# setMotor(CH2, 100, BACKWARD)
# sleep(5)
# 
# setMotor(CH1, 40, STOP)
# setMotor(CH2, 40, STOP)
# 
# GPIO.cleanup()
