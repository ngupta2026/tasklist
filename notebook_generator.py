from __future__ import annotations

import json
from typing import Any

from task_specs import TASK_SPECS


def markdown_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line if line.endswith("\n") else f"{line}\n" for line in source.splitlines()],
    }


def code_cell(source: str) -> dict[str, Any]:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line if line.endswith("\n") else f"{line}\n" for line in source.splitlines()],
    }


def level_guidance(level: str) -> str:
    guidance = {
        "Beginner": "The explanations should assume minimal prior image-processing experience and define each step clearly.",
        "Intermediate": "The explanations should move briskly, calling out key implementation ideas and tradeoffs.",
        "Advanced": "The explanations should emphasize algorithmic choices, parameter tuning, and extension ideas.",
    }
    return guidance[level]


def challenge_block(task: dict[str, Any]) -> str:
    prompts = "\n".join(f"1. {prompt}" for prompt in task["practice_prompts"])
    return f"## Practice Prompts\n\n{prompts}"


def notes_block(task: dict[str, Any]) -> str:
    bullets = "\n".join(f"- {note}" for note in task["solution_notes"])
    return f"## Why This Works\n\n{bullets}"


def build_notebook_bytes(
    task_key: str,
    tutorial_level: str,
    image_asset_path: str,
    original_filename: str,
    include_challenges: bool,
    include_solution_notes: bool,
) -> bytes:
    task = TASK_SPECS[task_key]

    intro = f"""# {task["title"]} Tutorial

This notebook was generated for the input image `{original_filename}`.

## Goal

{task["goal"]}

## Tutorial Style

{level_guidance(tutorial_level)}
"""

    setup = """# Core imports for the tutorial
from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

plt.style.use("seaborn-v0_8")
"""

    load_image = f"""# Load the image from the bundled assets folder
image_path = Path("{image_asset_path}")
image_bgr = cv2.imread(str(image_path))

if image_bgr is None:
    raise FileNotFoundError(f"Could not read image at {{image_path.resolve()}}")

image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
print("Image shape:", image_rgb.shape)

plt.figure(figsize=(8, 6))
plt.imshow(image_rgb)
plt.title("Original Image")
plt.axis("off")
plt.show()
"""

    notebook = {
        "cells": [
            markdown_cell(intro),
            markdown_cell(
                f"""## Workflow

- Task: {task["title"]}
- Suggested libraries: {", ".join(task["libraries"])}
- Input asset path: `{image_asset_path}`
"""
            ),
            code_cell(setup),
            code_cell(load_image),
            markdown_cell(f"## Step-by-Step Tutorial\n\n{task['walkthrough']}"),
            code_cell(task["code_template"]),
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    if include_solution_notes:
        notebook["cells"].append(markdown_cell(notes_block(task)))

    if include_challenges:
        notebook["cells"].append(markdown_cell(challenge_block(task)))

    notebook["cells"].append(
        markdown_cell(
            """## Next Steps

- Replace the sample image with another file from the `assets/` folder.
- Try tuning parameters and rerunning the notebook.
- Convert this tutorial into a reusable Python script once the workflow is stable.
"""
        )
    )

    return json.dumps(notebook, indent=2).encode("utf-8")
