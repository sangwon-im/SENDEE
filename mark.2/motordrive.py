# 라즈베리파이 GPIO 핀 사용가능하도록 하는 라이브러리
import RPi.GPIO as GPIO
from time import sleep

# 해당 핀의 PWM 제어를 초기화하는 함수
# L298N 모터드라이버 제어를 위해서는 모터 당 3개의 input이 필요한데,
# EN은 속도 신호, INA는 정회전 신호, INB는 역회전 신호라고 생각하면 된다.
def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100Hz PWM control -  L298N 모터드라이버는 50Hz~1000Hz의 pwm 주파수를 사용한다고 함
    # 즉 EN 핀의 pwm 주파수를 100Hz로 설정
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    return pwm

# 모터 정회전, 역회전, 정지 상태를 구현
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

# 모터의 속도와 회전방향을 직접 설정하는 함수        
def setMotor(ch, speed, stat):
    
    if ch == CH1:
        setMotorControl(pwmA, IN1, IN2, speed, stat)
    
    else:
        setMotorControl(pwmB, IN3, IN4, speed, stat)

# setMotor 함수를 이용해서 회전 동작을 구현한 함수
# SENDEE 무게로 인해 속도 40 이하에서는 움직이지 않음, 40이 최소 속도
# time을 주어야 해당 시간동안 모터가 set 된 속도로 회전함
def Rot(speed, time):# 40-100, SECOND

    if speed > 0:
        #print('move head leftward')
        setMotor(CH1, speed, FORWARD)
        setMotor(CH2, speed, BACKWARD)
        sleep(time)

    elif speed < 0:
        #print('move head rightward')
        setMotor(CH1, -speed, BACKWARD)
        setMotor(CH2, -speed, FORWARD)
        sleep(time)

    else:    
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)
        sleep(time)
      
# time 동안 모터 회전 후 정지
    setMotor(CH1, 0, STOP)
    setMotor(CH2, 0, STOP)
#    sleep(time*0.5)

# setMotor 함수를 사용해서 전진/후진 동작을 구현한 함수
# 원리는 Rot 함수와 동일하다
def Go(speed, time):# 40-100, SECOND

    if speed > 0:
        setMotor(CH1, speed, FORWARD)
        setMotor(CH2, speed, FORWARD)
        sleep(time)

    elif speed < 0:
        setMotor(CH1, -speed, BACKWARD)
        setMotor(CH2, -speed, BACKWARD)
        sleep(time)

    else:    
        setMotor(CH1, 0, STOP)
        setMotor(CH2, 0, STOP)
        sleep(time)
        
    setMotor(CH1, 1, FORWARD)
    setMotor(CH2, 1, FORWARD)
    sleep(time*0.5)

# SENDEE 얼굴(화면)을 움직이는 서보모터 pid제어 함수 
def Servo(error_Now, time, past_dc, error_Sum, error_Prev):
    # 얼굴 최대/최소 각도, 인터벌을 글로벌 상수로 받아옴
    global head_mindc
    global head_maxdc 
    global head_interval
    
    # pid 게인값
    Kp = 0.5
    Ki = 0
    Kd = 0
    
    # pid 에러 계산
    error = error_Now
    error_sum = error_Sum + error
    error_diff = (error-error_Prev)/time
    
    # 제어값 계산
    ctrlval = -(Kp*error + Ki*error_sum*time + Kd*error_diff)
    
    # 얼굴 위치가 일정 범위 내에 들어오면 정지하도록 함
    if abs(ctrlval) < 0.02:
        ctrlval = 0
    # 제어값 반올림
    ctrlval = round(ctrlval, 1)
    
    # 듀티 사이클(실제 서보모터 각도와 일대일 대응되는 값) 계산        
    head_duty = past_dc - head_interval * ctrlval
    
    # 최대 최소 범위를 벗어날 경우 컷
    if head_duty < head_mindc:
        head_duty = head_mindc
        
    elif head_duty > head_maxdc:
        head_duty = head_maxdc
    
    print('ctrlval',ctrlval)
    
    # ctrlval이 0.02 미만으로 움직이지 않게 될 경우 steady 표시
    # 아예 duty cycle을 0으로 만들어서 서보모터에 신호가 전송되지 않도록 함
    # ctrlval이 유의미할 경우 duty cycle을 변경하여 각도 변경
    if head_duty == past_dc:
        print(head_duty, past_dc,'steady')
        head_duty = past_dc
        head.ChangeDutyCycle(0)
    else:
        print(head_duty, past_dc,'move')
        head.ChangeDutyCycle(head_duty)
    
    # while loop에서 error 계산을 위해 현재 head duty를 리턴한다.
    return head_duty
    
