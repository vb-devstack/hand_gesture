import cv2
import mediapipe as mp
import pycaw.pycaw as pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Volume control setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()
min_vol = vol_range[0]
max_vol = vol_range[1]

# State variables
gesture_sequence = []
volume_control_mode = False
current_volume = 0.0

# Define a simple gesture classifier
def classify_gesture(hand_landmarks):
    fingertips_ids = [4, 8, 12, 16, 20]
    extended_fingers = 0
    wrist_y = hand_landmarks.landmark[0].y

    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        extended_fingers += 1

    for tip_id in [8, 12, 16, 20]:
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
            extended_fingers += 1

    if extended_fingers == 2:
        return "V"
    elif extended_fingers == 5:
        return "O"
    elif extended_fingers == 0:
        return "Fist"
    else:
        return f"{extended_fingers} fingers"

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label
            gesture = classify_gesture(hand_landmarks)

            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = image.shape
            cx = int(hand_landmarks.landmark[0].x * w)
            cy = int(hand_landmarks.landmark[0].y * h)

            cv2.putText(image, f"{label} Hand: {gesture}", (cx - 50, cy - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Update gesture sequence
            if gesture in ["V", "O"]:
                if len(gesture_sequence) == 0 or gesture != gesture_sequence[-1]:
                    gesture_sequence.append(gesture)
                    if len(gesture_sequence) > 2:
                        gesture_sequence.pop(0)

            # Toggle volume mode
            if gesture_sequence == ["V", "O"]:
                volume_control_mode = not volume_control_mode
                gesture_sequence = []

            # Volume control logic
            if volume_control_mode and label == "Right":
                thumb_tip = hand_landmarks.landmark[4]
                index_tip = hand_landmarks.landmark[8]

                x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
                x2, y2 = int(index_tip.x * w), int(index_tip.y * h)
                length = np.hypot(x2 - x1, y2 - y1)

                vol = np.interp(length, [30, 200], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol, None)

                # Update current volume level for visual bar
                current_volume = np.interp(length, [30, 200], [0, 100])

                cv2.putText(image, f"Volume Mode: ON ({int(length)} px)", (10, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    if not volume_control_mode:
        cv2.putText(image, "Volume Mode: OFF", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 0, 0), 2)

    # Draw visual volume bar
    bar_height = int(np.interp(current_volume, [0, 100], [400, 100]))
    cv2.rectangle(image, (50, 100), (85, 400), (0, 0, 0), 2)
    cv2.rectangle(image, (50, bar_height), (85, 400), (0, 255, 0), -1)
    cv2.putText(image, f'{int(current_volume)} %', (50, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Hand Gesture Recognition', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
