"""config.py

Module
------
config.py

Description
-----------
Module for SDSS reference sample extraction to contain configuration data values

"""

# no. of samples
startingSampleSize = 300
finalSampleSize = 100

# URL for SDSS
url = ""

# file structure for save - suggest archive.filter.mag e.g. ZTF.g.13.0
filenameStructure = ""

# min/max magnitude
minMag = 13.0
maxMag = 22.0

# step size
stepMag = 0.5

# iterations (to get to a min)
cycleIter = 4
