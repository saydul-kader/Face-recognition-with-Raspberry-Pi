# Face recognition with Raspberry Pi
This is a smart surveillance system with facial recognition capable of monitoring multiple camera premises in real time. Multiple Raspberry Pis are connected to an android app. The Pis keep a constant eye on the camera's surroundings. When a face is detected, the Raspberry Pi takes a picture of it and sends it to the Firebase Realtime Database along with the time of detection. The data is retrieved from Firebase and displayed in the Activity log by the app. In addition, whenever an unknown face is detected, the system sends the user an alert via email.
<br>The app provides the following features:
- Real time video streaming of multiple camera
- Activity log with detected face and time of detection
## Technology Used:
- Android
- Raspberry Pi
- Pi camera
- Python
- OpenCV
- Firebase Realtime Database
- SMTP
- Motion for Linux

## Device Overview:
<img src="https://user-images.githubusercontent.com/64978219/128914426-ccd41e65-5f2b-419d-9baa-088f8a0e246c.jpg" width="250" height="320">

## App Dashboard:
<img src="https://user-images.githubusercontent.com/64978219/128406332-9ffc2af7-b9b1-47e3-a1dd-50ff6c6f633e.jpg" width="250" height="400">

## Real time Video Streaming from Pi Camera:
<img src="https://user-images.githubusercontent.com/64978219/128406913-edcc863c-559d-4554-86d1-6dd7b9301d8b.png" width="250" height="400">

## Activity Log:
<img src="https://user-images.githubusercontent.com/64978219/128407113-a99f78e7-02ce-46a9-92d2-81b1515f6ae0.png" width="250" height="400"> <img src="https://user-images.githubusercontent.com/64978219/128407188-8eb8bd08-2e27-4c4a-b7ac-3d3d2e6481f9.png" width="250" height="400">


Upcoming Feature:
- Alert notification
