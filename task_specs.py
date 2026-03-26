from __future__ import annotations


TASK_SPECS = {
    "grayscale_enhancement": {
        "title": "Grayscale Conversion and Contrast Enhancement",
        "description": "Convert an input image to grayscale and improve contrast using histogram equalization.",
        "goal": "Produce a cleaner monochrome image that is easier to inspect or use in downstream vision tasks.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We first convert the RGB image into grayscale because many classical image-processing steps work on a single intensity channel.
Next, we use histogram equalization to spread out intensity values and make dim regions easier to see.
Finally, we compare the original grayscale image with the enhanced version side by side.""",
        "code_template": """# Convert to grayscale and improve contrast
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
enhanced = cv2.equalizeHist(gray)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(gray, cmap="gray")
axes[0].set_title("Grayscale")
axes[0].axis("off")

axes[1].imshow(enhanced, cmap="gray")
axes[1].set_title("Equalized Contrast")
axes[1].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Grayscale reduces computational complexity by collapsing color channels into one intensity map.",
            "Histogram equalization can reveal hidden details, especially in low-contrast images.",
            "This technique is often a useful preprocessing step before thresholding or edge detection.",
        ],
        "practice_prompts": [
            "Replace histogram equalization with CLAHE and compare the result.",
            "Plot the grayscale histogram before and after enhancement.",
            "Save the enhanced image to disk with `cv2.imwrite`.",
        ],
    },
    "resize_and_crop": {
        "title": "Resize and Crop for Model-Ready Inputs",
        "description": "Standardize image dimensions with resizing and center cropping.",
        "goal": "Create clean, consistently sized inputs for machine learning or document-processing pipelines.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We inspect the original dimensions first so the resize step is transparent.
Then we resize the image to a target width and height and extract a center crop.
This mirrors the sort of preprocessing often used before training or inference.""",
        "code_template": """# Resize and then center crop the image
target_size = (512, 512)
resized = cv2.resize(image_rgb, target_size, interpolation=cv2.INTER_AREA)

crop_size = 320
height, width = resized.shape[:2]
start_y = (height - crop_size) // 2
start_x = (width - crop_size) // 2
cropped = resized[start_y:start_y + crop_size, start_x:start_x + crop_size]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(resized)
axes[0].set_title("Resized Image")
axes[0].axis("off")

axes[1].imshow(cropped)
axes[1].set_title("Center Crop")
axes[1].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Resizing enforces a predictable input size across a dataset.",
            "Center cropping is a simple baseline when the subject is near the middle of the frame.",
            "Interpolation choice matters: `INTER_AREA` is often a good default for shrinking images.",
        ],
        "practice_prompts": [
            "Turn the crop logic into a reusable function.",
            "Try a non-square target size and inspect aspect-ratio distortion.",
            "Pad instead of crop when preserving all content matters.",
        ],
    },
    "denoise_and_blur": {
        "title": "Noise Reduction with Gaussian and Median Blur",
        "description": "Compare two common smoothing methods for reducing image noise.",
        "goal": "Reduce visual noise while keeping as much meaningful structure as possible.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We apply Gaussian blur to smooth the full image with a weighted kernel.
Then we apply median blur, which is especially useful for salt-and-pepper noise.
Comparing them side by side shows that each blur type has a different visual signature.""",
        "code_template": """# Compare Gaussian and median blur
gaussian = cv2.GaussianBlur(image_rgb, (7, 7), sigmaX=1.5)
median = cv2.medianBlur(image_rgb, 5)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(image_rgb)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(gaussian)
axes[1].set_title("Gaussian Blur")
axes[1].axis("off")

axes[2].imshow(median)
axes[2].set_title("Median Blur")
axes[2].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Gaussian blur smooths gradual variation and is widely used before edge detection.",
            "Median blur is more robust to isolated pixel spikes.",
            "Kernel size directly changes the strength of smoothing.",
        ],
        "practice_prompts": [
            "Increase the kernel size and observe detail loss.",
            "Measure the difference between blurred and original images numerically.",
            "Apply blur only to a region of interest.",
        ],
    },
    "threshold_segmentation": {
        "title": "Threshold-Based Segmentation",
        "description": "Separate foreground and background regions using binary thresholding.",
        "goal": "Create a mask that isolates brighter or darker structures in the image.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We begin by converting the image to grayscale so thresholding can operate on a single channel.
Then we compare a fixed threshold with Otsu's automatic threshold selection.
The resulting binary masks help reveal how segmentation quality depends on intensity distribution.""",
        "code_template": """# Build binary masks with fixed and Otsu thresholding
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
_, fixed_mask = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
_, otsu_mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(gray, cmap="gray")
axes[0].set_title("Grayscale")
axes[0].axis("off")

axes[1].imshow(fixed_mask, cmap="gray")
axes[1].set_title("Fixed Threshold")
axes[1].axis("off")

axes[2].imshow(otsu_mask, cmap="gray")
axes[2].set_title("Otsu Threshold")
axes[2].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Thresholding is one of the simplest forms of segmentation.",
            "Otsu's method chooses a threshold automatically from the histogram.",
            "Lighting changes can strongly affect binary segmentation quality.",
        ],
        "practice_prompts": [
            "Invert the mask to isolate the opposite intensity region.",
            "Apply morphological cleanup after thresholding.",
            "Overlay the mask on the original image using transparency.",
        ],
    },
    "edge_detection": {
        "title": "Edge Detection with Canny",
        "description": "Detect strong intensity transitions that correspond to object boundaries.",
        "goal": "Highlight structural contours that can support feature extraction or inspection workflows.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We first convert the image to grayscale and lightly smooth it to suppress noise.
Then we apply the Canny detector with lower and upper thresholds.
The result is a sparse map of likely edges, which often serves as a foundation for downstream analysis.""",
        "code_template": """# Detect edges with the Canny operator
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, threshold1=80, threshold2=180)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(gray, cmap="gray")
axes[0].set_title("Grayscale Input")
axes[0].axis("off")

