import os
import time
from adiutor import celery, s3, BUCKET_NAME
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

    incoming_file_temp_location = f'{os.getcwd()}/tmp/{path_to_file}'

    s3.Bucket(BUCKET_NAME).download_file(
        path_to_file,
        incoming_file_temp_location,
    )

    if _is_pdf(path_to_file):
        list_of_electrical_items = sorted(
            lector.get_electrical_items_denotations(
                path_to_file=incoming_file_temp_location,
                sought_denotations=library.gost2710_denotations(),
            )
        )
    else:
        list_of_electrical_items = convert.to_list(
            incoming_file_temp_location
        )

    logger.info(list_of_electrical_items)

    drawing_config = pictorConfig.DefaultConfig()
    output_path = f'{os.getcwd()}/tmp/marking_{task_id}.pdf'

    pictor.draw_marking(
        items=list_of_electrical_items,
        output_file_name=output_path,
        config=drawing_config,
        with_cutting_lines=True,
    )

    with open(output_path, 'rb') as f:
        marking_object = s3.Object(BUCKET_NAME, f'marking_{task_id}.pdf')
        marking_object.put(Body=f)

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
