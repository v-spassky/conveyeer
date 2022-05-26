
"""
This module contains dataclessed used to configure 
the workflow of lector._crop_pdf() function.
"""


class DefaultA4CroppingConfig:
    """
    Dataclass with default cropping configurations. 
    All custom classes are meant to inherit from this class 
    so that no setting is missed.
    """

    LEFT_OFFSET_TO_DOCUMENT_WIDTH_RATIO = 0.084
    CROP_AREA_WIDTH_TO_DOCUMENT_WIDTH_RATIO = 0.11765
    TOP_OFFSET_TO_DOCUMENT_HEIGHT_RATIO = 0.0118765
    CROP_AREA_HEIGHT_TO_DOCUMENT_HEIGHT_RATIO = 0.9145


class CustomA4CroppingConfig_v1(DefaultA4CroppingConfig):
    """
    Custom configs may be implemented like this.
    """
    ...
