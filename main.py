#######################################################################################################################
#
# GPX AUDAX
#
#   File:           main.py
#   Author:         Simon Thompson
#   Date:           4/11/2020
#   Requirements:   Python 3, argparse
#   Licence:        GPL v3
#   Copyright:      (c) Simon Thompson 2020
#
######################################################################################################################

# User Libraries
import GPXHandler as GPX
import GPXanalyse as analyse

# Published Libraries
import argparse

# Constants

### Classes

### Functions

def main():
    print("Audax GPX Tool")

    parser = argparse.ArgumentParser(description='Audax GPX Tool')
    parser.add_argument('GPXfilename', help='Input GPX Filename')
    args = parser.parse_args()

    gpx = GPX.readGPXFileTracks(args.GPXfilename)

    #analyse.printGPX(gpx)
    climb = analyse.calculateClimb(gpx)
    dist = analyse.getDistance(gpx)
    dist1 = analyse.calculateQuickDistance2D(gpx)


if __name__ == "__main__":
    main()
