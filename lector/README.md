# Main purpose

This package provides a utility for extracting electrical items denotations from incoming .pdf file for further drawing in [pictor](../pictor/README.md) package.

# Notes

- For now input .pdf is supposed to be formatted according to this [standard](https://library.ontu.edu.ua/assets/pdf/DSTY-GOST/2.701-2008.pdf).

# Installation

    $ clone git repo
    $ pip install -r requirements.txt

# Usage

```python
import lector
import library
import croppingConfig


cropping_config = croppingConfig.DefaultA4CroppingConfig()
cropping_config.LEFT_OFFSET_TO_DOCUMENT_WIDTH_RATIO = 0.08

lector.get_electrical_items_denotations(
    path_to_file=r'samplePDF_v1.pdf',
    sought_denotations=library.gost2710_denotations(),
    cropping_config=cropping_config,
)
```

# To do

- Parser needs improvments in general because possible variativity in items` denotations is high.
