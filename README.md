# Senior Design 2

Team Lunar
------------
![LunarLogo (1)](https://user-images.githubusercontent.com/67570641/160968812-b9a223ba-cee6-48a2-b9b7-40acf1144df5.png)
- Mohammad Abusalah
- Eric Nwagwu
- Showvik Das
- Sunil Pandey
- Sweekar Shrestha


Background Information
-----------------------
- This repository contains our Capstone project source code and relevant files for Senior Deign course (CSE-4317) at UTA offered by Dr. McMurrough.
- We were tasked with creating an interactive projection mapping software to improve the nightlife of downtown Arlington
- Our software allows for a spatial video mapping projection onto a Cube - where each faces provide a unique projection presentation involving graphic design and computer vision games
- Each face of the Cube is detected by our software through AruCo Markers and for each unique face, the software will project a unique projection or an interactive OpenCV application.


Python and OpenCV Installation requirements
---------------------------
- Install opencv with aruco markers -> `pip3 install opencv-contrib-python`
- Install native opencv -> `pip3 install opencv-python`
- Install numpy -> `pip3 install numpy`
- Allow Python camera usage from system preferences. 
- Modify opencv camera code if configured with multiple cameras
- REQUIRED - PYTHON 3.7, NEWER WILL NOT WORK


Madmapper and Spout Installation requirements
----------------------------------------------
_will be added soon_


Current Limitations
---------------------
- We are currently using Spout to transfer over our OpenCV Script to Madmapper. However, due to spout only being available on Windows, this project only runs on Windows machine for now. An alternative to spout for macOS is Syphon which can be used for similar functionality. 
- As mentioned in installation requirements, currently only Python 3.7 will work with the project
