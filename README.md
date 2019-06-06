# Hand_Exoskeleton
3d printed wearable variable stiffness exoskeleton for hand

Video Link: https://youtu.be/ZS-GP4a4qsU

1. Install ROS kinetic - follow steps from: http://wiki.ros.org/kinetic/Installation/Ubuntu
2. Create a catkin workspace - follow steps from: http://wiki.ros.org/catkin/Tutorials/create_a_workspace
3. Prepare the repository
   
   Gitclone the repository to the created workspace
   ```bash
   $ cd ~/handexo_ws
   ```
   ```bash
   $ git clone https://github.com/isparekh/Hand_Exoskeleton.git
   ```
   Compile handexo_ws
   ```bash
   $ cd ~/handexo_ws
   ```
   ```bash
   $ catkin_make 
   ```
   
   ## Running the system
   
   Execute following steps to control the dynamixel motors:
   
   1. Run roscore in a terminal 

   ```bash
   $ roscore
   ```
   
   2. Open a new terminal and run the launch file to scan how many and which dynamixels are connected
   
    ```bash
   $ cd ~/handexo_ws
   ```
  
    ```bash
   $ roslaunch dynamixel_tutorials controller_manager.launch
   ```
   
   3. Open a new terminal and run the launch file to start dynamixel motors and control them
   
   ```bash
   $ cd ~/handexo_ws
   ```
   
   ```bash
   $ roslaunch dynamixel_tutorials controller_spawner.launch
   ```
   
   ## Executing the python file to control the exoskeleton using hand gestures
   
      Prerequisites
   
      1. Install OpenCV version 2
      2. Configure webcam to be detected by raspberry pi
      3. Import python libraries for dynamixel
      
  
   ```bash
   $ cd ~/Control_Using_Gestures
   ```
   
   ```bash
   $ python Ges_2.py
   ```
   
   
  
