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
save_path = Path(f"/local-scratch2/asa409/data/INR_paper_plots/{model_name}")
save_path.mkdir(parents=True, exist_ok=True)
save_name = save_path / (mesh_name + f"_{sys.argv[-1]}.png")
meshPath = str(mesh_path)
outputPath = str(save_name)

# save_path = Path("/local-scratch2/asa409/data/INR_paper_plots/")
# save_path.mkdir(parents=True, exist_ok=True)
# save_name = save_path / (Path(mesh_path).stem + f"_{sys.argv[-1]}.png")
# meshPath = str(mesh_path)
# outputPath = str(save_name)

# location = (1.12, -0.14, 0) # (GUI: click mesh > Transform > Location)
location = (2.4539, -1.2489, 0)  # g1d1
location = (-1.1361, 1.2211, 0.09)  # g1d1
location = (1.0012, 0.4781, 0.8253)  # g1d2
location = (0.4112, 0.5181, 0.5553)  # g1d3
# location = (1.0012, -0.54605, 0.82924) # g1d3
# location = (0.8811, 0.57395, 0.76924) # g1d4

# location = (0.5, 0.5, 0.5)
# rotation = (90, 0, 180) # (GUI: click mesh > Transform > Rotation)
rotation = (90, 0, 0)  # g1d4
# scale = (1.5,1.5,1.5) # (GUI: click mesh > Transform > Scale)
scale = (0.03, 0.03, 0.03)  # g1d1
scale = (0.01, 0.01, 0.01)  # g1d2
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
RGBA = bt.derekBlue  # (144.0/255, 210.0/255, 236.0/255, 1)
meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## End material
###########################################

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera
## Option 1: don't change camera setting, change the mesh location above instead
camLocation = (3, 0, 2)
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
