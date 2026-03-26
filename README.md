# Image Processing Tutorial Notebook Generator

This project is a lightweight app for generating Python tutorial notebooks from uploaded images.

## What it does

- Accepts one or more input images.
- Lets the user choose an image-processing task from a predefined list.
- Generates a Jupyter notebook tutorial tailored to that task.
- Bundles the notebook and uploaded image assets into a ZIP for easy execution.

## Supported task types

- Grayscale conversion and contrast enhancement
- Resize and crop
- Noise reduction
- Threshold-based segmentation
- Edge detection
- Contour analysis

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## How the generated notebooks work

Each notebook includes:

- Setup imports
- Image loading code
- A step-by-step explanation of the selected workflow
- Runnable OpenCV and Matplotlib code
- Optional practice prompts and solution notes

## Future improvements

- Generate task-specific notebooks with LLM-authored explanations
- Add notebook export for multiple tasks at once
- Let users define custom processing goals in plain language
- Save notebook generation history
