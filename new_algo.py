import io
import os
# import pandas as pd
from random import randint

import numpy

from PIL import Image, ImageDraw
from enum import Enum

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

FUCKING_EPSILON = 20


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def main():
    # Instantiates a client
    client = vision.ImageAnnotatorClient.from_service_account_json(
        'main_key.json')

    # The name of the image file to annotate
    file_name = os.path.abspath('main_test3.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    content_image = types.Image(content=content)
    img = Image.open(file_name)

    img_size = img.size
    print(img_size)

    # Performs label detection on the image file
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation
    print(document)

    word_bounds = get_document_bounds(FeatureType.WORD, document)
    block_bounds = get_document_bounds(FeatureType.BLOCK, document)

    print(word_bounds[0])

    kv = get_key_value(block_bounds, word_bounds)
    for i in range(len(kv)):
        # loop for every pair of block, and 2 lists of its words: header and body
        block, vals = kv[i]

        # make the fucking folder if doesnt exist
        if not os.path.exists("output"):
            os.makedirs("output")

        key_img = img.crop(capture_boxes(vals[0]))
        value_img = img.crop(capture_boxes(vals[1]))

        key_img.save("output/key%d.jpeg" % i, format="JPEG")
        value_img.save("output/value%d.jpeg" % i, format="JPEG")

        img = draw_boxes(img, [block], 'red')
        img = draw_box(img, capture_boxes(vals[0]), 'yellow')
        img = draw_box(img, capture_boxes(vals[1]), 'blue')

    img.save("output/hole.jpeg", format="JPEG")
    img.show()


def draw_box(img, box, color, width=4):
    if box is not None:
        draw = ImageDraw.Draw(img)
        draw.line([
            box[0], box[1],
            box[0], box[3],
            box[2], box[3],
            box[2], box[1],
            box[0], box[1]], fill=color, width=width)
    return img


def capture_boxes(boxes):
    x1mins = [min(b.vertices[0].x, b.vertices[3].x) for b in boxes]
    y1mins = [min(b.vertices[0].y, b.vertices[1].y) for b in boxes]
    x2mins = [max(b.vertices[2].x, b.vertices[1].x) for b in boxes]
    y2mins = [max(b.vertices[2].y, b.vertices[3].y) for b in boxes]
    if not (x1mins and x2mins and y1mins and y2mins):
        return None
    x1 = min(x1mins)
    y1 = min(y1mins)
    x2 = max(x2mins)
    y2 = max(y2mins)

    return x1, y1, x2, y2


def get_key_value(block_bounds, word_bounds):
    kv = []
    for block in block_bounds:

        x1 = min(block.vertices[0].x, block.vertices[3].x)
        y1 = min(block.vertices[0].y, block.vertices[1].y)
        x2 = max(block.vertices[2].x, block.vertices[1].x)
        y2 = max(block.vertices[2].y, block.vertices[3].y)

        words = ([], [])
        lowest_y = 9999999999

        for word in word_bounds:
            if word.vertices[0].y < lowest_y and y1 - FUCKING_EPSILON <= word.vertices[0].y <= y2 + FUCKING_EPSILON:
                lowest_y = word.vertices[0].y

        for word in word_bounds:
            if x1 <= word.vertices[0].x <= x2 and y1 <= word.vertices[0].y <= y2:
                if lowest_y - FUCKING_EPSILON <= word.vertices[0].y <= lowest_y + FUCKING_EPSILON:
                    words[0].append(word)
                else:
                    words[1].append(word)
        kv.append((block, words))
    return kv


def draw_boxes(image, bounds, color, width=4):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y], fill=color, width=width)
    return image


def get_document_bounds(feature, document):
    bounds = []
    if feature == FeatureType.BLOCK:
        for i, page in enumerate(document.pages):
            for block in page.blocks:
                bounds.append(block.bounding_box)

    if feature == FeatureType.WORD:
        for i, page in enumerate(document.pages):
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        if feature == FeatureType.WORD:
                            bounds.append(word.bounding_box)
    return bounds


# def get_document_bounds(feature, document):
#     bounds = []
#     for i, page in enumerate(document.pages):
#         for block in page.blocks:
#             if feature == FeatureType.BLOCK:
#                 bounds.append(block.bounding_box)
#             for paragraph in block.paragraphs:
#                 if feature == FeatureType.PARA:
#                     bounds.append(paragraph.bounding_box)
#                 for word in paragraph.words:
#                     for symbol in word.symbols:
#                         if feature == FeatureType.SYMBOL:
#                             bounds.append(symbol.bounding_box)
#                     if feature == FeatureType.WORD:
#                         bounds.append(word.bounding_box)
#     return bounds


if __name__ == '__main__':
    main()
