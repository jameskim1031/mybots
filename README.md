# Assignment 7

## How to test
You can run/ test the code using two ways
```
python search.py
```
or 
```
python button.py
```

## Documentation
This assignment builds upon the code used in assignment 6 for random snake. The main addition is that everytime that a snake body is generated, it randomly selects whether that body part will have no arms, 1 arm, or 2 arms. If it decides to have no arm, it simply moves onto the next iteration of body creation. If it decides to have 1 arm, it randomly select whether to grow an arm on the left side or the right side of the body. If at least one arm is generated, I randomly decide if the arm will grow a leg or not. If it decides to grow a leg, then I again randomly choses to grow the leg in the positive z or negative z direction. Unfortunately, I ran out of time to implement the last part. Therefore, my robot can only able to expland in 2 dimentions (x and y). I will certainly add this feature as well in the near future. The number of motors and sensors are kept in track throughout the generating process so that we can connect it to the brain. I also randomly select which sensors are not selected before I generate send_cube and mark those cubes with blue.

## Generating body & brain
The body is generated starting the from the head of the snake. The position of the first cube (the head) and its joint is absolute. For the body of the snake, I follow exactly what I did for assignment 6. However, the snake can choose to expand into a lizard by adding arms to its snake body. To do this, I first choose whether the snake will have arms, 1 arm, or 2 arms. For 1 arm, depending whether the snake is growing a left or right arm, I calculate the joint of the arm. Since the snake body grows along the x axis, the y coordinate is the only important. In my algorithm, it is important to bring the joint position back to the next snake body position as that variable will be used to create the next snake body. Although I wasn't able to implement it, adding the legs would work similarly. After choosing what direction I want the leg to grow, I would calculate the leg_joint position. Similar to the arm_joint position, only the y coordinate would be relevant. To be more precise, the leg_joint coordinate would simply be adding the arm_size and the leg_joint arrays. 

The brain is generated using 2 for loops. One for loop iterates over to create the sensor neurons, while the other to create the motor neurons. The number of iteration of the each for loop is determined by keeping track of the cubes and joints being sent to pyrosim. It is also important to exclude the cubes that we randomly decide to not include.

## Diagram to help understand generating the body
