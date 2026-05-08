import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from datetime import datetime
import re
import warnings
from enum import Enum

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

def get_horizontal_projection_profile(image: np.ndarray, img_name: str, save_profiles=True) -> np.ndarray:
    """
    Computes the horizontal projection profile of the image.
    Returns a 1D array where each element is the sum of pixel values in that row.
    """
    # make sure to account for space in between lines
    # space between lines of text vs space between each entry
    profile = np.sum(image, axis=1)  # one value per row

    if save_profiles:
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

def get_vertical_projection_profile(image: np.ndarray, img_name: str, save_profiles=True) -> np.ndarray:
    """
    Computes the vertical projection profile of the image.
    Returns a 1D array where each element is the sum of pixel values in that column.
    """
    # return np.sum(image, axis=0)
    ## SHOULD THIS BE A VERTICAL PROJECTION OF THE ORIGINAL IMAGE, OR THE HORIZONTAL PROJECTION?
    profile = np.sum(image, axis=0)  # one value per column

    if save_profiles:
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

def normalize_profile(profile: np.ndarray, img_name: str, save_profiles=True) -> np.ndarray:
    """
    Normalizes a projection profile to the range [0.0, 1.0] based on its own min and max values.
    This makes it more robust to different backgrounds and resolutions.
    """
    p_min = np.percentile(profile, 5)  # 5th percentile to account for outliers (ex: A1 - rim of white, see A1 projection profile)
    p_max = np.percentile(profile, 95)
    normalized = (profile - p_min) / (p_max - p_min + 1e-6)
    normalized = np.clip(normalized, 0.0, 1.0) # sets outliers to 0 or 1 instead of negative or above 1 (kinda like ReLu)
    
    if save_profiles:
        plt.figure(figsize=(10, 4))
        plt.plot(normalized)
        plt.title("Normalized Horizontal Projection Profile")
        plt.xlabel("Row index")
        plt.ylabel("Normalized sum of pixel values")
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f"projection-profiles/{img_name}-normalized-horizontal-{timestamp}.png")
        plt.close()

    return normalized

def estimate_threshold_and_gap(horizontal_profile: np.ndarray) -> tuple[float, int]:
    """
    Dynamically estimates threshold and min_gap by normalizing the profile
    to its own range, making it robust to different backgrounds and resolutions.
    """
    # normalize profile to 0-1 range based on its own min and max
    # p_min = np.min(horizontal_profile)
    # p_max = np.max(horizontal_profile)
    p_min = np.percentile(horizontal_profile, 5)  # 5th percentile to account for outliers (ex: A1)
    p_max = np.percentile(horizontal_profile, 95)
    normalized = (horizontal_profile - p_min) / (p_max - p_min + 1e-6)
    normalized = np.clip(normalized, 0.0, 1.0) # sets outliers to 0 or 1 instead of negative or above 1 (kinda like ReLu)

    # row must be at least 20% above normalized signal to be considered not a gap
    threshold_normalized = 0.20

    # set threshold (multiply by p_max-p_min to convert back to original scale)
    threshold = p_min + threshold_normalized * (p_max - p_min)

    # estimate gap from the normalized profile
    is_empty = normalized < threshold_normalized  # boolean array
    gap_lengths = [] # list of lengths of consecutive True values in is_empty
    count = 0
    for val in is_empty:
        if val:
            count += 1
        else:
            if count > 0:
                gap_lengths.append(count)
                count = 0
    if count > 0:
        gap_lengths.append(count)

    if len(gap_lengths) == 0:
        min_gap = 3
        warnings.warn("No gaps detected in profile. Defaulting to min_gap=3.")
    else:
        # use 25th percentile of gap lengths (account for gap between lines within same entry)
        min_gap = max(2, int(np.percentile(gap_lengths, 25)))

    print(f"Normalized threshold: {threshold:.1f}, min_gap: {min_gap}")
    return threshold, min_gap

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

                    # TODO add 5px buffer
                    slices.append(image[start:i, :])
                    in_gap = True

    # catch the last entry if the image doesn't end with whitespace
    if not in_gap:
        slices.append(image[start:height, :])

    print(f"Found {len(slices)} row slices.")
    return slices

