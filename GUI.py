import cv2
import numpy as np
import pydicom as pydicom
from matplotlib import pyplot as plt


class GUI:
    def __init__(self):
        self.cropped_image_plot = None
        self.original_image_plot = None
        self.segmentation_plot = None
        self.image = None
        self.plot = plt.figure()

    def load_image(self, file_path):
        if len(file_path) == 0:
            raise Exception('File argument is mandatory.')

        if file_path.split('.')[-1] != 'dcm':
            raise Exception('File must be .dcm')

        # load image
        self.dcm_image = pydicom.dcmread(file_path)
        # get pixel array
        pixel_array = self.dcm_image.pixel_array
        # window image to 0-255 bits (png standard)
        img = []
        scale = 255 / pixel_array.max()
        for row in pixel_array:
            img.append(list(map(lambda x: x * scale, row)))

        self.image = np.asarray(img).astype('uint8')

        # plot image
        self.original_image_plot.imshow(self.image)

    def crop_image(self, left, top, right, bot):
        # since image is stored as ndarray, crop is done by extracing sub-matrix
        self.image = self.image[top:bot, left:right]
        self.cropped_image_plot.imshow(self.image)

    def segmentation(self):
        # watershed segmentation algorithm based on article
        # https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_watershed/py_watershed.html
        ret, thresh = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.75 * dist_transform.max(), 255, 3)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1

        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        # converting grayscale image to RGB so we can apply watershed algorithm
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2RGB)
        markers = cv2.watershed(rgb_image, markers)
        red_rgb_code = [255, 0, 0]
        rgb_image[markers == -1] = red_rgb_code

        self.segmentation_plot.imshow(rgb_image)
        plt.title("Image after watershed")
        plt.show()

    def create_gui(self):
        self.original_image_plot = self.plot.add_subplot(131)
        self.cropped_image_plot = self.plot.add_subplot(132)
        self.segmentation_plot = self.plot.add_subplot(133)
        self.original_image_plot.title.set_text('Original image')
        self.cropped_image_plot.title.set_text('Cropped image')
        self.segmentation_plot.title.set_text('Segmentation')

    def render(self):
        plt.show()

    def get_dcm_image(self):
        return self.dcm_image
