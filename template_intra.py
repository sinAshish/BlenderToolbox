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

location = (-2.39, -6.0766, 5.4022)
location = (1.17, -1.8766, 5.6922)
location = (0.67, 0.0234, 1.2322)  # complete
# location = (0.5, 0.5, 0.5)
# rotation = (90, 0, 180) # (GUI: click mesh > Transform > Rotation)
rotation = (0, 0, 90)  # complete
scale = (0.08, 0.08, 0.07)  # (GUI: click mesh > Transform > Scale)
scale = (0.01, 0.01, 0.01)  # complete
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
RGBA = (144.0 / 255, 210.0 / 255, 236.0 / 255, 1)
# RGBA = bt.iglGreen if "fixed" in sys.argv[-1] else bt.derekBlue

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
