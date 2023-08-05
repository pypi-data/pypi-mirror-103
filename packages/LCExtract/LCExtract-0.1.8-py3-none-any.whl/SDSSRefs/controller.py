"""controller.py

Module
------
controller.py

Description
-----------
Module to control the selection of 'pseudo-random' stars from SDSS database for use in definition of transient facility
intrinsic scatter / error for different magnitudes.

"""
from astroquery import sdss


def controller():
    # set config for samples

    # start iterator at min mag
    #   # get SDSS startingSamples at mag (save data)
    #   # get lightcurves for each object (save data)
    #   # analyse for scatter
    #   #   # discard bottom 20% (to reject variables and noisy observations)
    #   #   # accept if change < 10% or samples remaining <= finalSamples
    #   # repeat at next mag

    pass
