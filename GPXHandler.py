#######################################################################################################################
#
# GPX AUDAX
#
#   File:           GPXHandler.py
#   Author:         Simon Thompson
#   Date:           4/11/2020
#   Requirements:   Python 3, gpxpy
#   Licence:        GPL v3
#   Copyright:      (c) Simon Thompson 2020
#
######################################################################################################################

# User Libraries

# Published Libraries
import gpxpy
import gpxpy.gpx

# Constants

### Classes

### Functions
def readGPXFileTracks(filename):
    '''Reads a GPX File and extracts recorded tracks'''

    print("...Read GPX File: ", filename)
    gpx_file = open(filename, 'r')

    print("...Parse GPX File")
    gpx = gpxpy.parse(gpx_file)

    print("......File contains tracks: ", len(gpx.tracks))

    return gpx



