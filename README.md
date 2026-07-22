# Brain Atlas

Interactive 3D brain atlas for introductory neuroscience study. 45 anatomical mesh files covering 23 brain structures, organized by lobe and color-coded by region.

[Braint Atlas](https://ssrpw2.github.io/brain-atlas/)
## What's in this repo

| File / Folder | What it is |
|---|---|
| `brain_atlas.blend` | Blender scene with all 23 structures imported, colored by lobe, and organized into collections |
| `brain_obj/` | 45 individual mesh files (`.obj` format) — left and right hemispheres for most structures |
| `renders/` | 7 pre-rendered views (lateral, anterior, posterior, dorsal, ventral, midsagittal) as PNG images |
| `render_brain.py` | Python script to re-render the 7 views from the command line |
| `save_scene.py` | Python script to rebuild the `.blend` file from the raw meshes |
| `index.html` | Project home page |
| `views.html` | Visual atlas page showing all 7 anatomical views with labels |

## Structures included

**Frontal Lobe** — Superior frontal gyrus, middle frontal gyrus, inferior frontal gyrus, precentral gyrus (primary motor cortex)

**Parietal Lobe** — Postcentral gyrus (primary somatosensory cortex), supramarginal gyrus, angular gyrus

**Temporal Lobe** — Middle temporal gyrus, inferior temporal gyrus, fusiform gyrus, parahippocampal gyrus

**Occipital Lobe** — Occipital lobe (primary visual cortex)

**Limbic and Deep Structures** — Hippocampus, amygdala, thalamus, hypothalamus, cingulate gyrus, insula, corpus callosum

**Brainstem and Cerebellum** — Cerebellum, pons, medulla oblongata, midbrain

## How to view the 3D model

You need [Blender](https://www.blender.org/download/), a free and open-source 3D application. Version 4.0 or newer is required.

### Step-by-step instructions

1. **Download and install Blender**
   - Go to [blender.org/download](https://www.blender.org/download/)
   - Choose your operating system (Windows, Mac, or Linux)
   - Run the installer and follow the prompts — all default settings are fine

2. **Download this repository**
   - Click the green **Code** button at the top of this page
   - Click **Download ZIP**
   - Unzip the downloaded file to a folder on your computer

3. **Open the brain atlas**
   - Launch Blender
   - Go to **File > Open** (or press `Ctrl+O` / `Cmd+O` on Mac)
   - Navigate to the folder you unzipped and select `brain_atlas.blend`
   - Click **Open**

4. **Navigate the 3D model**
   - **Orbit (rotate the view):** Hold the middle mouse button and drag. On a trackpad, hold `Ctrl` and two-finger drag
   - **Zoom:** Scroll the mouse wheel. On a trackpad, pinch or two-finger scroll
   - **Pan (move the view):** Hold `Shift` + middle mouse button and drag. On a trackpad, `Shift` + two-finger drag
   - **Reset the view:** Press `Numpad .` (period) to center on the selected object, or `Home` to see everything

5. **Toggle structure visibility**
   - In the top-right panel (called the **Outliner**), you'll see collections named by lobe (Frontal Lobe, Parietal Lobe, etc.)
   - Click the **eye icon** next to any collection to hide or show that group of structures
   - Click the **eye icon** next to individual structures within a collection to toggle them one at a time

### Re-rendering the views (optional, requires command-line use)

If you modify the scene and want to regenerate the 7 PNG views:

```bash
blender --background --python render_brain.py
```

Output images are saved to the `renders/` folder.

## Data source

All 3D mesh data comes from **BodyParts3D** (version 4.0), produced by the Database Center for Life Science (DBCLS), Japan.

> BodyParts3D, Copyright The Database Center for Life Science, licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

The CC BY 4.0 license means the data is free to use, share, and adapt for any purpose, including commercially, as long as you give appropriate credit. This repository provides that attribution here and in the project pages.

- Website: https://lifesciencedb.jp/bp3d/
- Download: https://dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html
- Anatomical concepts follow the Foundational Model of Anatomy (FMA) ontology
