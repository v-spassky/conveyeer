import os
from lector import lector
from lector import library
from lector import croppingConfig

cropping_config = croppingConfig.DefaultA4CroppingConfig()
cropping_config.LEFT_OFFSET_TO_DOCUMENT_WIDTH_RATIO = 0.08

items = lector.get_set_of_electrical_items_denotations(
    path_to_file=f'{os.getcwd()}/examples/sample_pdf_input.pdf',
    sought_denotations=library.gost2710_denotations_with_added({'XT_'}),
    cropping_config=cropping_config,
)
