import numpy as np
import cv2


def flatten_perspective(image):
    """
    Warps the image from the vehicle front-facing camera mapping hte road to a bird view perspective.

    Parameters
    ----------
    image       : Image from the vehicle front-facing camera.

    Returns
    -------
    Warped image.
    """
    # Get image dimensions
    (h, w) = (image.shape[0], image.shape[1])
    # Define source points
    source = np.float32([[w // 2 - w*.60, h * .6], [w // 2 + w*.60, h * .6], [0, h], [w, h]])
    # Define corresponding destination points
    destination = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    transform_matrix = cv2.getPerspectiveTransform(source, destination)
    unwarp_matrix = cv2.getPerspectiveTransform(destination, source)
    return (cv2.warpPerspective(image, transform_matrix, (w, h)), unwarp_matrix)