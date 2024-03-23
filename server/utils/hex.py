from typing import List

from config import (
    CAMERA_WIDTH,
    CAMERA_HEIGHT
)


def convert_hex_to_maxtrix_image(string: str) -> List[List[int]]:
    """
    Convert a hex string to a list of lists of integers.

    Parameters:
        string (str): A string of hex values.

    Returns:
        List[List[int]]: A list of lists of integers (0-255).
    """

    hex_values = string.split(",")
    pixels = [int(hex_value, 16) for hex_value in hex_values]

    total_pixels_needed = CAMERA_WIDTH * CAMERA_HEIGHT

    if len(pixels) < total_pixels_needed:
        last_pixel = pixels[-1] if pixels else 0
        pixels.extend([last_pixel] * (total_pixels_needed - len(pixels)))

    image = [pixels[i * CAMERA_WIDTH:(i + 1) * CAMERA_WIDTH] for i in range(CAMERA_HEIGHT)]

    return image
