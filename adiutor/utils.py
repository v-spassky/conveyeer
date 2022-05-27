import os
import time
from adiutor import celery
from celery.utils.log import get_task_logger
from pictor import pictor, convert, pictorConfig
from lector import lector, library

"""
Defines custom utility functions used in routes.
"""

logger = get_task_logger(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'csv', 'json', 'yaml'}


def _is_pdf(file):
    """
    Checks if the file is a pdf.
    """

    return file.endswith(('.pdf', '.PDF'))


@celery.task(name='adiutor.utils.process_incoming_file')
def process_incoming_file(path_to_file):
    """
    Handles input file using custom utilities: 
    'lector' parses incoming .pdf file, extracts 
    electrocal components` denotations; 
    'pictor' draws marking document.
    """

    task_id = celery.current_task.request.id

    if _is_pdf(path_to_file):
        list_of_electrical_items = sorted(
            lector.get_electrical_items_denotations(
                path_to_file=path_to_file,
                sought_denotations=library.gost2710_denotations(),
            )
        )
    else:
        list_of_electrical_items = convert.to_list(path_to_file)

    logger.info(list_of_electrical_items)

    drawing_config = pictorConfig.DefaultConfig()
    output_path = f'{os.getcwd()}/tmp/marking_{task_id}'

    pictor.draw_marking(
        items=list_of_electrical_items,
        output_file_name=output_path,
        config=drawing_config,
        with_cutting_lines=True,
    )

    # Added a bit of delay so that loading animation plays a little longer
    time.sleep(3)


def format_is_valid(filename):
    """
    Checks if the file format is valid (application should not accept 
    any input other than listed in 'ALLOWED_EXTENSIONS').
    """

    return (
        ('.' in filename)
        and
        (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    )
