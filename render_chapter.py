import bpy
import mathutils
import os
import math
import sys
import json

OBJ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_obj")
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "renders")
os.makedirs(OUT_DIR, exist_ok=True)

COLORS = {
    "superior_frontal_gyrus": (0.42, 0.68, 0.79, 1.0),
    "middle_frontal_gyrus":   (0.42, 0.68, 0.79, 1.0),
    "inferior_frontal_gyrus": (0.42, 0.68, 0.79, 1.0),
    "precentral_gyrus":       (0.35, 0.60, 0.72, 1.0),
    "postcentral_gyrus":      (0.78, 0.71, 0.39, 1.0),
    "supramarginal_gyrus":    (0.78, 0.71, 0.39, 1.0),
    "angular_gyrus":          (0.78, 0.71, 0.39, 1.0),
    "middle_temporal_gyrus":  (0.36, 0.78, 0.48, 1.0),
    "inferior_temporal_gyrus":(0.36, 0.78, 0.48, 1.0),
    "fusiform_gyrus":         (0.36, 0.78, 0.48, 1.0),
    "parahippocampal_gyrus":  (0.36, 0.78, 0.48, 1.0),
    "occipital_lobe":         (0.66, 0.42, 0.78, 1.0),
    "cerebellum":             (0.77, 0.52, 0.42, 1.0),
    "pons":                   (0.54, 0.56, 0.44, 1.0),
    "medulla_oblongata":      (0.54, 0.56, 0.44, 1.0),
    "midbrain":               (0.54, 0.56, 0.44, 1.0),
    "superior_temporal_gyrus": (0.36, 0.78, 0.48, 1.0),
    "superior_parietal_lobule":(0.78, 0.71, 0.39, 1.0),
    "orbital_gyrus":          (0.42, 0.68, 0.79, 1.0),
    "thalamus":               (0.72, 0.42, 0.65, 1.0),
    "hypothalamus":           (0.92, 0.33, 0.33, 1.0),
    "hippocampus":            (0.95, 0.75, 0.35, 1.0),
    "amygdala":               (0.90, 0.60, 0.30, 1.0),
    "fornix":                 (0.80, 0.80, 0.78, 1.0),
    "fornix_commissure":      (0.80, 0.80, 0.78, 1.0),
    "caudate_nucleus":        (0.40, 0.72, 0.68, 1.0),
    "putamen":                (0.35, 0.65, 0.62, 1.0),
    "globus_pallidus":        (0.30, 0.60, 0.70, 1.0),
    "pineal_gland":           (0.54, 0.56, 0.44, 1.0),
    "corpus_callosum":        (0.75, 0.75, 0.75, 1.0),
    "insula":                 (0.50, 0.70, 0.65, 1.0),
    "cingulate_gyrus":        (0.60, 0.60, 0.80, 1.0),
    "lateral_ventricle":      (0.45, 0.65, 0.90, 1.0),
    "third_ventricle":        (0.40, 0.60, 0.85, 1.0),
    "fourth_ventricle":       (0.35, 0.55, 0.80, 1.0),
    "optic_chiasm":           (0.95, 0.85, 0.40, 1.0),
    "mammillary_body":        (0.92, 0.45, 0.38, 1.0),
    "superior_colliculus":    (0.60, 0.52, 0.42, 1.0),
    "inferior_colliculus":    (0.55, 0.48, 0.40, 1.0),
    "internal_capsule":       (0.82, 0.82, 0.80, 1.0),
    "cerebral_peduncle":      (0.70, 0.62, 0.50, 1.0),
    "optic_tract":            (0.90, 0.80, 0.40, 1.0),
    "anterior_commissure":    (0.78, 0.78, 0.76, 1.0),
    "posterior_commissure":   (0.76, 0.76, 0.74, 1.0),
    "choroid_plexus":         (0.85, 0.45, 0.50, 1.0),
    "stria_medullaris":       (0.72, 0.72, 0.70, 1.0),
    "cerebral_white_matter":  (0.88, 0.88, 0.86, 1.0),
}

DIM_COLOR = (0.55, 0.55, 0.58, 1.0)
DIM_ALPHA = 0.08

