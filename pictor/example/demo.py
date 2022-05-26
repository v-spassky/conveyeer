import pictor
import pictorConfig
import convert

"""
This file shows supposed mean of use of the module.
Input data is in ./sample_input.txt.
Result can be seen in ./sample_output.pdf.
"""

list_of_electrical_items = convert.txt2list('sample_input.txt')

drawing_config = pictorConfig.DefaultConfig()
drawing_config.HORIZONTAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM = 4
drawing_config.VERTICAL_GAP_BETWEEN_MARKING_ITEMS_IN_MM = 4

pictor.draw_marking(
    items=list_of_electrical_items,
    output_file_name=r'sample_output',
    config=drawing_config,
    with_cutting_lines=True,
)
