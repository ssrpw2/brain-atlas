# Brain Atlas

Interactive 3D brain atlas for introductory neuroscience study. 45 anatomical mesh files covering 23 brain structures, organized by lobe.

## Usage

Open `brain_atlas.blend` in [Blender](https://www.blender.org/) (4.0+). Navigate with middle-mouse drag (orbit), scroll (zoom), shift+middle-mouse (pan). Toggle lobe visibility via the eye icons in the Outliner panel.

### Collections

- **Frontal Lobe** — Superior/middle/inferior frontal gyrus, precentral gyrus (motor cortex)
- **Parietal Lobe** — Postcentral gyrus (somatosensory), supramarginal gyrus, angular gyrus
- **Temporal Lobe** — Middle/inferior temporal gyrus, fusiform gyrus, parahippocampal gyrus
- **Occipital Lobe** — Occipital lobe (visual cortex)
- **Limbic / Deep** — Hippocampus, amygdala, thalamus, hypothalamus, cingulate gyrus, insula, corpus callosum
- **Brainstem + Cerebellum** — Cerebellum, pons, medulla oblongata, midbrain

### Re-rendering

Requires Blender 4.0+ and Python with numpy.

```bash
# Render 7 multi-view stills
blender --background --python render_brain.py

# Rebuild the .blend scene file
blender --background --python save_scene.py
```

## Data Source

3D mesh data from **BodyParts3D** (version 4.0), Database Center for Life Science (DBCLS), Japan.

> BodyParts3D, © The Database Center for Life Science licensed under [CC Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)

- Website: https://lifesciencedb.jp/bp3d/
- Download: https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html
- Anatomical concepts follow the Foundational Model of Anatomy (FMA) ontology