# Chapter configs: which structures to highlight and which views to render
CHAPTERS = {
    "ch10": {
        "name": "Biological Rhythms and Sleep",
        "highlight": ["hypothalamus", "thalamus", "pons", "medulla_oblongata", "midbrain", "pineal_gland", "optic_chiasm", "optic_tract", "mammillary_body"],
        "views": {
            "midsagittal":    {"azimuth": 90,  "elevation": 0,  "label": "Midsagittal"},
            "anterior":       {"azimuth": 0,   "elevation": 5,  "label": "Anterior"},
            "ventral":        {"azimuth": 0,   "elevation": -89, "label": "Ventral"},
            "deep_ghosted":   {"azimuth": 70,  "elevation": 20, "label": "Deep structures (ghosted)"},
            "deep_only":      {"azimuth": 70,  "elevation": 20, "label": "Deep structures (isolated)", "hide_dim": True},
        }
    }
}

chapter = sys.argv[sys.argv.index("--chapter") + 1] if "--chapter" in sys.argv else "ch10"
cfg = CHAPTERS[chapter]
highlight_set = set(cfg["highlight"])

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.film_transparent = True
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'

# Enable transparency in EEVEE
scene.eevee.use_gtao = True

world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.95, 0.95, 0.97, 1.0)

imported_objects = []
dim_objects = []
for fname in sorted(os.listdir(OBJ_DIR)):
    if not fname.endswith('.obj'):
        continue
    filepath = os.path.join(OBJ_DIR, fname)
    bpy.ops.wm.obj_import(filepath=filepath)
    obj = bpy.context.selected_objects[0]

    struct_name = '_'.join(fname.replace('.obj', '').split('_')[:-1])
    is_highlighted = struct_name in highlight_set

    mat = bpy.data.materials.new(name=f"mat_{fname}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]

    if is_highlighted:
        color = COLORS.get(struct_name, (0.7, 0.7, 0.7, 1.0))
        bsdf.inputs["Base Color"].default_value = color
        bsdf.inputs["Roughness"].default_value = 0.5
        bsdf.inputs["Specular IOR Level"].default_value = 0.4
        bsdf.inputs["Emission Color"].default_value = color
        bsdf.inputs["Emission Strength"].default_value = 0.6
    else:
        bsdf.inputs["Base Color"].default_value = DIM_COLOR
        bsdf.inputs["Roughness"].default_value = 0.8
        bsdf.inputs["Specular IOR Level"].default_value = 0.1
        bsdf.inputs["Alpha"].default_value = DIM_ALPHA
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'
        dim_objects.append(obj)

    obj.data.materials.clear()
    obj.data.materials.append(mat)

    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()
    imported_objects.append(obj)

print(f"Imported {len(imported_objects)} objects, {len(highlight_set)} structures highlighted")

# Rotate brainstem down
rot_matrix = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')
for obj in imported_objects:
    obj.matrix_world = rot_matrix @ obj.matrix_world

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# Compute bounds and center
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

offset = mathutils.Vector((-cx, -cy, -z_min))
for obj in imported_objects:
    obj.location += offset

center = (0.0, 0.0, (z_max - z_min) / 2.0)

# Lighting
key = bpy.data.lights.new(name="Key", type='SUN')
key.energy = 3.0
key_obj = bpy.data.objects.new(name="Key", object_data=key)
scene.collection.objects.link(key_obj)
key_obj.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))

fill = bpy.data.lights.new(name="Fill", type='SUN')
fill.energy = 1.5
fill_obj = bpy.data.objects.new(name="Fill", object_data=fill)
scene.collection.objects.link(fill_obj)
fill_obj.rotation_euler = (math.radians(40), math.radians(-30), math.radians(-60))

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

dist = span * 2
for view_name, view_cfg in cfg["views"].items():
    hide_dim = view_cfg.get("hide_dim", False)
    for obj in dim_objects:
        obj.hide_render = hide_dim

    az = math.radians(view_cfg["azimuth"])
    el = math.radians(view_cfg["elevation"])

    vx = center[0] + dist * math.cos(el) * math.sin(az)
    vy = center[1] + dist * math.cos(el) * math.cos(az)
    vz = center[2] + dist * math.sin(el)

    cam_obj.location = (vx, vy, vz)
    direction = (center[0] - vx, center[1] - vy, center[2] - vz)
    rot_quat = mathutils.Vector(direction).to_track_quat('-Z', 'Y')
    cam_obj.rotation_euler = rot_quat.to_euler()

    outpath = os.path.join(OUT_DIR, f"{chapter}_{view_name}.png")
    scene.render.filepath = outpath
    bpy.ops.render.render(write_still=True)
    print(f"Rendered: {chapter}_{view_name} -> {outpath}")

print("Done!")
