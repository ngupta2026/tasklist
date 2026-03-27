from __future__ import annotations

import io
import zipfile
from pathlib import Path

import streamlit as st
from PIL import Image

from notebook_generator import build_notebook_bytes
from task_specs import TASK_SPECS


st.set_page_config(
    page_title="Image Task Tutorial Notebook Generator",
    page_icon="IP",
    layout="wide",
)


def sanitize_name(name: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in name)
    return cleaned.strip("_") or "image"


def image_preview(uploaded_file) -> Image.Image:
    return Image.open(uploaded_file).convert("RGB")


def make_archive(files: list[tuple[str, bytes]]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for filename, payload in files:
            archive.writestr(filename, payload)
    buffer.seek(0)
    return buffer.getvalue()


st.title("Image Processing Tutorial Notebook Generator")
st.write(
    "Upload one or more images, pick a task, and generate Python notebooks that walk "
    "through image-processing workflows such as blurring, sharpening, thresholding, "
    "edge detection, and enhancement as a tutorial."
)

with st.sidebar:
    st.header("Notebook Settings")
    selected_task = st.selectbox(
        "Task type",
        options=list(TASK_SPECS.keys()),
        format_func=lambda key: TASK_SPECS[key]["title"],
    )
    tutorial_level = st.select_slider(
        "Tutorial depth",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner",
    )
    include_challenges = st.checkbox("Add practice prompts", value=True)
    include_solution_notes = st.checkbox("Add explanation notes", value=True)

uploaded_files = st.file_uploader(
    "Input images",
    type=["png", "jpg", "jpeg", "bmp", "tif", "tiff"],
    accept_multiple_files=True,
)

task = TASK_SPECS[selected_task]

st.subheader(task["title"])
st.write(task["description"])
st.caption(f"Python stack: {', '.join(task['libraries'])}")

if uploaded_files:
    preview_cols = st.columns(min(3, len(uploaded_files)))
    for index, uploaded_file in enumerate(uploaded_files):
        with preview_cols[index % len(preview_cols)]:
            preview = image_preview(uploaded_file)
            st.image(preview, caption=uploaded_file.name, use_container_width=True)

generate = st.button("Generate tutorial notebook", type="primary", disabled=not uploaded_files)

if generate and uploaded_files:
    output_files: list[tuple[str, bytes]] = []

    for uploaded_file in uploaded_files:
        image_bytes = uploaded_file.getvalue()
        image_name = Path(uploaded_file.name).name
        stem = sanitize_name(Path(image_name).stem)
        image_extension = Path(image_name).suffix.lower() or ".png"
        asset_name = f"assets/{stem}{image_extension}"
        notebook_name = f"{stem}_{selected_task}_tutorial.ipynb"

        notebook_bytes = build_notebook_bytes(
            task_key=selected_task,
            tutorial_level=tutorial_level,
            image_asset_path=asset_name,
            original_filename=image_name,
            include_challenges=include_challenges,
            include_solution_notes=include_solution_notes,
        )

        output_files.append((notebook_name, notebook_bytes))
        output_files.append((asset_name, image_bytes))

    if len(uploaded_files) == 1:
        notebook_filename, notebook_payload = output_files[0]
        st.success("Notebook generated successfully.")
        st.download_button(
            "Download notebook",
            data=notebook_payload,
            file_name=notebook_filename,
            mime="application/x-ipynb+json",
        )
        st.info(
            "Download the image separately from the uploader or use the ZIP option below "
            "to keep notebook and asset paths together."
        )

    archive_bytes = make_archive(output_files)
    st.download_button(
        "Download ZIP bundle",
        data=archive_bytes,
        file_name=f"{selected_task}_tutorial_bundle.zip",
        mime="application/zip",
    )
    st.code(
        "pip install -r requirements.txt\njupyter notebook",
        language="bash",
    )
