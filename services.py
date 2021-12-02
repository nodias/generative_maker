import copy
import random

import numpy as np
import cv2 as cv
import json


def makeMeta(properties, name):
    with open('png/.properties.json') as f:
        json_p_name = json.load(f)
    with open('png/.properties_at.json') as f:
        json_pa_name = json.load(f)

    print("@MAKE_META")
    before_json = '{ "attributes" : [ '

    i = 0
    for p in properties:
        if i != 0:
            before_json = before_json + " ,"
        before_json = before_json + '{ ' \
                                    '"trait_type" : "' + json_p_name[p] + '",' \
                                                                          '"value" : "' + json_pa_name[p][
                          str(properties[p])] + '"' \
                                                ' }'
        i = i + 1

    after_json = '], ' \
                 '"description" : "The world\'s most adorable and sensitive pup.", ' \
                 '"image" : "ipfs://", ' \
                 '"edition" : ' + name + ', ' \
                                         '"name" : "CipherAssembly #' + name + '" ' \
                                                                               '}'

    meta = before_json + after_json

    with open('out/save' + name + '.json', 'w') as f:
        json.dump(json.loads(meta), f, indent=4)


def makeImage(result_properties, count, path, properties):
    for c in range(0, count):
        property_this = copy.deepcopy(properties)
        result = None;
        for p in result_properties:
            print(str(c) + '. ' + p)
            properties_path = path + '/' + p + '/' + str(result_properties[p][c]) + '.png'
            # ----- CUSTOM ----------------------------------
            if p == "0_background":
                result = cv.imread(properties_path)
            else:
                img = cv.imread(properties_path, -1)
                result = overlayImage(result, img, 0, 0)
            # ----- CUSTOM ----------------------------------
            property_this[p] = result_properties[p][c]
            print(str(c) + '. ' + str(result_properties[p][c]) + "-----------------------")
        cv.imwrite('out/save' + str(c) + '.png', result)

        # NFT 메타파일 생성
        makeMeta(property_this, str(c))


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


def randomSelect(num, property_counts, limits_count, limits, p, result_properties):
    random_num = random.randrange(0, property_counts[p])
    if limits_count[p][random_num] < limits[p][random_num]:
        # ----- CUSTOM ----------------------------------
        if p == "3_head":
            if result_properties["2_clothes"][num] == 5:
                result_properties[p].append(0)
                limits_count[p][0] = limits_count[p][0] + 1
                return
        # ----- CUSTOM ----------------------------------
        result_properties[p].append(random_num)
        limits_count[p][random_num] = limits_count[p][random_num] + 1
    else:
        randomSelect(num, property_counts, limits_count, limits, p, result_properties)
    # return limits_count