def detect_entry_boundaries(norm_horizontal_profile_left: np.ndarray, norm_horizontal_profile_right: np.ndarray, norm_horizontal_profile_full: np.ndarray) -> list[int]:
    """
    Uses the horizontal projection profiles of the left and right halves of the image
    to detect the row indices where each vocabulary entry begins.
    
    Returns a tuple of two elements:
    - a list of row indices where each entry begins
    - a list of row indices where each entry ends
    """
    is_empty_left = norm_horizontal_profile_left < 0.01
    is_empty_right = norm_horizontal_profile_right < 0.01
    is_empty_full = norm_horizontal_profile_full < 0.01

    def is_gap(row_idx, profile_type):
        if profile_type == ProfileType.LEFT:
            return is_empty_left[row_idx]
        elif profile_type == ProfileType.RIGHT:
            return is_empty_right[row_idx]
        elif profile_type == ProfileType.FULL:
            return is_empty_full[row_idx]
        
    def is_content(row_idx, profile_type):
        if profile_type == ProfileType.LEFT:
            return not is_empty_left[row_idx]
        elif profile_type == ProfileType.RIGHT:
            return not is_empty_right[row_idx]
        elif profile_type == ProfileType.FULL:
            return not is_empty_full[row_idx]

    ### STEP 1: get entry boundaries based on left normalized profile ###

    entry_starts = []  # list of row indices where entry start (transition from GAP to CONTENT in is_empty_left)
    entry_ends = []    # list of row indices where entry end (transition from CONTENT to GAP in is_empty_left)

    # edge case page starts with an entry (no leading gap)
    if is_content(0, ProfileType.LEFT):
        entry_starts.append(0)

    for i in range(1, len(is_empty_left)):
        # gap to content transition
        if is_gap(i-1, ProfileType.LEFT) and is_content(i, ProfileType.LEFT):
            entry_starts.append(i)
        # content to gap transition
        elif is_content(i-1, ProfileType.LEFT) and is_gap(i, ProfileType.LEFT):
            entry_ends.append(i)
    
    # ends with content (no gap at page bottom), add unmatched end
    if is_content(-1, ProfileType.LEFT):
        entry_ends.append(len(is_empty_left) - 1)

    assert len(entry_starts) - len(entry_ends) == 0, f"Mismatched entry starts and ends. Starts: {len(entry_starts)}, Ends: {len(entry_ends)}"

    ### STEP 2: remove stylistic elements, such as horizontal separator lines ###
    # remove stylistic elements (content with height < 10px)
    height_threshold = 10
    filtered_entry_starts = []
    filtered_entry_ends = []
    min_entry_height = float('inf')

    for start, end in zip(entry_starts, entry_ends):
        height = end-start
        if height >= height_threshold:
            filtered_entry_starts.append(start)
            filtered_entry_ends.append(end)
            min_entry_height = min(min_entry_height, height)

    ### STEP 3: adjust entry end boundaries ###
    # look at left, right, and full horizontal profile, and go back from the start of the next entry 
    # until we hit content in either profile to find the true end of the current entry (accounts for multi-line translations)

    for i in range(1, len(filtered_entry_starts)):
        start = filtered_entry_starts[i]
        end = filtered_entry_ends[i]
        next_start = filtered_entry_starts[i + 1] if i + 1 < len(filtered_entry_starts) else len(is_empty_full) - 1
        
        # if the gap between this entry's end and the next entry's start is less than the smallest entry height, 
        # then no need to adjust end because there isn't enough space for overflow content
        if next_start - end < min_entry_height:
            continue

        # look back from the start of the next entry until we find content in left, right, or full profile
        buffer = 3  # buffer to account for differences between left profile (which was used to detect the starts) and the other profiles
        for j in range(next_start-buffer, end, -1):
            if is_content(j, ProfileType.LEFT) or is_content(j, ProfileType.RIGHT) or is_content(j, ProfileType.FULL):
                # found content, update entry end to this index
                updated_entry_end = j
                filtered_entry_ends[i] = updated_entry_end
                print(f"Adjusted entry {i} end from {end} to {updated_entry_end}")
                break

    # print(f"START: {filtered_entry_starts}")
    # print(f"END: {filtered_entry_ends}")
    print(f"Detected {len(filtered_entry_starts)} entry boundaries.")
    return (filtered_entry_starts, filtered_entry_ends)


