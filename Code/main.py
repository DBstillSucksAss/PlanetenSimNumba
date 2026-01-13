from CSVReader import Reader 
import Objects
import Physics
import time
import pyvista as pv
import numpy as np
import Logging as lg

#print(pv.Report())
Filepath = r"C:\Users\seege\Desktop\Uni\Informatik\ProjectV2\planets_moons_and_more.csv"
TestFilepath = r"C:\Users\seege\Desktop\Uni\Informatik\ProjectV2\test.csv"

R = Reader()
a = R.ReadCSVToObjectContainer(Filepath=Filepath)

Physics.compute_system_accelerations(a.pos,a.mass,a.acc)

VIS_SCALE = 1.0 / 1.496e11  # meters → AU

points = pv.PolyData(a.pos * VIS_SCALE)  #refference, no copy
plotter = pv.Plotter()

#print("Any NaN:", np.isnan(a.pos).any())
#print("Any Inf:", np.isinf(a.pos).any())
#print("Min:", np.min(a.pos))
#print("Max:", np.max(a.pos))

plotter.set_background("black")
actor = plotter.add_points(
    points,
    color="red",
    point_size=10
)
plotter.add_axes()
plotter.add_bounding_box()


plotter.reset_camera()
plotter.reset_camera_clipping_range()
#print("Bounds:", points.bounds)
#print("Camera position:", plotter.camera_position)


#plotter.show(interactive_update=True,auto_close=False)
time.sleep(0.1)

MOVE_SPEED = 0.2

def move(dir_vec):
    cam = plotter.camera
    pos = np.array(cam.GetPosition())
    focal = np.array(cam.GetFocalPoint())

    cam.SetPosition(*(pos + MOVE_SPEED * dir_vec))
    cam.SetFocalPoint(*(focal + MOVE_SPEED * dir_vec))

def forward():
    cam = plotter.camera
    move(np.array(cam.GetDirectionOfProjection()))

def backward():
    cam = plotter.camera
    move(-np.array(cam.GetDirectionOfProjection()))

def right():
    cam = plotter.camera
    dop = np.array(cam.GetDirectionOfProjection())
    up = np.array(cam.GetViewUp())
    right = np.cross(dop, up)
    move(right / np.linalg.norm(right))

def left():
    cam = plotter.camera
    dop = np.array(cam.GetDirectionOfProjection())
    up = np.array(cam.GetViewUp())
    left = -np.cross(dop, up)
    move(left / np.linalg.norm(left))

def up():
    cam = plotter.camera
    move(np.array(cam.GetViewUp()))

def down():
    cam = plotter.camera
    move(-np.array(cam.GetViewUp()))

plotter.add_key_event("w", forward)
plotter.add_key_event("s", backward)
plotter.add_key_event("a", left)
plotter.add_key_event("d", right)
plotter.add_key_event("q", down)
plotter.add_key_event("e", up)

for i in range(50):
    Physics.verlet_step(acc=a.acc, pos=a.pos, mass=a.mass, vel=a.vel, dt_days=1)
    lg.LogState(i,a,["ids","mass","pos","classes","names"],r"C:\Users\seege\Desktop\Uni\Informatik\ProjectV2\testLog.csv")
    print("step: "+ str(i))
    #points.points[:] = a.pos * VIS_SCALE
    
    #actor.GetMapper().GetInput().Modified()
    
    #plotter.update()
    #time.sleep(0.1)
