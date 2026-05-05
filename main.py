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

def get_horizontal_projection_profile(image: np.ndarray, img_name: str) -> np.ndarray:
    """
    Computes the horizontal projection profile of the image.
    Returns a 1D array where each element is the sum of pixel values in that row.
    """
    # make sure to account for space in between lines
    # space between lines of text vs space between each entry
    profile = np.sum(image, axis=1)  # one value per row

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

def get_vertical_projection_profile(row_image: np.ndarray, img_name: str) -> np.ndarray:
    """
    Computes the vertical projection profile of the image.
    Returns a 1D array where each element is the sum of pixel values in that column.
    """
    # return np.sum(image, axis=0)
    ## SHOULD THIS BE A VERTICAL PROJECTION OF THE ORIGINAL IMAGE, OR THE HORIZONTAL PROJECTION?
    profile = np.sum(row_image, axis=0)  # one value per column

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

def category_tagging():
    pass

def ocr():
    pass

def to_spreadsheet():
    pass

if __name__ == "__main__":
    print("---------------------------")
    print("Welcome to Gridline OCR!")
    print("---------------------------")
    print("Please upload image to input folder and enter the filename below.")
    img_file = input("Enter image filename (with .png or .jpg!): \n")
    print(f"Processing image: {img_file}")

    image, img_name = load_image_as_grayscale(img_file)
    # print(img_name)
    print("Calculating horizontal projection profile...")
    horizontal_profile = get_horizontal_projection_profile(image, img_name)
    print("Calculating vertical projection profile...")
    vertical_profile = get_vertical_projection_profile(image, img_name)
    print("Done!")