def slice_rows_v2(image: np.ndarray, boundaries: tuple[list[int], list[int]], buffer=5) -> list[np.ndarray]:
    """
    Slices the image into row bands using pre-detected boundary indices.
    Each boundary marks the start of a new vocabulary entry.
    
    Returns a list of 2D numpy arrays, each being one row slice.
    """
    slices = []
    for start, end in zip(boundaries[0], boundaries[1]):
        slice_start = max(0, start - buffer)  # add buffer above
        slice_end = min(image.shape[0], end + buffer)  # add buffer below
        slices.append(image[slice_start:slice_end, :])

    print(f"Sliced into {len(slices)} row entries.")
    return slices

def category_tagging():
    pass

def ocr():
    pass

def to_spreadsheet():
    pass

def process_image(img_file: str, save_profiles=True) -> list:
    """
    Main processing function that can be called programmatically.
    
    Args:
        img_file: Image filename (can include subdirectory like "setA/vocab-page-A1")
        save_profiles: Whether to save the projection profiles
        
    Returns:
        List of row slices as numpy arrays
    """
    print(f"Processing image: {img_file}")

    image, img_name = load_image_as_grayscale(img_file)

    # print("Calculating horizontal projection profile...")
    # horizontal_profile = get_horizontal_projection_profile(image, img_name, test)
    # # print("Calculating vertical projection profile...")
    # # vertical_profile = get_vertical_projection_profile(horizontal_profile, img_name)

    # # find background color to set as threshold for slicing rows (good for image with non-white backgrounds)
    # # background_color = np.percentile(horizontal_profile, 60)
    # # threshold = max(background_color+300, 500)
    # # gap = 5

    # threshold, gap = estimate_threshold_and_gap(horizontal_profile)
    # # print("threshold:", threshold)
    # # print("gap:", gap)
    # # print(horizontal_profile)

    # print("Slicing rows...")
    # row_slices = slice_rows(image, horizontal_profile, threshold, gap)

    height, width = image.shape
    if height < 100 or width < 100:
        raise Exception("Image is too small")
    mid = width // 2

    print("Calculating projection profiles...")
    hprofile_left = get_horizontal_projection_profile(image[:, :mid], img_name + "_left", save_profiles)
    hprofile_right = get_horizontal_projection_profile(image[:, mid:], img_name + "_right", save_profiles)
    hprofile_full = get_horizontal_projection_profile(image, img_name, save_profiles)

    hnorm_profile_left = normalize_profile(hprofile_left, img_name + "_left", save_profiles)
    hnorm_profile_right = normalize_profile(hprofile_right, img_name + "_right", save_profiles)
    hnorm_profile_full = normalize_profile(hprofile_full, img_name + "_full", save_profiles)

    print("Detecting entry boundaries...")
    boundaries = detect_entry_boundaries(hnorm_profile_left, hnorm_profile_right, hnorm_profile_full)

    print("Slicing rows...")
    row_slices = slice_rows_v2(image, boundaries)

    # save each slice to slices folder
    for idx, s in enumerate(row_slices):
        cv2.imwrite(f"slices/{img_name}_row_{idx}.png", (255.0 - s).astype(np.uint8)) # un-invert black and white values
    print("Done!")
    
    return row_slices

class ProfileType(Enum):
    FULL = "full"
    LEFT = "left"
    RIGHT = "right"

if __name__ == "__main__":
    print("---------------------------")
    print("Welcome to Gridline OCR!")
    print("---------------------------")
    print("Please upload image to input folder and enter the filename below.")
    img_file = input("Enter image filename (with .png or .jpg!): \n")
    process_image(img_file, save_profiles=False)