

# Hand Gesture Control — Advanced OpenCV Project


## About This Project

Welcome to my **first advanced OpenCV project!**  
This repository demonstrates how to build a real-time hand gesture recognition system using **MediaPipe**, **OpenCV**, and **Pycaw** to control your computer’s volume with intuitive hand signals.

It was a fun and challenging learning experience that pushed me to explore:

- Real-time computer vision techniques  
- Gesture recognition and classification  
- System-level audio control via Python  
- Visual feedback and interactive UI design  

I’m excited to share it here and continue improving it with new features and capabilities.

---

## Features

- **Multi-hand detection**: Recognizes both left and right hands simultaneously.  
- **Gesture-based volume control**:  
  - Toggle volume control mode with a “V” + “O” finger sequence.  
  - Adjust system volume by pinching thumb and index finger in volume mode.  
- **Visual overlays**:  
  - Real-time hand landmarks and gesture labels.  
  - Dynamic volume bar showing current volume percentage.  
- Easily extensible for more gestures and controls.

---

## Getting Started

### Prerequisites

- Windows OS (for Pycaw audio control)  
- Python 3.8 or higher

### Install Dependencies

Open your terminal or command prompt and run:

```bash
pip install opencv-python mediapipe comtypes pycaw numpy
```

---

## Usage

Run the Python script:

```bash
python hand_gesture_control.py
```

### How to Use

- Perform the **“V” then “O”** gesture sequence with your right hand to toggle volume control mode.  
- In volume mode, move your thumb and index finger closer or farther apart to decrease or increase volume.  
- Press **`q`** to quit the application.

---

## Screenshots

![image](https://github.com/user-attachments/assets/8bec3dd7-ba0b-4305-bcb7-2d859ab310a3)


---

## Roadmap & Future Enhancements

- Mute/unmute toggle with fist gesture  
- Media playback controls (play, pause, skip)  
- Brightness adjustment using left-hand gestures  
- Gesture-triggered app launcher and screenshot capture  
- Cross-platform support beyond Windows  

---

## Contributing

I welcome contributions, bug reports, and feature requests.  
Feel free to fork the repo and submit pull requests!

---

## License

This project is licensed under the MIT License — see the LICENSE file for details.

---

## Acknowledgements

- [MediaPipe](https://mediapipe.dev/) for powerful hand tracking  
- [OpenCV](https://opencv.org/) for computer vision tools  
- [PyCAW](https://github.com/AndreMiras/pycaw) for audio control on Windows  

---

Thank you for checking out my project!  
I’m excited to keep learning and improving with the OpenCV and Python community.
