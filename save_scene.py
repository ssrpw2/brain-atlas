import bpy
import mathutils
import os
import math

OBJ_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_obj")
OUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brain_atlas.blend")

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
    "thalamus":               (0.85, 0.55, 0.55, 1.0),
    "hypothalamus":           (0.85, 0.45, 0.45, 1.0),
    "hippocampus":            (0.95, 0.75, 0.35, 1.0),
    "amygdala":               (0.90, 0.60, 0.30, 1.0),
    "corpus_callosum":        (0.75, 0.75, 0.75, 1.0),
    "insula":                 (0.50, 0.70, 0.65, 1.0),
    "cingulate_gyrus":        (0.60, 0.60, 0.80, 1.0),
}

READABLE_NAMES = {
    "superior_frontal_gyrus": "Superior Frontal Gyrus",
    "middle_frontal_gyrus": "Middle Frontal Gyrus",
    "inferior_frontal_gyrus": "Inferior Frontal Gyrus",
    "precentral_gyrus": "Precentral Gyrus (Motor Cortex)",
    "postcentral_gyrus": "Postcentral Gyrus (Somatosensory)",
    "supramarginal_gyrus": "Supramarginal Gyrus",
    "angular_gyrus": "Angular Gyrus",
    "middle_temporal_gyrus": "Middle Temporal Gyrus",
    "inferior_temporal_gyrus": "Inferior Temporal Gyrus",
    "fusiform_gyrus": "Fusiform Gyrus",
    "parahippocampal_gyrus": "Parahippocampal Gyrus",
    "occipital_lobe": "Occipital Lobe",
    "cerebellum": "Cerebellum",
    "pons": "Pons",
    "medulla_oblongata": "Medulla Oblongata",
    "midbrain": "Midbrain",
    "thalamus": "Thalamus",
    "hypothalamus": "Hypothalamus",
    "hippocampus": "Hippocampus",
    "amygdala": "Amygdala",
    "corpus_callosum": "Corpus Callosum",
    "insula": "Insula",
    "cingulate_gyrus": "Cingulate Gyrus",
}

LOBE_GROUPS = {
    "Frontal Lobe": ["superior_frontal_gyrus", "middle_frontal_gyrus", "inferior_frontal_gyrus", "precentral_gyrus"],
    "Parietal Lobe": ["postcentral_gyrus", "supramarginal_gyrus", "angular_gyrus"],
    "Temporal Lobe": ["middle_temporal_gyrus", "inferior_temporal_gyrus", "fusiform_gyrus", "parahippocampal_gyrus"],
    "Occipital Lobe": ["occipital_lobe"],
    "Limbic / Deep": ["hippocampus", "amygdala", "thalamus", "hypothalamus", "cingulate_gyrus", "insula", "corpus_callosum"],
    "Brainstem + Cerebellum": ["cerebellum", "pons", "medulla_oblongata", "midbrain"],
}

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# World
world = bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.18, 0.20, 0.22, 1.0)

# Create collections for each lobe group
for group_name in LOBE_GROUPS:
    col = bpy.data.collections.new(group_name)
    scene.collection.children.link(col)

# Import OBJs into appropriate collections
imported = 0
for fname in sorted(os.listdir(OBJ_DIR)):
    if not fname.endswith('.obj'):
        continue
    filepath = os.path.join(OBJ_DIR, fname)
    bpy.ops.wm.obj_import(filepath=filepath)
    obj = bpy.context.selected_objects[0]

    struct_name = '_'.join(fname.replace('.obj', '').split('_')[:-1])
    fj_id = fname.replace('.obj', '').split('_')[-1]
    color = COLORS.get(struct_name, (0.7, 0.7, 0.7, 1.0))

    # Determine L/R suffix from FJ pairs
    side = ""
    if struct_name in ["corpus_callosum"]:
        side = ""
    else:
        # Most structures come in pairs; use FJ ordering
        pass

    readable = READABLE_NAMES.get(struct_name, struct_name.replace('_', ' ').title())
    obj.name = f"{readable} ({fj_id})"

    # Material
    mat = bpy.data.materials.new(name=f"mat_{struct_name}_{fj_id}")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = 0.55
    bsdf.inputs["Specular IOR Level"].default_value = 0.35
    obj.data.materials.clear()
    obj.data.materials.append(mat)

    # Smooth shading
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()

    # Move to appropriate collection
    for group_name, members in LOBE_GROUPS.items():
        if struct_name in members:
            target_col = bpy.data.collections[group_name]
            target_col.objects.link(obj)
            scene.collection.objects.unlink(obj)
            break

    imported += 1

print(f"Imported {imported} objects into {len(LOBE_GROUPS)} collections")

# Compute center for camera
import numpy as np
all_coords = []
for obj in bpy.data.objects:
    if obj.type != 'MESH':
        continue
    for v in obj.data.vertices:
        co = obj.matrix_world @ v.co
        all_coords.append((co.x, co.y, co.z))
coords = np.array(all_coords)
center = coords.mean(axis=0)
span = (coords.max(axis=0) - coords.min(axis=0)).max()

# Lighting
key = bpy.data.lights.new(name="Key Light", type='SUN')
key.energy = 3.0
key.color = (1.0, 0.98, 0.95)
key_obj = bpy.data.objects.new(name="Key Light", object_data=key)
scene.collection.objects.link(key_obj)
key_obj.rotation_euler = (math.radians(50), math.radians(10), math.radians(30))

fill = bpy.data.lights.new(name="Fill Light", type='SUN')
fill.energy = 1.5
fill.color = (0.90, 0.92, 1.0)
fill_obj = bpy.data.objects.new(name="Fill Light", object_data=fill)
scene.collection.objects.link(fill_obj)
fill_obj.rotation_euler = (math.radians(40), math.radians(-30), math.radians(-60))

rim = bpy.data.lights.new(name="Rim Light", type='SUN')
rim.energy = 2.0
rim_obj = bpy.data.objects.new(name="Rim Light", object_data=rim)
scene.collection.objects.link(rim_obj)
rim_obj.rotation_euler = (math.radians(-20), math.radians(0), math.radians(150))

# Camera — left lateral default view
cam_data = bpy.data.cameras.new(name="Camera")
cam_data.type = 'ORTHO'
cam_data.ortho_scale = span * 1.2
cam_obj = bpy.data.objects.new(name="Camera", object_data=cam_data)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

dist = span * 2
az = math.radians(90)
el = math.radians(10)
cx = center[0] + dist * math.cos(el) * math.sin(az)
cy = center[1] + dist * math.cos(el) * math.cos(az)
cz = center[2] + dist * math.sin(el)
cam_obj.location = (cx, cy, cz)
direction = mathutils.Vector((center[0] - cx, center[1] - cy, center[2] - cz))
rot_quat = direction.to_track_quat('-Z', 'Y')
cam_obj.rotation_euler = rot_quat.to_euler()

# Render settings
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080

# Save
bpy.ops.wm.save_as_mainfile(filepath=OUT_FILE)
print(f"Saved scene to {OUT_FILE}")
print(f"\nCollections (toggle visibility in Blender's Outliner):")
for name in LOBE_GROUPS:
    col = bpy.data.collections[name]
    print(f"  {name}: {len(col.objects)} objects")
print(f"\nNavigation: Middle-mouse to orbit, scroll to zoom, Shift+middle to pan")
print(f"Toggle collections with the eye icon in the Outliner to show/hide lobe groups")