# 바퀴 모터 pid제어 함수, 원리는 서보 제어와 같음
def MPIDCtrl(error_Now, interval, error_Sum, error_Prev):          # While 문 돌아갈 때 변수선언 필요 - error_Sum은 현재까지 error 합, error_Prev은 이전 error

    # Gain Values
    Kp = 0.5
    Ki = 0
    Kd = 0

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
    
# SENDEE 팔의 여러 행동 셋을 만들기 위한 기본 행동 함수들
# 공통적으로 동작 실행 후 각도를 반환함

# 부르르 떠는 동작을 구현한 함수, 동작 수행 전에 팔의 위치와 떠는 횟수를 입력받음
def shake(prev_angle, cycle):
    for i in range(0, cycle):
        left.ChangeDutyCycle(left_mindc + (prev_angle + 1) * left_interval)
        right.ChangeDutyCycle(right_mindc + prev_angle * right_interval)
        sleep(0.02)
        left.ChangeDutyCycle(left_mindc + prev_angle * left_interval)
        right.ChangeDutyCycle(right_mindc + (prev_angle + 1) * right_interval)
        sleep(0.02)
        
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    return prev_angle

# 양 팔을 목표 각도로 동시에 회전하는 함수, 현재 각도와 목표 각도, 속도를 입력받음
def movetogether(prev_angle, goal_angle, speed): # angle: 0-16, speed:1,2,3,5
    
    left_status = left_mindc + left_interval * prev_angle
    right_status = right_mindc + right_interval * prev_angle
    
    stptime = 30/speed
    left_step = left_interval * (goal_angle - prev_angle) / stptime
    right_step = right_interval * (goal_angle - prev_angle) / stptime
    
    for i in range(0, int(stptime)):
        left.ChangeDutyCycle(left_status + left_step * i)
        right.ChangeDutyCycle(right_status + right_step * i)
        sleep(0.02)
    # 행동 끝난 후 서보모터가 튀지 않도록 duty cycle 0으로 만들어서 신호를 끊음
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    
    return goal_angle


# 양 팔을 반대 회전방향으로 특정 각도만큼 움직이는 함수
# 예를 들어 90도만큼 움직이도록 사용하면
# 왼  팔 : 0 ->  90 -> 0 -> -90 -> 0
# 오른팔 : 0 -> -90 -> 0 ->  90 -> 0
# 이런 식의 움직임을 구현
def moveopposite(prev_angle, amount, speed):
    
    left_status = left_mindc + left_interval * prev_angle
    right_status = right_mindc + right_interval * prev_angle
    
    stptime = 30/speed
    
    left_goal = (left_interval * amount)/stptime
    right_goal = (right_interval * amount)/stptime
    
    for i in range(0, int(stptime)):
        left.ChangeDutyCycle(left_status - left_goal * i)
        right.ChangeDutyCycle(right_status + right_goal * i)
        sleep(0.02)
        
    for i in range(1, int(stptime) + 1):
        left.ChangeDutyCycle(left_status + left_goal * (i - int(stptime)))
        right.ChangeDutyCycle(right_status + right_goal * (int(stptime) - i))
        sleep(0.02)
        
    left.ChangeDutyCycle(0)
    right.ChangeDutyCycle(0)
    
    return prev_angle

# 고개를 특정 각도, 특정 속도로 움직이는 함수
def headmove(prev_angle, goal_angle, speed):
             
    head_status = head_mindc + head_interval * prev_angle
    
    stptime = 30/speed
    head_step = head_interval * (goal_angle - prev_angle) / stptime
    
    for i in range(0, int(stptime)):
        head.ChangeDutyCycle(head_status + head_step * i)
        sleep(0.02)
    head.ChangeDutyCycle(0)
    return goal_angle

# 고개를 해당 위치에서 정지시키는 함수
def headsleep():
    head.ChangeDutyCycle(0)

