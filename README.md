# Assignment 8

## How to test
You can run/ test the code using two ways
```
python search.py
```
or 
```
python button.py
```

## Summary
This assignment builds upon the code used in assignment 7 for generating 3D object. While most of the functions are similar to that of assignment 7, the new assignment allows the robot to evolve itself to optimize the fitness function. It does so through 3 new features. First, a newly created LinkedList class keep track of all information necessary to regenerate the robot. This is important so that we can modify and recreate the evolved robot. Second, the robot is able to evolve by identifying which body parts can be evolved. A simple array list keeps track of body that doesn't have either arm or an arm that doesn't have a leg. Each time the robot evolves, it randomly chooses from this list. Third, the robot is able to add the information of the new body part into the LinkedList. It would also need to make sure to increment the number of all the bodyID after the added LinkedList. The robot is then evovled with a new body part.

## Generating body & brain
I made a major improvement compared to assignment 7 in generating the body and the brain. I implemented a class called Body. This body represent each body of a snake. Inside a Body, I randomly determine how many arms I am planning to have for the Body. If I plan to have at least 1 arm for the Body, I also determine whether I will have no legs, a leg going up or leg going down. Essentially, each time the Body is called, the snake is added either just another body part, arms to become a lizard, or arms and legs to become a horse.

## The evolution
The robot is able to evolve by adding arms and legs to parts it previously didn't have. This is done through a LinkedList. Each time a creature is generated through the steps above, I also keep track of the various dimensions of each Body using a LinkedList. I keep track of the body_size, body_position, joint_position, bodyID, and the parent's ID. I keep track of these 5 variables as these are the only variables that I need to generate an exisiting creature. In addition, as I generate the body, I also keep track of the body blocks that didn't generate arms, or arm blocks that didn't generate legs. This is because these are the potential parts that I could evolve. Once all the parts are added to the LinkedList, I randomly selected a body part to evolve from the list. Then, I traverse through the LinkedList until I find the block that I need to attach the new part onto. Once the joint and the cube is sent to the pyrosim, I make sure to increment the rest of the LinkedList bodyID and parentID so that the synpases doesn't run into an error. Once the new part is added, I can regenerate the original creature with the added body part.

### Important functions:
LinkedList.add() --> creates a new link with the 5 variables
LinkedList.insert() --> adds a new body part in the correct position of the LinkedList
LinkedList.increment_all_joints() --> increments the rest of the links bodyID and parentIDs by 1 to compensate for the new link
LinkedList.Generate_Body_Using_LinkedList() --> generates the creature again but with the evolved body part


## Diagram to help understand generating the body
![327116947_710009484191220_2222516642722844365_n](https://user-images.githubusercontent.com/95663596/220276949-3c9fa871-0d03-45a0-91b7-bf047603e6f1.jpg)
This diagram shows in high level how the snake body, arms, and legs are generated. The body grows along the x axis; the arm grows along the y axis; the leg grows along the z axis
![327156150_736364211532701_4357122538420378307_n](https://user-images.githubusercontent.com/95663596/220276936-da5e378a-6b6b-4565-a5b5-67ba5c69a142.jpg)
This diagram shows how the joint and cube positions are determined for different body part. The snake body's cube position is always relative to the previous joint position. The arm's position is relative to the arm's joint position which is located in the edge of the body and the arm. The leg's position is relative to the leg's join position which is located at the very end of the arm.

## Diagram to help understand the evolution
![332639803_1448823769260910_8622236998661453762_n](https://user-images.githubusercontent.com/95663596/221785974-1c448c93-1e35-4c8e-be36-f84877d11ec9.jpg)
