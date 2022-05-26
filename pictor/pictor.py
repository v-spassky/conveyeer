import pyx
import math
from . import pictorConfig

"""
This module is intended for creating electrical marking document 
in PDF format based on given list of items. The draw_marking() function 
does the heavy lifting and meant to be used in external modules 
like shown in .example/demo.py. Everything else is internal.
"""


def _get_text_width_mm(
    text: str,
    config: pictorConfig,
) -> float:
    """
    Returns the width of a given text string in given font size in mm.
    """

    return (
        len(text)
        *
        config.MARKING_ITEM_FONT_SIZE
        *
        config.CHARECTER_WIDTH_IN_MM_TO_FONT_SIZE_RATIO
    )


def _get_text_height_mm(
    config: pictorConfig,
) -> float:
    """
    Returns the height of a given text string in given font size in mm.
    """

    return (
        config.MARKING_ITEM_FONT_SIZE
        *
        config.TEXT_HEIGHT_IN_MM_TO_FONT_SIZE_RATIO
    )


def _select_skicker_width_mm(
    text: str,
    config: pictorConfig,
) -> int:
    """
    Returns marking item width in mm.
    """

    return math.ceil(
        _get_text_width_mm(text=text, config=config)
        +
        config.HORIZONTAL_MARGIN_FROM_TEXT_TO_SKICKER_EDGE_IN_MM
        *
        2
    )


def _evaluete_document_height_mm(
    items: list,
    config: pictorConfig,
) -> int:
    """
    Returns the height of the document in mm.
    """

    effective_document_width_mm = (
        config.DOCUMENT_WIDTH_IN_MM
        -
        config.GENERAL_DOCUMENT_PADDING_IN_MM
        *
        2
    )

    number_of_lines = 1
    current_line_length_mm = 0

    for item in items:

        sticker_and_gap_width_mm = (
            _select_skicker_width_mm(text=item, config=config)
            +
            config.HORIZONTAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM
        )

        current_line_length_mm += sticker_and_gap_width_mm

        if current_line_length_mm > effective_document_width_mm:
            number_of_lines += 1
            current_line_length_mm = 0
            current_line_length_mm += sticker_and_gap_width_mm

    return math.ceil(
        config.GENERAL_DOCUMENT_PADDING_IN_MM
        +
        number_of_lines * config.MARKING_ITEM_HEIGHT_IN_MM
        +
        (
            (number_of_lines - 1)
            *
            config.VERTICAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM
        )
        +
        config.GENERAL_DOCUMENT_PADDING_IN_MM
    )


def _line_width_exceeded(
    cursor_x_coord: float,
    next_sticker_width: float,
    config: pictorConfig,
) -> bool:
    """
    Returns True if next sticker cannot be placed on the same line.
    """

    return(
        (cursor_x_coord
         +
         next_sticker_width * 0.5)
        >
        (config.DOCUMENT_WIDTH_IN_MM
         -
         config.GENERAL_DOCUMENT_PADDING_IN_MM)
    )


def _get_rounded_rectangle_contour(
    x_center: float,
    y_center: float,
    width: float,
    height: float,
    radius: float,
) -> pyx.path.path:
    """
    Returns path instance for geometrically determined rounded rectangle.
    """

    top_left_point = (
        x_center - width / 2 + radius,
        y_center + height / 2)
    top_right_point = (
        x_center + width / 2 - radius,
        y_center + height / 2)
    right_lower_point = (
        x_center + width / 2,
        y_center - height / 2 + radius)
    bottom_right_point = (
        x_center + width / 2 - radius,
        y_center - height / 2)
    bottom_left_point = (
        x_center - width / 2 + radius,
        y_center - height / 2)
    left_upper_point = (
        x_center - width / 2,
        y_center + height / 2 - radius)

    top_right_arc_center = (
        top_right_point[0],
        top_right_point[1] - radius)
    bottom_right_arc_center = (
        bottom_right_point[0],
        bottom_right_point[1] + radius)
    bottom_left_arc_center = (
        bottom_left_point[0],
        bottom_left_point[1] + radius)
    top_left_arc_center = (
        top_left_point[0],
        top_left_point[1] - radius)

    contour = pyx.path.path(
        pyx.path.moveto(*top_left_point),
        pyx.path.lineto(*top_right_point),
        pyx.path.arcn(*top_right_arc_center, radius, 90, 0),
        pyx.path.lineto(*right_lower_point),
        pyx.path.arcn(*bottom_right_arc_center, radius, 0, 270),
        pyx.path.lineto(*bottom_left_point),
        pyx.path.arcn(*bottom_left_arc_center, radius, 270, 180),
        pyx.path.lineto(*left_upper_point),
        pyx.path.arcn(*top_left_arc_center, radius, 180, 90),
    )

    return contour


