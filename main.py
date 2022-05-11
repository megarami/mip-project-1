import getopt
import sys

from GUI import GUI
from utils import get_coordinates, extract_info

if __name__ == '__main__':
    arguments = sys.argv[1:]
    options = 'f:c:se'
    long_options = ['file=', 'crop=', 'segmentation', 'extraction']
    gui = GUI()
    try:
        arguments, options = getopt.getopt(arguments, options, long_options)
        gui.create_gui(arguments)
        for argument, value in arguments:
            if argument == '-f':
                gui.load_image(value)

            if argument == '-c':
                left, top, right, bot = get_coordinates(value)
                gui.crop_image(left, top, right, bot)

            if argument == '-s':
                gui.segmentation()
            if argument == '-e':
                extract_info(gui.get_dcm_image())
        gui.render()
    except Exception as e:
        print(e)
        sys.exit(1)
