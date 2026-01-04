from CSVReader import Reader 
import Objects
import Physics
import time
Filepath = r"C:\Users\seege\Desktop\Uni\Informatik\ProjectV2\planets_moons_and_more.csv"
TestFilepath = r"C:\Users\seege\Desktop\Uni\Informatik\ProjectV2\test.csv"

R = Reader()
a = R.ReadCSVToObjectContainer(Filepath=Filepath)

Physics.compute_system_accelerations(a.pos,a.mass,a.acc)


starttime = time.time()
for i in range(101):
    Physics.verlet_step(a.pos,a.vel,a.mass,a.acc,1)
endtime = time.time()

time = endtime-starttime
b=2