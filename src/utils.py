import numpy as np

def put_over(image, overlay):
    alpha = overlay[:, :, 3:] / 255.0
    image[:, :, :3] = image[:, :, :3] * (1 - alpha) + overlay[:, :, :3] * alpha
    return image.astype(np.uint8)
