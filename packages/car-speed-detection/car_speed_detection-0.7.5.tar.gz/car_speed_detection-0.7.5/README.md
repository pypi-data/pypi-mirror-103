# Car-Speed-Detection
## 1.0 Description of Problem:

The rise of Tesla makes vehicle manufacturers realized that EV (Electronic Vehicle) with Autonomous Driving is the future of the car industry. Now, many vehicle manufacturers have the same plan, transforming the car into an autonomous EV. There are 2 camps from cost post of view. First, Waymo from Google is using a high-cost lidar, and second, Mobileye is using a low-cost camera. As the mature of AI technology and improvement of edge computing, our team believes that it’s possible to squeeze the power of dashboard camera by combining AI and powerful edge devices to achieve a similar performance of high-cost lidar solution. 

## 2.0 Proposed Solution:

Image Processing and AI are the keys to solve this problem. By using object recognition, the camera could recognize the static structural items like traffic lights, bus stops, or trees and we could then calculate the change of the distance between each frame to get the speed of the car. To recognize different objects in each frame, Machine Learning techniques like convolutional networks will be needed and implemented in this solution.


## 3.0 Market Analysis

The camera is the eye for the automobile. Being able to recognize the speed will increase the automobile’s awareness of its environment and allowed them to control the car fluently without putting the car driver in danger. Speed recognition used to be implemented with lidar, infrared sensing, and ultrasonic sensing, but the rise of image processing and Machine Learning allowed us to accomplish the same goal with simply a camera which could save more than $1000 per car, and therefore, save more than $92 billion per year for car producer.

## 4.0 Competitive Analysis

Our main competitive edges are price and efficiency. Without using expensive sensors like lidar, dual camera, infrared sensor and ultrasonic sensor that could cost more than $1000 each, people can simply use a cheap camera to easily detect car speed and possibly more scenarios like to follow the lane and to keep distance with front car frequently used in ADAS by using our library. By saving money and creating a new value for the low price camera, our library could create a win-win situation for the vehicle industry.

## 5.0 Team Members
Team Leader and Software Architecture: Shao-Chieh Lien 
Research Paper Writer: Meenakshi Pavithran 
Training Data Generator: Christopher Crocker 
