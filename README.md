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
This assignment builds upon the code used in assignment 6 for random snake. However, for this assignment, everytime that a snake body is generated, I randomly selected whether that body part will have no arms, 1 arm, or 2 arms. If it decides to have no arm, it simply moves onto the next iteration. If it decides to have 1 arm, it also randomly select whether to grow an arm on the left side or the right side. If at least one arm is generated, I again randomly decide if the arm will grow a leg or not. If it decides to grow a leg, then I randomly choses a positive or negative z direction to which the leg will grow. Unfortunately, I ran out of time to implement the random foot generating portion. Therefore, my robot is currently only able to expland in 2 dimentions. I will certainly add this feature as well in the near future. The number of motors and sensors are kept in track throughout the generating process so that we can connect it to the brain. I also randomly select which sensors are not selected before I generate send_cube and mark those cubes with blue.
