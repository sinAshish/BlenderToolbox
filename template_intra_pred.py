import blendertoolbox as bt
import sys
import bpy
import os
import numpy as np

cwd = os.getcwd()
# from bpy import Vector
# outputPath = os.path.join(cwd, './template.png')

## initialize blender
imgRes_x = 512  # recommend > 1080
imgRes_y = 512  # recommend > 1080
numSamples = 100  # recommend > 200
exposure = 1.5
use_GPU = True
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure, use_GPU)

## read mesh
# meshPath = './meshes/spot.ply'
mesh_path = sys.argv[-2]
from pathlib import Path

model_name = Path(mesh_path).parent.stem
mesh_name = Path(mesh_path).stem
mesh_res = mesh_name.split("_pred_")[-1].split("_")[0]
n_blocks, dim = list(map(int, model_name.split("_")[-1].split("x")))
save_path = Path(f"/local-scratch2/asa409/data/INR_paper_plots/{model_name}")
save_path.mkdir(parents=True, exist_ok=True)
mesh_name = mesh_name.split("_pred_")[0]
save_name = save_path / (mesh_name + f"_{sys.argv[-1]}.png")
meshPath = str(mesh_path)
outputPath = str(save_name)

# mesh_res = mesh_path.split("/")[-1].split("_")[-1].split(".")[0]
if "64" in mesh_res:
    location = (0.94, 0.0134, 1.1122)
    scale = (0.0004, 0.0004, 0.0004)
elif "32" in mesh_res:
    location = (0.49, 0.0134, 0.8322)
    scale = (0.0015, 0.0015, 0.0015)
elif "128" in mesh_res:
    # location = (0.94, 0.0134, 0.9122)  # pred complete
    location = (0.44, -0.0066, 0.8722)
    scale = (0.0001, 0.0001, 0.0001)  # pred complete
elif "256" in mesh_res:
    location = (1.2, 0.01, 1.18)
    scale = (0.00002, 0.00002, 0.00002)
elif "512" in mesh_res:
    sys.exit(0)
    location = (1.2, 0.01, 1.18)
    scale = (0.000001, 0.000001, 0.000001)
# location = (0.5, 0.5, 0.5)
# rotation = (90, 0, 180) # (GUI: click mesh > Transform > Rotation)
rotation = (0, 0, 90)  # complete
# scale = (0.0001, 0.0001, 0.0001) # pred complete
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth()  # Option1: Gouraud shading
# bpy.ops.object.shade_flat() # Option2: Flat shading
# bt.edgeNormals(mesh, angle = 10) # Option3: Edge normal shading

## subdivision
bt.subdivision(mesh, level=1)

###########################################
## Set your material here (see other demo scripts)

# bt.colorObj(RGBA, Hue, Saturation, Value, Bright, Contrast)
# n_blocks = int(str(sys.argv[-1]).split("x")[0])
# dim = int(str(sys.argv[-1]).split("x")[1])
if n_blocks == 5:
    RGBA = bt.coralRed
elif n_blocks == 1:
    RGBA = bt.cb_green
elif n_blocks == 3:
    RGBA = bt.cb_skyBlue
else:
    RGBA = bt.live_opal
# if n_blocks == 5 and (dim == 128):
#     RGBA = bt.coralRed
# elif n_blocks == 5 and (dim == 256):
#     RGBA = bt.caltechOrange
# elif n_blocks == 5 and (dim == 512):
#     RGBA = bt.aqua_blue
# elif n_blocks == 5 and (dim == 64):
#     RGBA = bt.royalYellow
# elif n_blocks == 1 and (dim == 64):
#     RGBA = bt.cb_orange
# elif n_blocks == 1 and (dim == 128):
#     RGBA = bt.cb_skyBlue
# elif n_blocks == 1 and (dim == 256):
#     RGBA = bt.cb_green
# elif n_blocks == 1 and (dim == 512):
#     RGBA = bt.cb_yellow
# elif n_blocks == 3 and (dim == 64):
#     RGBA = bt.cb_vermillion
# elif n_blocks == 3 and (dim == 128):
#     RGBA = bt.barbie_pink
# elif n_blocks == 3 and (dim == 256):
#     # RGBA = tuple(np.array(bt.cb_skyBlue) * 0.5 + np.array(bt.cb_Orange) * 0.5)
#     RGBA = bt.live_opal
# elif n_blocks == 3 and (dim == 512):
#     # RGBA = tuple(np.array(bt.cb_green) * 0.5 + np.array(bt.cb_yellow) * 0.5)
#     RGBA = (159 / 255.0, 1 / 255.0, 98 / 255.0, 1)
# else:
#     RGBA = bt.royalBlue
meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## End material
###########################################

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera
## Option 1: don't change camera setting, change the mesh location above instead
camLocation = (3, 0, 2.5)
lookAtLocation = (0, 0, 0.5)
focalLength = 45  # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)
## Option 2: if you really want to set camera based on the values in GUI, then
# camLocation = (3, 0, 2)
# rotation_euler = (63,0,90)
# focalLength = 45
# cam = bt.setCamera_from_UI(camLocation, rotation_euler, focalLength = 35)

## set light
## Option1: Three Point Light System
# bt.setLight_threePoints(radius=4, height=10, intensity=1700, softness=6, keyLoc='left')
## Option2: simple sun light
lightAngle = (6, -30, -155)
strength = 2
shadowSoftness = 0.3
sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
bt.setLight_ambient(color=(0.1, 0.1, 0.1, 1))

## set gray shadow to completely white with a threshold (optional but recommended)
bt.shadowThreshold(alphaThreshold=0.05, interpolationMode="CARDINAL")

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + "/test.blend")

## save rendering
bt.renderImage(outputPath, cam)
