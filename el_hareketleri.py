import cv2
import mediapipe as mp
import time

camera = cv2.VideoCapture(0)
camera.set(3, 640)
camera.set(4, 480)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

mp_drawing = mp.solutions.drawing_utils

pos_x, pos_y = 0, 0
pTime = 0


def fps(img):
    cTime = time.time()
    global pTime
    fps_ = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps_)}", (480, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

def print_on_frame(text):
    cv2.putText(frame, text, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


while True:
    _, frame = camera.read()
    fps(frame)

    if not _:
        print("Webcam error !")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            check_thumbs_up = False

            for finger_num, landmark in enumerate(hand_landmarks.landmark):

                position_x, position_y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])

                if finger_num > 4 and landmark.y < hand_landmarks.landmark[2].y:
                    break

                elif finger_num == 20 and landmark.y > hand_landmarks.landmark[2].y:
                    check_thumbs_up = True

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            x, y = int(index_finger_tip.x * frame.shape[1]), int(index_finger_tip.y * frame.shape[0])

            dx = x - pos_x
            dy = y - pos_y

            if check_thumbs_up:
                print_on_frame("THUMBS UP")

            else:
                if dx > 20:
                    print_on_frame("LEFT")
                elif dx < -20:
                    print_on_frame("RIGHT")
                elif dy > 20:
                    print_on_frame("DOWN")
                elif dy < -20:
                    print_on_frame("UP")

            pos_x, pos_y = x, y

    else:
        print_on_frame("NO HAND DETECTED")

    cv2.imshow("WEBCAM", frame)
    if cv2.waitKey(1) == 27:
        break

camera.release()
cv2.destroyAllWindows()
