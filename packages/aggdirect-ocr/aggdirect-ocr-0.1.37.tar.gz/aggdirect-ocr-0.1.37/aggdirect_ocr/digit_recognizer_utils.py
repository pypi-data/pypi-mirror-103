import numpy as np
import cv2
from skimage.filters import threshold_local


# skew correction
# this function behaves funny in docker
def deskew(image: np.ndarray):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC,
                             borderMode=cv2.BORDER_REPLICATE)
    return rotated


def preprocess_ROI(roi: np.ndarray, block_size: int, offset: int):
    gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
    T = threshold_local(gray, block_size, offset=offset, method="gaussian")
    thresholded = (gray > T).astype("uint8") * 255
    # thresholded = deskew(thresholded)
    return thresholded


def variance_of_laplacian(image: np.ndarray):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(image, cv2.CV_64F).var()


def cleanup_ticket_number(text: str):
    new_num = text.replace("\x0c", "")
    new_num = new_num.replace("\n", "")
    new_num = ''.join(i for i in new_num if i.isdigit())
    return new_num


def correct_orientation(im_: np.ndarray, BB: list):
    xmin, ymin, xmax, ymax = BB
    image_h, image_w = np.shape(im_)[0], np.shape(im_)[1]
    # Get BB aspect ratio
    BB_aspect_ratio = (xmax - xmin)/(ymax - ymin)
    if BB_aspect_ratio >= 1:
        # width > height, either orientation is 0 or 180 degree
        if ymin > image_h // 2 or ymax > image_h // 2:
            angle = 180  # k =2
        else:
            angle = 0
    else:
        # width < height, either orientation is 90 or 270 degree
        if xmin > image_w // 2 or xmax > image_w // 2:
            angle = 90  # k = 1
        else:
            angle = 270  # k = 3
    return angle


def add_padding_and_clip(angle: int, xmin: float, ymin: float,
                         xmax: float, ymax: float,
                         height: int, width: int):
    if angle == 0:
        startX = int(xmin-40)
        startY = int(ymin-10)
        endX = int(xmax+40)
        endY = int(ymax+20)
    elif angle == 270:
        startX = int(xmin-10)
        startY = int(ymin-40)
        endX = int(xmax+20)
        endY = int(ymax+40)
    elif angle == 180:
        startX = int(xmin-40)
        startY = int(ymin-20)
        endX = int(xmax+40)
        endY = int(ymax+10)
    elif angle == 90:
        startX = int(xmin-20)
        startY = int(ymin-40)
        endX = int(xmax+10)
        endY = int(ymax+40)

    # If padding exceeds dimension of image, clip it size
    startX = np.clip(startX, 0, height)
    startY = np.clip(startY, 0, width)
    endX = np.clip(endX, 0, height)
    endY = np.clip(endY, 0, width)
    return startX, startY, endX, endY
