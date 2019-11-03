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
    WORD = 5
    SYMBOL = 5


def main():
    # Instantiates a client
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'main_key.json'
    client = vision.ImageAnnotatorClient()
    # The name of the image file to annotate
    file_name = os.path.abspath('main_test3.jpg')

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
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)
                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)
    return bounds


def textedit():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'main_key.json'
    client = vision.ImageAnnotatorClient()

    IMAGE_FILE = 'main_test1.jpg'

    with io.open(IMAGE_FILE, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    docText = response.full_text_annotation.text
    return docText


f = open("text_edit.txt", "w+")
f.write(textedit())
f.close()

f = open("text_edit.txt","r")
a = []
c = []
dict = {}
f1 = f.readline()
while f1:
    if ':' in f1 or ';' in f1:
        a.append(f1)
    f1 = f.readline()
f.close()
b = []
for each in a:
    x = each[:-2]
    b.append(x)
print(b)
# f = open("text_edit.txt","r")
# c = []
# f2 = f.readline()
# while f2:
#     if ':' not in f2:
#         c.append(f2)
#     f2 = f.readline()
# f.close()
# d = []
# for each in c:
#     x = each[:-1]
#     d.append(x)
# for i in range(len(b)):
#     dict[b[i]] = d[i]

if __name__ == '__main__':
    main()
