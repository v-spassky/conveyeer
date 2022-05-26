import pyx
import inspect

"""
This file contains drawing configurations class for pictor.py. 
Default settings are defined in DefaultConfig. Tweaking default settings 
can be done via modifying DefaultConfig() instance 
like shown in .example/demo.py.
"""


class DefaultConfig:
    """
    Default configuration for pictor.py.
    """

    TEXT_HEIGHT_IN_MM_TO_FONT_SIZE_RATIO = 0.2764
    CHARECTER_WIDTH_IN_MM_TO_FONT_SIZE_RATIO = 0.212

    HORIZONTAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM = 3
    VERTICAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM = 3
    DOCUMENT_WIDTH_IN_MM = 400
    GENERAL_DOCUMENT_PADDING_IN_MM = 5

    MARKING_ITEM_FONT_TYPE = r"cmss10"
    MARKING_ITEM_FONT_SIZE = 22
    MARKING_ITEM_ROUNDING_RADIUS_IN_MM = 3
    MARKING_ITEM_HEIGHT_IN_MM = 13
    HORIZONTAL_MARGIN_FROM_TEXT_TO_SKICKER_EDGE_IN_MM = 3
    MARKING_ITEM_LINE_THICKNESS = pyx.style.linewidth.THick
    MARKING_ITEM_BOUNDING_LINE_COLOR = pyx.color.rgb.black
    MARKING_ITEM_FILL_COLOR = pyx.color.cmyk.YellowOrange
    MARKING_ITEM_TEXT_COLOR = pyx.color.rgb.black

    CUTTING_LINE_THICKNESS = pyx.style.linewidth.THIN
    CUTTING_LINE_COLOR = pyx.color.rgb.green
    CUTTING_LINE_CONTOUR_PADDING_IN_MM = 0.6
    CUTTING_LINE_RADIUS_PADDING_IN_MM = (
        CUTTING_LINE_CONTOUR_PADDING_IN_MM
        *
        0.5
    )

    def _attribute_is_config_value(self, attr_name, attr_value):
        """
        Checks if given attribute is a config value 
        judjing by ist name and value. Used in verify() method.
        """

        return (
            (not attr_name.startswith('_'))
            and
            (not inspect.ismethod(attr_value))
        )

    def verify(self):
        """
        Verifies a config agains a set of conditions:
        - all geometrical dimensions must be greater than zero;
        - rounding radius must be less than half of either width or height.

        Raises exception if any of the conditions is not met.
        """

        for attr_name, attr_value in inspect.getmembers(self):
            if self._attribute_is_config_value(attr_name, attr_value):
                if isinstance(attr_value, (int, float)) and attr_value <= 0:
                    raise ValueError(
                        f'{attr_name} must be greater than zero.'
                    )

        if (
            self.MARKING_ITEM_ROUNDING_RADIUS_IN_MM
            >
            self.MARKING_ITEM_HEIGHT_IN_MM * 0.5
        ):
            raise ValueError(
                """Rounding radius must be less than 
                half of either width or height."""
            )


class ProductionConfig_v1(DefaultConfig):
    """
    Custom configuration for pictor.py. 
    All possible changes should be implemented in child class like this one.
    """
    ...
