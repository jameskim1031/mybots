import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("box.sdf")

for i in range(5):
    for j in range(5):
        for k in range(10):
            pyrosim.Send_Cube(name="Box", pos=[i,j,0.5 + k] , size=[(1 * (0.9 ** k)),(1 * (0.9 ** k)),(1 * (0.9 ** k))])

pyrosim.End()