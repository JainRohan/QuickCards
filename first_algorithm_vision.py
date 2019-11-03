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
        'main_key.json')

    # The name of the image file to annotate
    file_name = os.path.abspath('test7.jpg')

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    content_image = types.Image(content=content)
    image = Image.open(file_name)

    # Performs label detection on the image file
    response = client.document_text_detection(image=content_image)
    document = response.full_text_annotation

    bounds = get_document_bounds(response, FeatureType.PARA, document)

    # para = get_document_bounds(response, FeatureType.BLOCK, document)
    img = draw_boxes(image, bounds, 'red')
    # img = draw_boxes(img, para, 'yellow')

    img.show()


def text_edit():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'main_key.json'
    client = vision.ImageAnnotatorClient()

    # FOLDER_PATH = r'<Folder Path>'
    image_file = 'test7.jpg'
    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    doctext = response.full_text_annotation.text
    print(doctext)
    #
    # pages = response.full_text_annotation.pages
    # for page in pages:
    #     for block in page.blocks:
    #         print('block confidence:', block.confidence)
    #
    #         for paragraph in block.paragraphs:
    #             print('paragraph confidence:', paragraph.confidence)
    #
    #             for word in paragraph.words:
    #                 word_text = ''.join([symbol.text for symbol in word.symbols])
    #
    #                 print('Word text: {0} (confidence: {1}'.format(word_text, word.confidence))
    #
    #                 for symbol in word.symbols:
    #                     print('\tSymbol: {0} (confidence: {1}'.format(symbol.text, symbol.confidence))
    #

def draw_boxes(image, bounds, color, width=4):
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        draw.line([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y,
            bound.vertices[0].x, bound.vertices[0].y], fill=color, width=width)
        # for each in bounds:
        #     pass
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
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)
                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)
    return bounds


text_edit()

if __name__ == '__main__':
    main()
