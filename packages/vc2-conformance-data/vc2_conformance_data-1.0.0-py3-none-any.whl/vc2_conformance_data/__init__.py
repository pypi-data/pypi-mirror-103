"""
VC-2 Conformance Data
=====================

This :py:mod:`vc2_conformance_data` module contains data files and test
pictures for use in conformance testing procedures.

You can find the source code (and data files) for
:py:mod:`vc2_conformance_data` `on GitHub
<https://github.com/bbc/vc2_conformance_data/>`_.

.. only:: not latex

    .. note::

        This documentation is also `available in PDF format
        <https://bbc.github.io/vc2_conformance_data/vc2_conformance_data_manual.pdf>`_.

.. only:: not html

    .. note::

        This documentation is also `available to browse online in HTML format
        <https://bbc.github.io/vc2_conformance_data/>`_.

Static filter analysis data
---------------------------

.. autodata:: STATIC_FILTER_ANALYSIS_BUNDLE_FILENAME
    :annotation: = "/path/to/bundle.zip"


Pictures
--------

Test pictures are provided in the raw format used by the VC-2 conformance
software (see :py:mod:`vc2_conformance.file_format`). Filenames are given for
the ``*.raw`` file, a corresponding ``*.json`` metadata file is also provided
with the same base name.

First, a synthetic test sprite:

.. autodata:: POINTER_SPRITE_FILENAME
    :annotation: = "/path/to/picture.raw"


Next, a small set of natural images (from photographs) are provided for testing
encoders and decoders on realistic picture content. The complete set of files
is enumerated in:

.. autodata:: NATURAL_PICTURES_FILENAMES
    :annotation: = ["/path/to/picture.raw", ...]

And the individual files are also named as follows:

.. autodata:: BERRIES_PICTURE_FILENAME
    :annotation: = "/path/to/picture.raw"

.. autodata:: KINGSWOOD_PICTURE_FILENAME
    :annotation: = "/path/to/picture.raw"

.. autodata:: TREES_PICTURE_FILENAME
    :annotation: = "/path/to/picture.raw"

"""

import os

from vc2_conformance_data.version import __version__


__all__ = [
    "STATIC_FILTER_ANALYSIS_BUNDLE_FILENAME",
    "POINTER_SPRITE_FILENAME",
    "BERRIES_PICTURE_FILENAME",
    "KINGSWOOD_PICTURE_FILENAME",
    "TREES_PICTURE_FILENAME",
    "NATURAL_PICTURES_FILENAMES",
]


def _full_path_to(name):
    return os.path.join(os.path.dirname(__file__), name)


STATIC_FILTER_ANALYSIS_BUNDLE_FILENAME = _full_path_to(
    "static_filter_analysis_bundle.zip"
)
"""
A :py:mod:`vc2_bit_widths` bundle containing static filter analyses for all
VC-2 codec configurations with a default quantisation matrix.
"""

POINTER_SPRITE_FILENAME = _full_path_to("pointer.raw")
"""
A 128x128 sprite with the following features:

* Saturated white triangle covering the top-left half of the sprite
* A black, perfectly circular hole cut out of the middle of the triangle.
* The letters 'VC-2' in the bottom right half of the sprite on a black
  background.
* The letters 'V', 'C', and '2' are printed in saturated primary red, green and
  blue respectively. The hyphen is printed in saturated white.
* All edges are antialiased

.. image:: /_static/pointer.png

"""


BERRIES_PICTURE_FILENAME = _full_path_to("berries.raw")
"""
A test picture of berries growing from a branch.

.. image:: /_static/berries.png

This shallow-depth-of-field image contains large amounts of low spatial
frequency content, including nearly-flat coloured areas.
"""


KINGSWOOD_PICTURE_FILENAME = _full_path_to("kingswood.raw")
"""
A test picture of a large white building amongst greenery.

.. image:: /_static/kingswood.png

This image is an example of a natural scene with broad general features and
fine detail.
"""


TREES_PICTURE_FILENAME = _full_path_to("trees.raw")
"""
A test picture of deciduous tree branches in winter against a blue sky.

.. image:: /_static/trees.png

This image contains a large amount of fine detail (i.e. high spatial frequency
content).
"""


NATURAL_PICTURES_FILENAMES = [
    BERRIES_PICTURE_FILENAME,
    KINGSWOOD_PICTURE_FILENAME,
    TREES_PICTURE_FILENAME,
]
"""
A collection of natural test pictures (photographs).
"""
