import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from datetime import datetime
import re

def load_image_as_grayscale(im_name: str) -> np.ndarray:
    """
    Loads a JPG or PNG image and converts it to a 2D numpy array
    of grayscale values between 0.0 (white) and 1.0 (black).
    NOTE that black and white values are inverted than in standard cv images

    Returns: A 2D numpy array of shape (height, width) with float32 values in [0.0, 255.0] and the image name
    """
    # img = Image.open(filepath).convert("L")  # "L" mode = grayscale
    # matrix = np.array(img, dtype=np.float32) / 255.0
    # return matrix
    im_name = im_name if im_name.endswith(".png") or im_name.endswith(".jpg") else f"{im_name}.png"
    im_path = os.path.join("input/", im_name)

    if not os.path.exists(im_path):
        raise Exception(f"ERROR: The file {im_path} does not exist.")
    else:
        image = cv2.imread(im_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            raise Exception("ERROR: Could not read image")
        else:
            print(f"Image loaded. Dimensions: {image.shape}")
            inverted = 255.0 - image.astype(np.float32)
            # filename without extension and path
            stripped_name = re.split(r'[/\\]', os.path.splitext(im_name)[0])[-1]
            return (inverted, stripped_name) 
            # return image.astype(np.float32)

def get_horizontal_projection_profile(image: np.ndarray, img_name: str, dont_save=False) -> np.ndarray:
    """
    Computes the horizontal projection profile of the image.
    Returns a 1D array where each element is the sum of pixel values in that row.
    """
    # make sure to account for space in between lines
    # space between lines of text vs space between each entry
    profile = np.sum(image, axis=1)  # one value per row

    if not dont_save:
        plt.figure(figsize=(10, 4))
        plt.plot(profile)
        plt.title("Horizontal Projection Profile")
        plt.xlabel("Row index")
        plt.ylabel("Sum of pixel values")
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f"projection-profiles/{img_name}-horizontal-{timestamp}.png")
        plt.close()

    return profile

def get_vertical_projection_profile(image: np.ndarray, img_name: str, dont_save=False) -> np.ndarray:
    """
    Computes the vertical projection profile of the image.
    Returns a 1D array where each element is the sum of pixel values in that column.
    """
    # return np.sum(image, axis=0)
    ## SHOULD THIS BE A VERTICAL PROJECTION OF THE ORIGINAL IMAGE, OR THE HORIZONTAL PROJECTION?
    profile = np.sum(image, axis=0)  # one value per column

    plt.figure(figsize=(10, 4))
    plt.plot(profile)
    plt.title("Vertical Projection Profile")
    plt.xlabel("Column index")
    plt.ylabel("Sum of pixel values")
    plt.tight_layout()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"projection-profiles/{img_name}-vertical-{timestamp}.png")
    plt.close()

    return profile

def slice_rows(image: np.ndarray, horizontal_profile: np.ndarray, threshold=500, min_gap=5) -> list:
    """
    Uses the horizontal projection profile to slice the image horizontally where gridlines were detected,

    threshold: rows with pixel sum below this are considered empty/whitespace (can account for noise, color, or small stylistic variations)
    min_gap: minimum number of consecutive empty pixels to count as a horizontal split between entries (prevents splitting on small gaps that may exist within text/lines)

    Returns: a list of 2D numpy arrays, each being one row slice of the image
    """
    height = image.shape[0]
    is_empty = horizontal_profile < threshold  # list of booleans for each entry in horizontal profile, true if below threshold

    slices = []
    in_gap = True
    start = 0

    for i in range(height):
        if in_gap:
            # was in gap but no longer
            if not is_empty[i]:
                start = i
                in_gap = False
        else:
            # not in gap but is empty (possible gap)
            if is_empty[i]:
                # check if this gap is large enough to count as a split
                gap_length = 0
                for j in range(i, min(i + min_gap, height)):
                    if is_empty[j]:
                        gap_length += 1

                if gap_length >= min_gap:
                    # large enough gap detected, make slice
                    slices.append(image[start:i, :])
                    in_gap = True

    # catch the last entry if the image doesn't end with whitespace
    if not in_gap:
        slices.append(image[start:height, :])

    print(f"Found {len(slices)} row slices.")
    return slices

def category_tagging():
    pass

def ocr():
    pass

def to_spreadsheet():
    pass

def process_image(img_file: str, test=False) -> list:
    """
    Main processing function that can be called programmatically.
    
    Args:
        img_file: Image filename (can include subdirectory like "setA/vocab-page-A1")
        min_gap: Minimum gap size for row slicing
        
    Returns:
        List of row slices as numpy arrays
    """
    print(f"Processing image: {img_file}")

    image, img_name = load_image_as_grayscale(img_file)

    print("Calculating horizontal projection profile...")
    horizontal_profile = get_horizontal_projection_profile(image, img_name, test)
    # print("Calculating vertical projection profile...")
    # vertical_profile = get_vertical_projection_profile(horizontal_profile, img_name)

    # find background color to set as threshold for slicing rows (good for image with non-white backgrounds)
    background_color = np.percentile(horizontal_profile, 60)
    threshold = max(background_color+300, 500)
    gap = 5
    print("threshold:", threshold)
    print("gap:", gap)
    print(horizontal_profile)

    print("Slicing rows...")
    row_slices = slice_rows(image, horizontal_profile, threshold, gap)

    # save each slice to slices folder
    for idx, s in enumerate(row_slices):
        cv2.imwrite(f"slices/{img_name}_row_{idx}.png", (255.0 - s).astype(np.uint8)) # un-invert black and white values
    print("Done!")
    
    return row_slices

if __name__ == "__main__":
    print("---------------------------")
    print("Welcome to Gridline OCR!")
    print("---------------------------")
    print("Please upload image to input folder and enter the filename below.")
    img_file = input("Enter image filename (with .png or .jpg!): \n")
    process_image(img_file)