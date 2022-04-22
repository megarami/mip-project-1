from pprint import pprint


def get_coordinates(input_string):
    left, top, right, bottom = input_string.split(',')

    coordinates = tuple(map(lambda x: int(x), [left, top, right, bottom]))

    if coordinates[0] > coordinates[2] or coordinates[1] > coordinates[3]:
        raise Exception("Incorrect coordinates")
    for num in coordinates:
        if num < 0:
            raise Exception("Coordinates can't be negative")

    return coordinates


def extract_info(dcm_image):
    headers = dict()
    header_keys = dcm_image.dir()
    for key in header_keys:
        headers[key] = dcm_image[key].repval.lstrip("'").rstrip("'")
    pprint(headers)
