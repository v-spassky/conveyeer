import re
import slate3k
import PyPDF2
from . import library
from . import croppingConfig

"""
This module provides a function get_electrical_items_denotations() 
that parses a given .pdf file and returns a list of 
electrical items denotations in this file. All other functions 
are used internally by that function and aren`t meant for outside usage.
"""


def _regex_from_set(denotations: set) -> str:
    """
    Returns a regex string for given set of electrical items denotations.
    This regex is used to parse .pdf`s text content.
    """

    items_enumeration = f"(?:{'|'.join(denotations)})"

    item_denotoaion_normal = f'{items_enumeration}[0-9]+'
    item_denotoaion_with_a_dot = items_enumeration + r'[0-9]+\.[0-9]+'
    item_denotoaion_with_an_underscore = '[A-Z]+[0-9]+_[A-Z]+[0-9]+'

    range_of_items = '[A-Z]+[0-9]+...[A-Z]+[0-9]+'
    range_of_items_dotted = '[A-Z]+[0-9]+.[0-9]+...[A-Z]+[0-9]+.[0-9]+'

    regexes = [
        item_denotoaion_with_an_underscore,
        item_denotoaion_with_a_dot,
        item_denotoaion_normal,
        range_of_items_dotted,
        range_of_items,
    ]

    return "(" + ")|(".join(regexes) + ")"


def _crop_pdf(
    path_to_input: str,
    path_to_output: str,
    cropping_config=croppingConfig.DefaultA4CroppingConfig()
) -> None:
    """
    Crops the PDF file so that only the column 
    with electrical items denotations left.
    """

    with open(path_to_input, "rb") as input_file:
        input = PyPDF2.PdfFileReader(input_file)
        output = PyPDF2.PdfFileWriter()

        number_of_pages = input.getNumPages()

        page_width = input.getPage(0).mediaBox[2].as_numeric()
        page_height = input.getPage(0).mediaBox[3].as_numeric()

        crop_area_upper_left_point = {
            'x': (
                page_width
                *
                cropping_config.LEFT_OFFSET_TO_DOCUMENT_WIDTH_RATIO
            ),
            'y': (
                page_height
                *
                cropping_config.TOP_OFFSET_TO_DOCUMENT_HEIGHT_RATIO
            ),
        }
        crop_area_width = (
            page_width
            *
            cropping_config.CROP_AREA_WIDTH_TO_DOCUMENT_WIDTH_RATIO
        )
        crop_area_height = (
            page_height
            *
            cropping_config.CROP_AREA_HEIGHT_TO_DOCUMENT_HEIGHT_RATIO
        )

        page_original_upper_left_point = {
            'x': input.getPage(0).cropBox.getUpperLeft()[0].as_numeric(),
            'y': input.getPage(0).cropBox.getUpperLeft()[1].as_numeric(),
        }

        new_upper_left_point = (
            (
                page_original_upper_left_point['x']
                +
                crop_area_upper_left_point['x']
            ),
            (
                page_original_upper_left_point['y']
                -
                crop_area_upper_left_point['y']
            ),
        )
        new_lower_right_point = (
            new_upper_left_point[0] + crop_area_width,
            new_upper_left_point[1] - crop_area_height,
        )

        for i in range(number_of_pages):
            page = input.getPage(i)
            page.cropBox.upperLeft = new_upper_left_point
            page.cropBox.lowerRight = new_lower_right_point
            output.addPage(page)

        with open(path_to_output, "wb") as output_file:
            output.write(output_file)


def get_electrical_items_denotations(
    path_to_file: str,
    sought_denotations: set,
    crop=True,
    cropping_config=croppingConfig.DefaultA4CroppingConfig()
) -> set:
    """
    Extracts electrical items denotations from given .pdf file.
    """

    if crop:
        _crop_pdf(
            path_to_input=path_to_file,
            path_to_output=f'{path_to_file[:-4]}_cropped.pdf',
            cropping_config=cropping_config,
        )
        path_to_file = f'{path_to_file[:-4]}_cropped.pdf'

    with open(path_to_file, 'rb') as file:
        pdf = slate3k.PDF(file)

    res = set()

    sought_regex = _regex_from_set(sought_denotations)

    for page in pdf:

        matches = re.findall(sought_regex, page)

        for match in matches:
            res.update(match)

        res.discard('')

    return res
