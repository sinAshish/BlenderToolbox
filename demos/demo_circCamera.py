import blendertoolbox as bt
import bpy
import os, sys
import numpy as np
cwd = os.getcwd()

outputHeader = os.path.join(cwd, './demo_circCamera_') # make it abs path for windows

## initialize blender
imgRes_x = 512
imgRes_y = 512
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

mesh_path = sys.argv[-2]
from pathlib import Path
save_path = Path("/local-scratch2/asa409/data/INR_paper_plots/")
save_path.mkdir(parents=True, exist_ok=True)
save_name = save_path / (Path(mesh_path).stem + f"_{sys.argv[-1]}_circCam_")
meshPath = str(mesh_path)
outputPath = str(save_name)

## read mesh (choose either readPLY or readOBJ)
# meshPath = '../meshes/spot.ply'
location = (-0.01, -0.0166, 0.7822)
rotation = (90, 0, 0) # g1d4
scale = (0.00008, 0.00008, 0.00008) # g1d2
# location = (1.12, -0.14, 0) # (UI: click mesh > Transform > Location)
rotation = (90, 0, 0) # (UI: click mesh > Transform > Rotation)
# scale = (1.5,1.5,1.5) # (UI: click mesh > Transform > Scale)
mesh_res= mesh_path.split("/")[-1].split("_")[-1].split(".")[0]

if "64" in mesh_res:
    scale = (0.0004, 0.0004, 0.0004)
elif "32" in mesh_res:
    scale = (0.004, 0.004, 0.004)
elif "128" in mesh_res:
    scale = (0.0001, 0.0001, 0.0001) # pred complete
elif "256" in mesh_res:
    # location = (1.2, 0.01, 1.18)
    scale = (0.00002, 0.00002, 0.00002)
elif "512" in mesh_res:
    sys.exit(0)
    location = (1.2, 0.01, 1.18)
    scale = (0.000001, 0.000001, 0.000001)
mesh = bt.readMesh(meshPath, location, rotation, scale)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
bt.subdivision(mesh, level = 1)

n_blocks = int(str(sys.argv[-1]).split("x")[0])
dim = int(str(sys.argv[-1]).split("x")[1])
if n_blocks == 5 and (dim == 128 ):
    RGBA = bt.coralRed
elif n_blocks == 5 and (dim == 256 ):
    RGBA = bt.caltechOrange
elif n_blocks == 5 and (dim == 512 ):
    RGBA = bt.aqua_blue
elif n_blocks == 5 and (dim == 64 ):
    RGBA = bt.royalYellow
elif n_blocks == 1 and (dim == 64 ):
    RGBA = bt.cb_orange
elif n_blocks == 1 and (dim == 128 ):
    RGBA = bt.cb_skyBlue
elif n_blocks == 1 and (dim == 256 ):
    RGBA = bt.cb_green
elif n_blocks == 1 and (dim == 512 ):
    RGBA = bt.cb_yellow
elif n_blocks == 3 and (dim == 64 ):
    RGBA = bt.cb_vermillion
elif n_blocks == 3 and (dim == 128 ):
    RGBA = bt.barbie_pink
elif n_blocks == 3 and (dim == 256 ):
    # RGBA = tuple(np.array(bt.cb_skyBlue) * 0.5 + np.array(bt.cb_Orange) * 0.5)
    RGBA = bt.live_opal
elif n_blocks == 3 and (dim == 512):
    # RGBA = tuple(np.array(bt.cb_green) * 0.5 + np.array(bt.cb_yellow) * 0.5)
    RGBA = (159/255., 1/255.0, 98/255., 1)
else:
    RGBA = bt.royalBlue
    # RGBA = tuple(np.array(bt.white) * 0.5 + np.array(bt.cb_black) * 0.5)
# # set material
# colorObj(RGBA, H, S, V, Bright, Contrast)
# RGBA = (144.0/255, 210.0/255, 236.0/255, 1)
meshColor = bt.colorObj(RGBA, 0.5, 1.0, 1.0, 0.0, 2.0)
bt.setMat_plastic(mesh, meshColor)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera 
R = 3 # radius of the circle camera path
H = 2 # height of the circle camera path
lookAtPos = (0,0,0.5) # look at position
startAngle = 0 # camera starting angle from positive x-axis
focalLength = 45
duration = 5 # number of frames in total for 360 degrees
cam = bt.setCameraPath(R, H, lookAtPos, focalLength,duration,startAngle)

## set light
lightAngle = (6, -30, -155) 
strength = 2
shadowSoftness = 0.3
sun = bt.setLight_sun(lightAngle, strength, shadowSoftness)

## set ambient light
bt.setLight_ambient(color=(0.1,0.1,0.1,1)) 

## set gray shadow to completely white with a threshold 
bt.shadowThreshold(alphaThreshold = 0.05, interpolationMode = 'CARDINAL')

## save blender file so that you can adjust parameters in the UI
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test_circ.blend')

## save rendering
bt.renderAnimation(outputPath, cam, duration)
