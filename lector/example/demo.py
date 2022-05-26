import lector
import library
import croppingConfig

"""
This demo showcases suggested use of this package`s utilities.
"""

cropping_config = croppingConfig.DefaultA4CroppingConfig()
cropping_config.LEFT_OFFSET_TO_DOCUMENT_WIDTH_RATIO = 0.08

lector.get_electrical_items_denotations(
    path_to_file=r'example/samplePDF_v1.pdf',
    sought_denotations=library.gost2710_denotations(),
    cropping_config=cropping_config,
)
