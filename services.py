import numpy as np
import cv2 as cv


def makeImage(properties, count, path):
    for c in range(0, count):
        result = None;
        for p in properties:
            print(str(c) + '. ' + p)
            properties_path = path + '/' + p + '/' + str(properties[p][c]) + '.png'
            if p == "background":
                result = cv.imread(properties_path)
            else:
                img = cv.imread(properties_path, -1)
                result = overlayImage(result, img, 0, 0)
            print(str(c) + '. ' + p + "-----------------------")
        cv.imwrite('out/save' + str(c) + '.png', result)


def overlayImage(background, overlay, x, y):
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype) * 255
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y + h, x:x + w] = (1.0 - mask) * background[y:y + h, x:x + w] + mask * overlay_image

    return background
