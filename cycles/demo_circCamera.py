import sys
sys.path.append('/Users/hsuehtil/Dropbox/BlenderToolbox/cycles')
sys.path.append('/home/hsuehtil/Dropbox/BlenderToolbox/cycles')
from include import *
import bpy

outputFolder = './results/demo_circCamera/'

# # init blender
imgRes_x = 720 
imgRes_y = 720 
numSamples = 50 
exposure = 1.0
blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

# read mesh 
meshPath = '../meshes/spot.ply'
location = (-0.3, 0.6, -0.04)
rotation = (90, 0,0)
scale = (1.5,1.5,1.5)
mesh = readPLY(meshPath, location, rotation, scale)

# # set shading
bpy.ops.object.shade_smooth()
# bpy.ops.object.shade_flat()

# # subdivision
level = 2
subdivision(mesh, level)

# # set material
# colorObj(RGBA, H, S, V, Bright, Contrast)
meshColor = colorObj(derekBlue, 0.5, 1.0, 1.0, 0.0, 2.0)
AOStrength = 0.5
setMat_singleColor(mesh, meshColor, AOStrength)

# # set invisible plane (shadow catcher)
groundCenter = (0,0,0)
shadowDarkeness = 0.7
groundSize = 20
invisibleGround(groundCenter, groundSize, shadowDarkeness)

# # set camera path
R = 3 # radius of the circle camera path
H = 2 # height of the circle camera path
lookAtPos = (0,0,0.5) # look at position
startAngle = 0 # camera starting angle from positive x-axis
focalLength = 45
duration = 10 # number of frames in total for 360 degrees
cam = setCameraPath(R, H, lookAtPos, focalLength,duration,startAngle)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 2
shadowSoftness = 0.1
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.2,0.2,0.2,1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # rendering
renderAnimation(outputFolder, cam, duration)