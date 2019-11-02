import io
import os
from PIL import Image, ImageDraw
from enum import Enum

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def main():
    # Instantiates a client
    client = vision.ImageAnnotatorClient.from_service_account_json(
        'key_dont_fucking_share.json')

    # The name of the image file to annotate
    file_name = os.path.abspath('img.png')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    content_image = types.Image(content=content)
    image = Image.open(file_name)

    # Performs label detection on the image file
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation

    bounds = get_document_bounds(response, FeatureType.PARA, document)
    img = draw_boxes(image, bounds, 'yellow')
    img.show()


def draw_boxes(image, bounds, color, width=5):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y], fill=color, width=width)
    return image


def get_document_bounds(response, feature, document):
    bounds = []
    for i, page in enumerate(document.pages):
        for block in page.blocks:
            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)
            for paragraph in block.paragraphs:
                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)
                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)
    return bounds


if __name__ == '__main__':
    main()
