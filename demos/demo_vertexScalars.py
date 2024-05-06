import blendertoolbox as bt
import sys
import bpy
import os
import numpy as np
cwd = os.getcwd()

# outputPath = os.path.join(cwd, './demo_vertexScalars.png') # make it abs path for windows

mesh_path = sys.argv[-2]
from pathlib import Path
from uuid import uuid4 as uuid

hex_id = uuid().hex
model_name = Path(mesh_path).parent.stem
mesh_name = Path(mesh_path).stem
mesh_res = hex_id  # mesh_name.split("_pred_")[-1].split("_")[0]
# n_blocks, dim = list(map(int, model_name.split("_")[-1].split("x")))
mesh_name = f"{mesh_name}_{hex_id}"  # .split("_pred_")[0]
save_path = Path(f"/local-scratch2/asa409/data/INR_paper_plots/{model_name}")
save_path.mkdir(parents=True, exist_ok=True)
save_name = save_path / (mesh_name + f"_{sys.argv[-1]}.png")
meshPath = str(mesh_path)
outputPath = str(save_name)
import trimesh
import mesh2sdf

tri_mesh = trimesh.load(meshPath)
center = tri_mesh.bounding_box.centroid
length = tri_mesh.bounding_box.extents.max()
scale = 2.0 / length
tri_mesh.apply_translation(-center)
tri_mesh.apply_scale(scale)

V = np.array(tri_mesh.vertices, dtype=np.float32)
F = np.array(tri_mesh.faces, dtype=np.int32)
tri_mesh = trimesh.Trimesh(vertices=V, faces=F, process=False)
if not Path(mesh_path.replace(".ply", "_scaled.ply")).exists():
    _, tri_mesh = mesh2sdf.compute(V, F, 128, fix=True, level=2 / 128, return_mesh=True)
    # tri_mesh.export(meshPath.replace(".ply", "_scaled.ply"))
    tri_mesh.export(meshPath.replace(".ply", "_scaled.ply"))

def get_colormap_colors(scalars, colormap='viridis'):
    """
    Map scalar values to colors using a specified colormap.

    Parameters:
    - scalars: An array of scalar values.
    - colormap: A string representing the colormap to use.

    Returns:
    - colors: An array of RGBA colors corresponding to the scalar values.
    """

    # Normalize scalars to range [0, 1]
    norm = mcolors.Normalize(vmin=np.min(scalars), vmax=np.max(scalars))

    # Get the colormap
    cmap = plt.get_cmap(colormap)

    # Map normalized scalar values to colors
    colors = cmap(norm(scalars))

    return colors

## initialize blender
imgRes_x = 480 
imgRes_y = 480 
numSamples = 100 
exposure = 1.5 
bt.blenderInit(imgRes_x, imgRes_y, numSamples, exposure)

## read mesh from numpy array
location = (0,0,0.67)
rotation = (0,0,0) 
scale = (.5,.5,.5)
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
rotation = (90, 0, 0)  # g1d4
# mesh_res = mesh_path.split("/")[-1].split("_")[-1].split(".")[0]
location = (-0.26, -0.0124, 0.7022)
location = (-0.26, 0.0076, 0.8022)
rotation = (90, 293, 180)
rotation = (360,0,33) # han seg
rotation = (94, 207, 0) # airway
#rotation = (0, 0, 90) # aneurysm
scale = (0.8, 0.8, 0.8)
#scale = (0.9, 0.9, 0.9)
# scale = (0.00009, 0.00009, 0.00009)
#mesh = bt.readMesh(meshPath.replace(".ply", "_scaled.ply"), location, rotation, scale)
# V = np.array([[1,1,1],[-1,1,-1],[-1,-1,1],[1,-1,-1]], dtype=np.float32) # vertex list
# F = np.array([[0,1,2],[0,2,3],[0,3,1],[2,1,3]], dtype=np.int32) # face list
mesh = bt.readNumpyMesh(V,F,location,rotation,scale)
# han seg
# vertex_scalars = np.load("/local-scratch2/asa409/data/brain_vessels/HaN-Seg/HAN-SEG-CT_recon_scalars.npz")["colors"]
# vertex_scalars = np.load("/local-scratch2/asa409/data/brain_vessels/HaN-Seg/HAN-SEG-CT_GT_scalars.npz")["colors"]
# airways
vertex_scalars = np.load("/local-scratch/localhome/asa409/DATA/brain_vessels/NeRP/case1_fixed_recon_colors.npz")["colors"]
#vertex_scalars = np.load("/local-scratch/localhome/asa409/DATA/brain_vessels/NeRP/case1_fixed_gt_colors.npz")["colors"]
# aneurysm
#vertex_scalars = np.load("/local-scratch/localhome/asa409/DATA/brain_vessels/IntrA/complete/ArteryObjAN168_error_gt.npz")["colors"]
#vertex_scalars = np.load("/local-scratch/localhome/asa409/DATA/brain_vessels/IntrA/complete/ArteryObjAN168_error_pred.npz")["colors"]
# vasc
#vertex_scalars = np.load("/local-scratch/localhome/asa409/DATA/WT_vascusynth/VASCSYNTH_processed/G4D10_error_gt.npz")["colors"] * 0.0001
#vertex_scalars = np.load("/local-scratch/localhome/asa409/DATA/WT_vascusynth/VASCSYNTH_processed/G4D10_error_pred.npz")["colors"] 

#vertex_scalars= get_colormap_colors(vertex_scalars, colormap='plasma')
print (vertex_scalars.shape, V.shape)
# vertex_scalars = np.array([0.,1.,2.,3.]) # vertex color list
color_type = 'vertex'
color_map = 'red'
#mesh = bt.setMeshColors(mesh, vertex_scalars, color_type)
mesh = bt.setMeshScalars(mesh, vertex_scalars, color_map, color_type)

## set shading (uncomment one of them)
bpy.ops.object.shade_smooth() 

## subdivision
# bt.subdivision(mesh, level = 0)
from matplotlib import cm
import matplotlib.pyplot as plt

#meshVColor = cm.get_cmap('jet')(vertex_scalars)
# # set material 
meshVColor = bt.colorObj([], 0.5, 1.0, 1.0, 0.0, 0.0)
bt.setMat_VColor(mesh, meshVColor)

## set invisible plane (shadow catcher)
bt.invisibleGround(shadowBrightness=0.9)

## set camera (recommend to change mesh instead of camera, unless you want to adjust the Elevation)
camLocation = (3, 0, 2)
lookAtLocation = (0,0,0.5)
focalLength = 45 # (UI: click camera > Object Data > Focal Length)
cam = bt.setCamera(camLocation, lookAtLocation, focalLength)

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
bpy.ops.wm.save_mainfile(filepath=os.getcwd() + '/test.blend')

# save rendering
bt.renderImage(outputPath, cam)
