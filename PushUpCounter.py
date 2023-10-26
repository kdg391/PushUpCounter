import cv2
import numpy as np
import PoseModule as pm
import time
import pygame

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
direction = 0
form = 0
feedback = "Fix Form"

mirror = True
is_playing = False
# 1번 ~ 10번 갯수를 말했는지 True False
spoken_numbers = [False] * 9

prev_elbow_angle = 0
prev_time = time.time()


slow_threshold = 10  # 느린 경우
fast_threshold = 30  # 빠른 경우

window_name = 'Pushup Counter' # OpenCV 창 이름

cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)

pygame.mixer.init()

def speak(text: str): # tts mp3 파일 재생
    global is_playing # is_playing을 전역 변수로 선언

    if is_playing:
        return
    
    is_playing = True

    pygame.mixer.music.load(f'voice/{text.lower()}.mp3')
    pygame.mixer.music.play()

    is_playing = False

while cap.isOpened():
    ret, img = cap.read() #640 x 480
    if mirror:
        img = cv2.flip(img, 1)
    #Determine dimensions of video - Help with creation of box in Line 43
    width  = cap.get(3)  # float `width`
    height = cap.get(4)  # float `height`
    # print(width, height)
    
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) != 0:
        elbow = detector.findAngle(img, 11, 13, 15)
        shoulder = detector.findAngle(img, 13, 11, 23)
        hip = detector.findAngle(img, 11, 23,25)
        
        #Percentage of success of pushup
        per = np.interp(elbow, (90, 160), (0, 100))
        
        #Bar to show Pushup progress
        bar = np.interp(elbow, (90, 160), (380, 50))

        current_time = time.time()
        time_interval = current_time - prev_time
        angle_change = elbow - prev_elbow_angle
        elbow_speed = abs(angle_change / time_interval)
      
        # 속도에 따른 음성 메시지 생성
        if elbow_speed < slow_threshold:
            feedback = "SLOW"
        elif elbow_speed > fast_threshold:
            feedback = "FAST"
        else:
            feedback = "GOOD"

        # TTS로 음성 출력
        #speak(feedback)

        # 현재 값을 이전 값으로 업데이트
        prev_elbow_angle = elbow
        prev_time = current_time

        #Check to ensure right form before starting the program
        if elbow > 160 and shoulder > 40 and hip > 160:
            form = 1
    
        #Check for full range of motion for the pushup
        if form == 1:
            if per == 0:
                if elbow <= 90 and hip > 160:
                    feedback = "Up"
                    if direction == 0:
                        count += 0.5
                        direction = 1

                        # 추가한 코드
                        if 1 <= count <= 10 and str(count)[-1] == '0': # count가 1 이상 10 이하이고, 소수점의 마지막이 0이면
                            index = int(count) - 1
                            if spoken_numbers[index] == False:
                                speak(str(int(count)))
                                spoken_numbers[index] = True
                else:
                    feedback = "Fix Form"
                    
            if per == 100:
                if elbow > 160 and shoulder > 40 and hip > 160:
                    feedback = "Down"
                    if direction == 1:
                        count += 0.5
                        direction = 0

                        # 추가한 코드
                        if 1 <= count <= 10 and str(count)[-1] == '0': # count가 1 이상 10 이하이고, 소수점의 마지막이 0이면
                            index = int(count) - 1
                            if spoken_numbers[index] == False:
                                speak(str(int(count)))
                                spoken_numbers[index] = True
                else:
                    feedback = "Fix Form"
                        # form = 0
                

        print(count)
        

        #Draw Bar
        #if form == 1:
        if 1 == 1:
            cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 0, 0), 2)


        #Pushup counter
        cv2.rectangle(img, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5,
                    (255, 0, 0), 5)
        
        #Feedback 
        cv2.rectangle(img, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2,
                    (0, 255, 0), 2)

        
    cv2.imshow(window_name, img)

    if cv2.waitKey(10) & 0xFF == ord('m'): # 카메라 반전
        mirror = not mirror

    if cv2.waitKey(10) & 0xFF == ord('r'): # 카운트 초기화
        count = 0
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()