import bpy
import mathutils
import os
import math

OBJ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_obj")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "renders")
os.makedirs(OUT_DIR, exist_ok=True)

# Color palette by region group
COLORS = {
    "superior_frontal_gyrus": (0.42, 0.68, 0.79, 1.0),   # frontal - blue
    "middle_frontal_gyrus":   (0.42, 0.68, 0.79, 1.0),
    "inferior_frontal_gyrus": (0.42, 0.68, 0.79, 1.0),
    "precentral_gyrus":       (0.35, 0.60, 0.72, 1.0),    # frontal/motor - darker blue
    "postcentral_gyrus":      (0.78, 0.71, 0.39, 1.0),    # parietal - gold
    "supramarginal_gyrus":    (0.78, 0.71, 0.39, 1.0),
    "angular_gyrus":          (0.78, 0.71, 0.39, 1.0),
    "middle_temporal_gyrus":  (0.36, 0.78, 0.48, 1.0),    # temporal - green
    "inferior_temporal_gyrus":(0.36, 0.78, 0.48, 1.0),
    "fusiform_gyrus":         (0.36, 0.78, 0.48, 1.0),
    "parahippocampal_gyrus":  (0.36, 0.78, 0.48, 1.0),
    "occipital_lobe":         (0.66, 0.42, 0.78, 1.0),    # occipital - purple
    "cerebellum":             (0.77, 0.52, 0.42, 1.0),    # cerebellum - terracotta
    "pons":                   (0.54, 0.56, 0.44, 1.0),    # brainstem - olive
    "medulla_oblongata":      (0.54, 0.56, 0.44, 1.0),
    "midbrain":               (0.54, 0.56, 0.44, 1.0),
    "superior_temporal_gyrus": (0.36, 0.78, 0.48, 1.0),    # temporal - green
    "superior_parietal_lobule":(0.78, 0.71, 0.39, 1.0),   # parietal - gold
    "orbital_gyrus":          (0.42, 0.68, 0.79, 1.0),    # frontal - blue
    "thalamus":               (0.72, 0.42, 0.65, 1.0),    # thalamus - mauve
    "hypothalamus":           (0.92, 0.33, 0.33, 1.0),    # hypothalamus - vivid red
    "hippocampus":            (0.95, 0.75, 0.35, 1.0),    # hippocampus - amber
    "amygdala":               (0.90, 0.60, 0.30, 1.0),    # amygdala - orange
    "corpus_callosum":        (0.75, 0.75, 0.75, 1.0),    # corpus callosum - light gray
    "insula":                 (0.50, 0.70, 0.65, 1.0),    # insula - teal
    "cingulate_gyrus":        (0.60, 0.60, 0.80, 1.0),    # cingulate - lavender
}

VIEWS = {
    "lateral_left":   {"azimuth": 90,  "elevation": 10, "label": "Left Lateral"},
    "lateral_right":  {"azimuth": -90, "elevation": 10, "label": "Right Lateral"},
    "anterior":       {"azimuth": 0,   "elevation": 5,  "label": "Anterior (Front)"},
    "posterior":      {"azimuth": 180, "elevation": 5,  "label": "Posterior (Back)"},
    "dorsal":         {"azimuth": 0,   "elevation": 89, "label": "Dorsal (Top)"},
    "ventral":        {"azimuth": 0,   "elevation": -89,"label": "Ventral (Bottom)"},
    "midsagittal":    {"azimuth": 90,  "elevation": 0,  "label": "Midsagittal"},
}

# Clear default scene
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# World background
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.95, 0.95, 0.97, 1.0)

# Import all brain OBJ files
imported_objects = []
for fname in sorted(os.listdir(OBJ_DIR)):
    if not fname.endswith('.obj'):
        continue
    filepath = os.path.join(OBJ_DIR, fname)
    bpy.ops.wm.obj_import(filepath=filepath)
    obj = bpy.context.selected_objects[0]

    # Determine color from filename
    struct_name = '_'.join(fname.replace('.obj', '').split('_')[:-1])
    color = COLORS.get(struct_name, (0.7, 0.7, 0.7, 1.0))

    # Create material
    mat = bpy.data.materials.new(name=f"mat_{fname}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.6
    bsdf.inputs["Specular IOR Level"].default_value = 0.3

    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # Smooth shading
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

    imported_objects.append(obj)

print(f"Imported {len(imported_objects)} objects")

# Rotate brain so brainstem faces down (-Z), matching save_scene.py
rot_matrix = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
for obj in imported_objects:
    obj.matrix_world = rot_matrix @ obj.matrix_world

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# Compute bounding box of all objects (no numpy needed)
all_x, all_y, all_z = [], [], []
for obj in imported_objects:
    for v in obj.data.vertices:
        co = obj.matrix_world @ v.co
        all_x.append(co.x)
        all_y.append(co.y)
        all_z.append(co.z)

cx = sum(all_x) / len(all_x)
cy = sum(all_y) / len(all_y)
z_min = min(all_z)
z_max = max(all_z)
span = max(max(all_x) - min(all_x), max(all_y) - min(all_y), z_max - z_min)

# Center brain at origin (XY), brainstem resting on XY plane (Z=0)
offset = mathutils.Vector((-cx, -cy, -z_min))
for obj in imported_objects:
    obj.location += offset

center = (0.0, 0.0, (z_max - z_min) / 2.0)

print(f"Center: {center}, Span: {span}")

# Add lighting
# Key light
key = bpy.data.lights.new(name="Key", type='SUN')
key.energy = 3.0
key_obj = bpy.data.objects.new(name="Key", object_data=key)
scene.collection.objects.link(key_obj)
key_obj.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))

# Fill light
fill = bpy.data.lights.new(name="Fill", type='SUN')
fill.energy = 1.5
fill_obj = bpy.data.objects.new(name="Fill", object_data=fill)
scene.collection.objects.link(fill_obj)
fill_obj.rotation_euler = (math.radians(40), math.radians(-30), math.radians(-60))

# Rim light
rim = bpy.data.lights.new(name="Rim", type='SUN')
rim.energy = 2.0
rim_obj = bpy.data.objects.new(name="Rim", object_data=rim)
scene.collection.objects.link(rim_obj)
rim_obj.rotation_euler = (math.radians(-20), math.radians(0), math.radians(150))

# Camera
cam_data = bpy.data.cameras.new(name="Camera")
cam_data.type = 'ORTHO'
cam_data.ortho_scale = span * 1.6
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Render each view
dist = span * 2
for view_name, view_cfg in VIEWS.items():
    az = math.radians(view_cfg["azimuth"])
    el = math.radians(view_cfg["elevation"])

    # Camera position on sphere around center
    cx = center[0] + dist * math.cos(el) * math.sin(az)
    cy = center[1] + dist * math.cos(el) * math.cos(az)
    cz = center[2] + dist * math.sin(el)

    cam_obj.location = (cx, cy, cz)

    # Point camera at center
    direction = (center[0] - cx, center[1] - cy, center[2] - cz)
    rot_quat = mathutils.Vector(direction).to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()

    # Render
    outpath = os.path.join(OUT_DIR, f"brain_{view_name}.png")
    scene.render.filepath = outpath
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {view_name} -> {outpath}")

print("Done! All views rendered.")
