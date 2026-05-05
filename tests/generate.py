import numpy as np
import cv2

def create_random_bw_image(size, filename, rowlines=None, collines=None):
    """
    Generates a tiny square image with random black or white pixels.
    Assumes standard 8-bit depth (0 or 255).
    """
    dest_name = f"{filename}.png" if not filename.endswith(".png") else filename
    filepath = f"tests/input/{filename}.png"
    # 1. Generate random binary values (0 or 1) for the 10x10 grid
    raw_pixels = np.random.randint(2, size=(size, size))

    # 2. Convert to OpenCV 8-bit image format (uint8)
    #    Binary 0 (black) stays 0.
    #    Binary 1 (white) must be converted to 255.
    image = (raw_pixels * 255).astype(np.uint8)

    if rowlines is not None:
        for row in rowlines:
            if 0 <= row < size:
                image[row, :] = 255  # Set entire row to white

    if collines is not None:
        for col in collines:
            if 0 <= col < size:
                image[:, col] = 255  # Set entire column to white

    write_success = cv2.imwrite(filepath, image)
    if write_success:
        print(f"{size}x{size} black & white test image saved as: {filepath}")
    else:
        print("Error: Failed to save image.")

    # Optional: Display the actual values to verify
    print("\nGenerated pixel array (0=Black, 255=White):")
    print(image)

if __name__ == "__main__":
    size = int(input("Enter the size of the image (e.g., 10 for 10x10): "))
    rowlines_input = input("Enter row indices to be white (comma-separated, e.g., 2,5): ")
    collines_input = input("Enter column indices to be white (comma-separated, e.g., 3,7): ")
    filename = input("Enter image destination: ")
    print(size)
    print(filename)
    rowlines = [int(x) for x in rowlines_input.split(",")] if rowlines_input else None
    collines = [int(x) for x in collines_input.split(",")] if collines_input else None
    create_random_bw_image(size, filename, rowlines=rowlines, collines=collines)