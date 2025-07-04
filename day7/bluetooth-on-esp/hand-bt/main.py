import cv2
import mediapipe as mp
import serial

# Serial setup
ser = serial.Serial("/dev/rfcomm0", 115200, timeout=1)

# MediaPipe setup
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

def count_fingers(landmarks):
    # Finger tip and pip landmarks
    tips = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
    pips = [3, 6, 10, 14, 18]
    
    count = 0
    for tip, pip in zip(tips, pips):
        if landmarks[tip].y < landmarks[pip].y:  # finger is up
            count += 1
    return count

cap = cv2.VideoCapture(0)
last_state = None

while True:
    ret, frame = cap.read()
    if not ret: continue
    
    frame = cv2.flip(frame, 1)
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    
    state = "off"
    if results.multi_hand_landmarks:
        fingers = count_fingers(results.multi_hand_landmarks[0].landmark)
        if fingers >= 3:  # 3 or more fingers = ON
            state = "on"
    
    if state != last_state:
        ser.write((state + "\n").encode())
        print(f"Sent: {state}")
        last_state = state
    
    cv2.putText(frame, f"LED: {state.upper()}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("Finger Counter", frame)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