axes[1].imshow(edges, cmap="gray")
axes[1].set_title("Canny Edges")
axes[1].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Canny combines smoothing, gradient estimation, and hysteresis thresholding.",
            "The two thresholds determine how aggressively faint edges are kept or rejected.",
            "Pre-blurring helps reduce false positives caused by noise.",
        ],
        "practice_prompts": [
            "Tune the two Canny thresholds and compare edge density.",
            "Run contour detection on the edge map.",
            "Overlay edges on the original image in color.",
        ],
    },
    "contour_analysis": {
        "title": "Contour Detection and Shape Analysis",
        "description": "Extract object outlines from a binary mask and draw them on the source image.",
        "goal": "Identify connected shapes and compute simple geometric summaries.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We generate a binary mask from the grayscale image as a first pass.
Then we find external contours and compute area and perimeter for the largest regions.
Finally, we draw the contours so the notebook explains both detection and interpretation.""",
        "code_template": """# Detect contours and visualize them
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

annotated = image_rgb.copy()
cv2.drawContours(annotated, contours, contourIdx=-1, color=(255, 0, 0), thickness=2)

areas = sorted((cv2.contourArea(cnt) for cnt in contours), reverse=True)[:5]
print("Largest contour areas:", areas)
print("Number of contours:", len(contours))

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(mask, cmap="gray")
axes[0].set_title("Binary Mask")
axes[0].axis("off")

axes[1].imshow(annotated)
axes[1].set_title("Contours")
axes[1].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Contours are extracted from binary structure, so mask quality is critical.",
            "Area and perimeter are lightweight geometric features for filtering shapes.",
            "This pattern is common in industrial inspection and document analysis.",
        ],
        "practice_prompts": [
            "Filter contours by minimum area to remove small artifacts.",
            "Compute bounding boxes for each contour.",
            "Approximate contours with polygons using `cv2.approxPolyDP`.",
        ],
    },
}
