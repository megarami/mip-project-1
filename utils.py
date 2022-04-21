from pprint import pprint


def get_coordinates(input_string):
    left, top, right, bottom = input_string.split(',')
    return tuple(map(lambda x: int(x), [left, top, right, bottom]))


def extract_info(dcm_image):
    headers = dict()
    header_keys = dcm_image.dir()
    for key in header_keys:
        headers[key] = dcm_image[key].repval.lstrip("'").rstrip("'")
    pprint(headers)
