# Senior Design 2

Team Lunar
------------

- Mohammad Abusalah
- Eric Nwagwu
- Showvik Das
- Sweekar Shrestha


Background Information
-----------------------
- This repository contains our Capstone project source code and relevant files for Senior Deign Project course (CSE-4317) at UTA offered by Dr. McMurrough.
- We were tasked with creating an interactive projection mapping software to improve the nightlife of downtown Arlington
- Our project projects a spatial video mapping projection onto a Cube - where each faces provide a unique projection presentation involving graphic design and computer vision games
- Each face of the Cube is detected by our software through AruCo Markers and for each unique face, the software will project a unique projection or an interactive OpenCV application.


Installation requirements
---------------------------
- Install opencv with aruco marker -> `pip3 install opencv-contrib-python`
- Allow Python camera usage from system preferences. 
- Modify opencv camera code if configured with multiple cameras
- Run command -> `python3 DetectArucoMarkers.py`
- Show aruco markers on the camera feed.
- The program should output the markerId (_of the shown aruco marker_) on the console
- REQUIRED - PYTHON 3.7, NEWER WILL NOT WORK


Current Limitations
---------------------
- We are currently using Spout to transfer over our OpenCV Script to Madmapper. However, due to spout only being available on Windows, this project only runs on Windows machine for now. An alternative to spout for macOS is Syphon which can be used for similar functionality. 
- As mentioned in installation requirements, currently only Python 3.7 will work with the project
