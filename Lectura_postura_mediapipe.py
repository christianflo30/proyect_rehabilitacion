import cv2
import mediapipe as mp 
import math
import sys 

if len(sys.argv) != 3:
    print("python usando lectura de postura")
    sys.exit(1)


angulo_semi_circulo_inter = int(sys.argv[1])
Repeticiones_inter =int(sys.argv[2])
mp_drawing = mp.solutions.drawing_utils 
mp_pose = mp.solutions.pose 

cap= cv2.VideoCapture(0,cv2.CAP_DSHOW)

LEFT_HIP = 23
LEFT_KNEE = 25
LEFT_ANKLE = 27

RIGHT_HIP = 24
RIGHT_KNEE = 26
RIGHT_ANKLE = 28

angulo_semi_circulo = angulo_semi_circulo_inter
left_inside_cont = 0
right_inside_cont =0
left_inside_final = False
right_inside_final =False

Repeticiones = Repeticiones_inter


# def calcular_angulo(A,B,C):
#     radianes = math.atan2(C[1]-B[1],C[0]-B[0])-math.atan2(A[1]-B[1],A[0]-B[0]) 
#     angulo = math.degrees(abs(radianes))
#     return angulo
# def caluclar_distancia(punto_1,punto_2):
#     return math.sqrt((punto_1[0]-punto_2[0])**2 + (punto_1[1]-punto_2[1])**2)
    

def dibujar_angulo_accion(frame,centro,radio,inicio_angulo,fin_angulo,color):
    axes = (int(radio),int(radio))
    thickness =2 
    cv2.ellipse(frame,centro,axes,0, inicio_angulo,fin_angulo,color,thickness)

def punto_dentro_area(centro,radio,inicio_angulo,fin_angulo,point):
    inicio_angulo_radianes = math.radians(inicio_angulo)
    fin_angulo_radianes = math.radians(fin_angulo)

    distancia = math.sqrt((point[0]-centro[0])**2 + (point[1]-centro[1])**2)
    angulo_punto = math.atan2(point[1]-centro[1], point[0]-centro[0])

    if angulo_punto < 0:
        angulo_punto += 360

    inicio_angulo %= 360
    fin_angulo %= 360
    

    # if inicio_angulo < fin_angulo:
    return distancia <=radio and inicio_angulo_radianes <= angulo_punto <=fin_angulo_radianes 
    # else:
    #     return distancia <=radio and (angulo_punto>=inicio_angulo or angulo_punto<= fin_angulo)
def conteo_repes(centro,radio,inicio_angulo,fin_angulo,point,inside_cont):
        distancia = math.sqrt((point[0]-centro[0])**2 + (point[1]-centro[1])**2)
        angulo_punto = math.degrees(math.atan2(point[1]-centro[1],point[0]-centro[0]))
        if angulo_punto < 0:
            angulo_punto += 360
        fin_angulo %= 360

        if distancia <= radio and abs(angulo_punto- fin_angulo)<5:
            if not inside_cont:
                inside_cont =True
                return True,inside_cont
        else:
            inside_cont = False
        return False,inside_cont

with mp_pose.Pose(static_image_mode=False) as pose:
    while True:
        ret, frame =cap.read()
        if ret == False:
            break
        frame= cv2.flip(frame,1)
        height,width,_=frame.shape
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results= pose.process(frame_rgb)

        if results.pose_landmarks is not None:
            landmarks = results.pose_landmarks.landmark
            # left_hip = (landmarks[LEFT_HIP].x*width,landmarks[LEFT_HIP].y*height)
            left_knee = (int(landmarks[LEFT_KNEE].x*width),int(landmarks[LEFT_KNEE].y*height))
            left_ankle = (int(landmarks[LEFT_ANKLE].x*width),int(landmarks[LEFT_ANKLE].y*height))

            # right_hip = (landmarks[RIGHT_HIP].x*width,landmarks[RIGHT_HIP].y*height)
            right_knee = (int(landmarks[RIGHT_KNEE].x*width),int(landmarks[RIGHT_KNEE].y*height))
            right_ankle = (int(landmarks[RIGHT_ANKLE].x*width),int(landmarks[RIGHT_ANKLE].y*height))
           
            radio_izq = math.sqrt((left_ankle[0]-left_knee[0])**2+(left_ankle[1]-left_knee[1])**2)
            radio_derecha = math.sqrt((right_ankle[0]-right_knee[0])**2+(right_ankle[1]-right_knee[1])**2)

            angulo_ideal_izq = (left_knee[0],left_knee[1]+int(radio_izq))
            angulo_ideal_dere = (right_knee[0],right_knee[1]+ int(radio_derecha))


            cv2.line(frame,left_knee,left_ankle,(255,0,0),2)
            cv2.line(frame,right_knee,right_ankle,(255,0,0),2)

            left_inside = punto_dentro_area(left_knee,radio_izq,0,angulo_semi_circulo,left_ankle)
            right_inside = punto_dentro_area(right_knee,radio_derecha,0,angulo_semi_circulo, right_ankle)

            left_color = (0,255,0) if left_inside else (0,0,255)
            right_color = (0,255,0) if right_inside else (0,0,255)
            # conteo

            left_inside_ver, left_inside_final = conteo_repes(left_knee,radio_izq,0,angulo_semi_circulo,left_ankle,left_inside_final)
            right_inside_ver, right_inside_final = conteo_repes(right_knee,radio_derecha,0,angulo_semi_circulo,right_ankle,right_inside_final)
            if left_inside_ver == True:
                left_inside_cont += 1
            if right_inside_ver == True :
                right_inside_cont +=1
        
            cv2.putText(frame, f"Repeticiones_izq: {max(0,Repeticiones-left_inside_cont)}", (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, f"Repeticiones_der: {max(0,Repeticiones-right_inside_cont)}", (15, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # angulo_left = calcular_angulo(left_hip,left_knee,left_ankle)
            # angulo_right = calcular_angulo(right_hip,right_knee,right_ankle)

            # cv2.putText(frame,f"angulo izquierdo:{int(angulo_left)}",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            # cv2.putText(frame,f"angulo derecho:{int(angulo_right)}",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
            dibujar_angulo_accion(frame,left_knee,radio_izq,90,angulo_semi_circulo,left_color)
            dibujar_angulo_accion(frame,right_knee,radio_derecha,90,angulo_semi_circulo,right_color)

            mp_drawing.draw_landmarks(
                frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(128,0,250),thickness=2,circle_radius=2),
                mp_drawing.DrawingSpec(color=(255,255,255),thickness=2))
            
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) and 0xFF == 27:
            break
cap.release()
cv2.destroyAllWindows()