# 감정에 대한 리액션 셋을 정의한 함수
def emoreact(emotion):
    #neutral, happy, surprised, 
    if emotion == 'neutral1':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(0.5)
    
    elif emotion == 'neutral2':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2.5)
        
    elif emotion == 'neutral3':
        left.ChangeDutyCycle(left_maxdc)
        right.ChangeDutyCycle(0)
        sleep(1)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(1)
        left.ChangeDutyCycle(left_mindc)
        sleep(0.5)
        left.ChangeDutyCycle(0)
        
    elif emotion == 'happy1':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2.5)
        
    elif emotion == 'happy2':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(1)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc-1)
        right.ChangeDutyCycle(right_mindc+1)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc-1)
        right.ChangeDutyCycle(right_mindc+1)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc-1)
        right.ChangeDutyCycle(right_mindc+1)
        sleep(0.18)
        left.ChangeDutyCycle(left_mindc)
        right.ChangeDutyCycle(right_mindc)
        sleep(0.5)
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        
    elif emotion == 'sad1':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        prev_angle = 0
        sleep(0.3)
        prev_angle = movetogether(prev_angle, 14, 2)
        sleep(0.5) #### sdflkasjfoasdjf
        prev_angle = movetogether(prev_angle, 0, 0.5)
        
    elif emotion == 'sad2':
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2)
        prev_angle = 0
        prev_angle = movetogether(prev_angle, 2, 3)
        prev_angle = movetogether(prev_angle, 0, 3)
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        
    elif emotion == 'angry1':
        # Go(-40, 0.5)
        sleep(0.5)
        shake(0, 15)
        # Go(40, 0.5)
    
    elif emotion == 'angry2':
        sleep(1.4)


    elif emotion == 'fear1':
        prev_angle = 14
        sleep(1)
        prev_angle = movetogether(prev_angle, 14, 3)
        sleep(0.2)
        prev_angle = moveopposite(prev_angle, 2, 5)
        prev_angle = moveopposite(prev_angle, -2, 5)
        prev_angle = moveopposite(prev_angle, 2, 5)
        prev_angle = moveopposite(prev_angle, -2, 5)
        prev_angle = moveopposite(prev_angle, 2, 5)
        prev_angle = moveopposite(prev_angle, -2, 5)
        sleep(0.5)
        prev_angle = movetogether(prev_angle, 0, 3)
        
    elif emotion == 'surprised1':
        prev_angle = 0
        sleep(0.1)
        prev_angle = movetogether(prev_angle, 5, 5)
        prev_angle = movetogether(prev_angle, 0, 5)
        sleep(1.5)
    
    elif emotion == 'surprised2':
        left.ChangeDutyCycle(left_maxdc)
        right.ChangeDutyCycle(0)
        sleep(1)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc)
        sleep(0.2)
        left.ChangeDutyCycle(left_maxdc-1)
        sleep(1)
        left.ChangeDutyCycle(left_mindc)
        sleep(0.5)
        left.ChangeDutyCycle(0)
        # Rot(-40, 0.1)
        # sleep(0.8)
        # # Rot(40, 0.2)
        # sleep(0.65)
        # Rot(-40, 0.1)

    else:
        left.ChangeDutyCycle(0)
        right.ChangeDutyCycle(0)
        sleep(2.5)
        

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
head_mindc = 3
head_maxdc = 9
head_interval = (head_maxdc - head_mindc)/16

        
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

GPIO.setup(24, GPIO.OUT)
head = GPIO.PWM(24, 50) #pin no 18 bcm24 head
head.start(head_mindc + 1)
head.ChangeDutyCycle(0)
print('head ready')


right_mindc = 5
right_maxdc = 10
right_interval = (right_maxdc - right_mindc)/16

left_mindc = 11
left_maxdc = 4
left_interval = (left_maxdc - left_mindc)/16

# percent

GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
left = GPIO.PWM(27, 50)
right = GPIO.PWM(22, 50)

left.start(left_mindc)
right.start(right_mindc)
left.ChangeDutyCycle(0)
right.ChangeDutyCycle(0)
print('arm ready')



#Control example
#     
# prev_angle = 0
# head_angle = 0
# 
# 
# while True:
#     
# #     prev_angle = movetogether(prev_angle, 0, 1)
# #     sleep(1)
#     emoreact('surprise2')
#     sleep(1)

    
#GPIO.cleanup()
