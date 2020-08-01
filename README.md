Universal Broadband for Africa
==============================

**uba** assesses the costs of universal broadband connectivity in Africa.

Using conda
==========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and
packages.

Create a conda environment called uba:

    conda create --name uba python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate uba

First, install optional packages:

    conda install geopandas sklearn contextily

Then install uba:

    python setup.py install

Alternatively, for development purposes, clone this repo and run:

    python setup.py develop


Download necessary data
=======================

You will need numerous input data sets.

First, download the Global Administrative Database (GADM), following the link below and making
sure you download the "six separate layers.":

- https://gadm.org/download_world.html

Place the data into the following path `data/raw/gadm36_levels_shp`.

Then download the WorldPop global settlement data from:

- https://www.worldpop.org/geodata/summary?id=24777.

Place the data in `data/raw/settlement_layer`.

Next, download the nightlight data here:

https://ngdc.noaa.gov/eog/data/web_data/v4composites/F182013.v4.tar

Place the unzipped data in `data/raw/nightlights/2013`.

Obtain the Mobile Coverage Explorer data from Collins Bartholomew:

https://www.collinsbartholomew.com/mobile-coverage-maps/mobile-coverage-explorer/

Place the data into `data/raw/Mobile Coverage Explorer`.

Once complete, run the following to preprocess all data:

    python scripts/preprocess.py


Using the code
==============

First make sure you have run the preprocessing script to extract the necessary files:

    python scripts/preprocess.py

Then execute:

    python scripts/run.py


Thanks for the support
======================

**uba** was written and developed at the `Environmental Change Institute, University of Oxford <http://www.eci.ox.ac.uk>`_ within the EPSRC-sponsored MISTRAL programme, as part of the `Infrastructure Transition Research Consortium <http://www.itrc.org.uk/>`_.