def _draw_cutting_line(
    canvas: pyx.canvas.canvas,
    x_center: float,
    y_center: float,
    width: float,
    height: float,
    radius: float,
    config: pictorConfig,
) -> None:
    ...

    cutting_lines_layer = canvas.layer('Cutting lines')

    contour = _get_rounded_rectangle_contour(
        x_center=x_center,
        y_center=y_center,
        width=width,
        height=height,
        radius=radius,
    )

    cutting_lines_layer.stroke(
        contour,
        [
            config.CUTTING_LINE_THICKNESS,
            config.CUTTING_LINE_COLOR,
        ]
    )


def _draw_marking_item(
    canvas: pyx.canvas.canvas,
    x_center: float,
    y_center: float,
    width: float,
    text: str,
    config: pictorConfig,
) -> None:
    """
    Draws a rounded rectangle on a given canvas. Canvas is modified in-place. 
    Raises ValueError if any geometric dimension is less or equal than 0. 
    Raises ValueError if radius is greater than half of the width or height. 
    Raises InvalidInputError if no canvas is given.
    """

    main_layer = canvas.layer('Main')

    radius = config.MARKING_ITEM_ROUNDING_RADIUS_IN_MM
    height = config.MARKING_ITEM_HEIGHT_IN_MM

    contour = _get_rounded_rectangle_contour(
        x_center=x_center,
        y_center=y_center,
        width=width,
        height=height,
        radius=radius,
    )

    main_layer.stroke(
        contour,
        [
            pyx.deco.filled([config.MARKING_ITEM_FILL_COLOR]),
            config.MARKING_ITEM_LINE_THICKNESS,
            config.MARKING_ITEM_TEXT_COLOR,
        ]
    )

    unicode_text_engine = pyx.text.UnicodeEngine(
        fontname=config.MARKING_ITEM_FONT_TYPE,
        size=config.MARKING_ITEM_FONT_SIZE,
    )
    main_layer.insert(
        unicode_text_engine.text(
            x_center - _get_text_width_mm(text=text,
                                          config=config) * 0.5,
            y_center - _get_text_height_mm(config=config) * 0.5,
            text,
        ))


def draw_marking(
    items: list,
    output_file_name: str,
    config: pictorConfig,
    with_cutting_lines: bool,
) -> None:
    """
    Draws marking for a given list of items in .pdf format. 
    Drawing settings (font size, colors, gap sizes etc.) 
    are configiured in pictorConfig module.
    """

    config.verify()

    pyx.unit.set(defaultunit="mm")

    canvas = pyx.canvas.canvas()

    document_height_mm = _evaluete_document_height_mm(
        items=items,
        config=config,
    )

    cursor_position = {
        'x': config.GENERAL_DOCUMENT_PADDING_IN_MM,
        'y': (
            document_height_mm
            -
            config.MARKING_ITEM_HEIGHT_IN_MM * 0.5
            -
            config.GENERAL_DOCUMENT_PADDING_IN_MM
        )
    }

    for item in items:

        width = _select_skicker_width_mm(text=item, config=config)

        cursor_position['x'] += width * 0.5

        if _line_width_exceeded(
            cursor_x_coord=cursor_position['x'],
            next_sticker_width=width,
            config=config,
        ):
            cursor_position['x'] = (
                config.GENERAL_DOCUMENT_PADDING_IN_MM
                +
                width * 0.5
            )
            cursor_position['y'] -= (
                config.MARKING_ITEM_HEIGHT_IN_MM
                +
                config.VERTICAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM
            )

        _draw_marking_item(
            canvas=canvas,
            x_center=cursor_position['x'],
            y_center=cursor_position['y'],
            width=width,
            text=item,
            config=config,
        )

        if with_cutting_lines:
            _draw_cutting_line(
                canvas=canvas,
                x_center=cursor_position['x'],
                y_center=cursor_position['y'],
                width=width + config.CUTTING_LINE_CONTOUR_PADDING_IN_MM,
                height=config.MARKING_ITEM_HEIGHT_IN_MM +
                config.CUTTING_LINE_CONTOUR_PADDING_IN_MM,
                radius=config.MARKING_ITEM_ROUNDING_RADIUS_IN_MM +
                config.CUTTING_LINE_RADIUS_PADDING_IN_MM,
                config=config,
            )

        cursor_position['x'] += (
            width * 0.5
            +
            config.HORIZONTAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM
        )

    canvas.writePDFfile(
        output_file_name,
        page_bbox=pyx.bbox.bbox(
            0, 0, config.DOCUMENT_WIDTH_IN_MM, document_height_mm),
    )
