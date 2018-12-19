import sys
sys.path.append('/Users/Hsueh-Ti/Dropbox/BlenderToolbox')

from include import *
import bpy

outputPath = './results/demo_iglGreen.png'

# # init blender
imgRes_x = 1000
imgRes_y = 1000 
numSamples = 1000 # should set it to perhaps 2000 for high quality paper images
blenderInit(imgRes_x, imgRes_y, numSamples)

# # read mesh 
meshPath = './meshes/spot.ply'
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

# set material (option2: normal mode)
saturation = 1.3
meshColor = iglGreen
brightness = 1.0
setMat_normal(mesh, saturation, brightness, meshColor)

# # set invisible plane
groundCenter = (0,0,0)
groundSize = 5
invisibleGround(groundCenter, groundSize)

# # ambient occlusion
AOStrength = 1.0
ambientOcclusion(AOStrength)

# # set camera
camLocation = (1.9,2,2.2)
lookAtLocation = (0,0,0.5)
focalLength = 45
cam = setCamera(camLocation, lookAtLocation, focalLength)

# # set sunlight
lightAngle = (-15,-34,-155) 
strength = 4
shadowSoftness = 0.05
sun = setLight_sun(lightAngle, strength, shadowSoftness)

# # set ambient light
ambientColor = (0.1,0.1,0.1)
setLight_ambient(ambientColor)

# # save blender file
bpy.ops.wm.save_mainfile(filepath='./test.blend')

# # save rendering
bpy.data.scenes['Scene'].render.filepath = outputPath
bpy.data.scenes['Scene'].camera = cam
bpy.ops.render.render(write_still = True)