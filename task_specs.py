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
    "box_and_bilateral_blur": {
        "title": "Box Blur and Bilateral Filtering",
        "description": "Compare a simple averaging blur with edge-preserving bilateral filtering.",
        "goal": "Smooth noisy regions while learning how different blur algorithms affect edges and fine detail.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We start with a box blur, which replaces each pixel with the average of a local neighborhood.
Then we apply a bilateral filter, which smooths similar pixels while preserving stronger intensity changes.
Viewing the results side by side makes it easier to see why bilateral filtering is often preferred near object boundaries.""",
        "code_template": """# Compare averaging blur with bilateral filtering
box_blur = cv2.blur(image_rgb, (9, 9))
bilateral = cv2.bilateralFilter(image_rgb, d=9, sigmaColor=60, sigmaSpace=60)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(image_rgb)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(box_blur)
axes[1].set_title("Box Blur")
axes[1].axis("off")

axes[2].imshow(bilateral)
axes[2].set_title("Bilateral Filter")
axes[2].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "A box blur is fast and simple but tends to wash out edges.",
            "Bilateral filtering is slower but usually keeps boundaries sharper.",
            "This comparison is useful when you need denoising without losing important structure.",
        ],
        "practice_prompts": [
            "Increase the box kernel size and compare edge softness.",
            "Tune `sigmaColor` and `sigmaSpace` for stronger or weaker bilateral smoothing.",
            "Test both filters before running edge detection.",
        ],
    },
    "sharpening_filters": {
        "title": "Image Sharpening with Kernels and Unsharp Masking",
        "description": "Enhance edges and local contrast using classic sharpening operations.",
        "goal": "Create a sharper image while understanding the tradeoff between detail enhancement and noise amplification.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We first apply a custom sharpening kernel to emphasize local intensity changes.
Then we build an unsharp mask by subtracting a blurred version from the original image.
Comparing both outputs shows that sharpening can be implemented either as convolution or as detail boosting.""",
        "code_template": """# Sharpen the image with a kernel and an unsharp mask
kernel = np.array([
    [0, -1, 0],
    [-1, 5, -1],
    [0, -1, 0],
], dtype=np.float32)

sharpened_kernel = cv2.filter2D(image_rgb, ddepth=-1, kernel=kernel)
gaussian = cv2.GaussianBlur(image_rgb, (0, 0), sigmaX=2.0)
sharpened_unsharp = cv2.addWeighted(image_rgb, 1.6, gaussian, -0.6, 0)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].imshow(image_rgb)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(sharpened_kernel)
axes[1].set_title("Kernel Sharpening")
axes[1].axis("off")

axes[2].imshow(sharpened_unsharp)
axes[2].set_title("Unsharp Mask")
axes[2].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Sharpening increases local contrast, which can make boundaries appear crisper.",
            "Unsharp masking is built by subtracting a blurred version from the original image.",
            "Over-sharpening can emphasize noise and create halos around strong edges.",
        ],
        "practice_prompts": [
            "Change the kernel weights to make sharpening more or less aggressive.",
            "Tune the blur radius and blending weights in the unsharp mask.",
            "Apply sharpening after denoising and compare the result.",
        ],
    },
    "morphology_operations": {
        "title": "Morphological Operations for Cleanup",
        "description": "Use erosion, dilation, opening, and closing to refine binary image masks.",
        "goal": "Clean up small artifacts and repair fragmented foreground regions after segmentation.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We start by generating a binary mask from the grayscale image.
Then we apply erosion and dilation to see how binary shapes shrink and grow.
Finally, we compare opening and closing, which are standard cleanup operations for removing noise or filling small gaps.""",
        "code_template": """# Use morphology to clean up a thresholded mask
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = np.ones((5, 5), dtype=np.uint8)

eroded = cv2.erode(mask, kernel, iterations=1)
dilated = cv2.dilate(mask, kernel, iterations=1)
opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

fig, axes = plt.subplots(1, 5, figsize=(20, 4))
axes[0].imshow(mask, cmap="gray")
axes[0].set_title("Original Mask")
axes[0].axis("off")

axes[1].imshow(eroded, cmap="gray")
axes[1].set_title("Erosion")
axes[1].axis("off")

axes[2].imshow(dilated, cmap="gray")
axes[2].set_title("Dilation")
axes[2].axis("off")

axes[3].imshow(opened, cmap="gray")
axes[3].set_title("Opening")
axes[3].axis("off")

axes[4].imshow(closed, cmap="gray")
axes[4].set_title("Closing")
axes[4].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Erosion removes small white regions and thins larger ones.",
            "Dilation expands white regions and can reconnect separated components.",
            "Opening removes small specks, while closing fills small holes and gaps.",
        ],
        "practice_prompts": [
            "Change the kernel shape or size and inspect the effect.",
            "Run contour detection before and after cleanup.",
            "Apply opening twice to see how aggressive cleanup changes the mask.",
        ],
    },
    "gradient_emboss": {
        "title": "Laplacian, Sobel, and Emboss-Style Filtering",
        "description": "Explore derivative-based filters and a stylized emboss effect.",
        "goal": "Highlight directional structure and learn how convolution kernels can emphasize texture and relief.",
        "libraries": ["OpenCV", "NumPy", "Matplotlib"],
        "walkthrough": """We compute Sobel gradients to measure horizontal and vertical intensity changes.
Then we apply the Laplacian operator to capture second-order detail.
Finally, we use an emboss-style kernel to create a relief effect that makes texture direction easier to see.""",
        "code_template": """# Apply derivative filters and an emboss kernel
gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
laplacian = cv2.Laplacian(gray, cv2.CV_64F)

emboss_kernel = np.array([
    [-2, -1, 0],
    [-1, 1, 1],
    [0, 1, 2],
], dtype=np.float32)
emboss = cv2.filter2D(gray, ddepth=-1, kernel=emboss_kernel)
emboss = cv2.convertScaleAbs(emboss + 128)

fig, axes = plt.subplots(1, 4, figsize=(18, 5))
axes[0].imshow(np.abs(sobel_x), cmap="gray")
axes[0].set_title("Sobel X")
axes[0].axis("off")

axes[1].imshow(np.abs(sobel_y), cmap="gray")
axes[1].set_title("Sobel Y")
axes[1].axis("off")

axes[2].imshow(np.abs(laplacian), cmap="gray")
axes[2].set_title("Laplacian")
axes[2].axis("off")

axes[3].imshow(emboss, cmap="gray")
axes[3].set_title("Emboss Effect")
axes[3].axis("off")

plt.tight_layout()
plt.show()
""",
        "solution_notes": [
            "Sobel filters reveal directional gradients, which are useful for structure analysis.",
            "The Laplacian responds strongly to rapid intensity change in any direction.",
            "Embossing is a stylized convolution that creates a raised-surface appearance.",
        ],
        "practice_prompts": [
            "Combine Sobel X and Sobel Y into a gradient magnitude image.",
            "Try larger derivative kernels to change sensitivity.",
            "Colorize the emboss output by blending it with the original image.",
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
