#######################################################################################################################
#
# GPX AUDAX
#
#   File:           GPXanalyse.py
#   Author:         Simon Thompson
#   Date:           4/11/2020
#   Requirements:   Python 3, math
#   Licence:        GPL v3
#   Copyright:      (c) Simon Thompson 2020
#
######################################################################################################################

# User Libraries
import libs.gpxsmooth as smooth

# Published Libraries
import math
import gpxpy
from lxml import etree

# Constants
climbMin = 0.1

### Classes

### Functions
def printGPX(gpx):
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

def calculateClimb(gpx):
    '''Calculates the total climb in a GPX file'''
    print("...Calculate Climb")

    # Variables
    firstPoint = True
    prevPoint = 0.0
    currPoint = 0.0
    climb = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if(firstPoint):
                    prevPoint = point.elevation
                    currPoint = point.elevation
                    firstPoint = False
                else:
                    currPoint = point.elevation
                    if((currPoint - prevPoint) > climbMin):
                        climb = climb + (currPoint - prevPoint)
                        #print(".........Climb: ", (currPoint - prevPoint), climb)
                    prevPoint = currPoint

    print("......Total Climb(m)", climb)
    return climb

def getDistance(gpx):
    dist = 0.0
    print("...Get Distance from GPX File")
    for track_idx, track in enumerate(gpx.tracks):
        track_length = track.length_3d()
        dist = dist + track_length
    dist = dist / 100.0
    distf = math.floor(dist)
    distf = distf / 10.0
    print("......Total Distance (km):", distf)
    return distf


def calcQuickDistancePoint(Lat1, Long1, Lat2, Long2):
    '''Calculate quick 2D distance - https://www.cartographyunchained.com/cgsta1/'''
    x = Lat2 - Lat1
    y = (Long2 - Long1) * math.cos((Lat2 + Lat1) * 0.00872664626)
    dist = 111.3 * math.sqrt(x*x + y*y)
    #print(dist)
    return dist

def calculateQuickDistance2D(gpx):
    '''Calculates the total Distance in a GPX file'''
    print("...Calculate Distance")

    # Variables
    firstPoint = True
    prevLat = 0.0
    prevLong = 0.0
    currLat = 0.0
    currLong = 0.0
    dist = 0.0

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if(firstPoint):
                    prevLat = point.latitude
                    prevLong = point.longitude
                    firstPoint = False
                else:
                    currLat = point.latitude
                    currLong = point.longitude
                    dist = dist + calcQuickDistancePoint(currLat, currLong, prevLat, prevLong)
                    prevLat = currLat
                    prevLong = currLong

    dist = 10.0 * dist
    distf = math.floor(dist)
    distf = distf / 10.0
    print("......Total Distance (km)", distf)
    return distf

def smoothGPXfile(filename, outputfilename):

    maxdistance = 50.0
    maxinterval = 100.0

    print("...Smooth GPX Track")
    with open(filename, 'r') as fh:
        root = etree.parse(fh).getroot()
        NS = "{" + root.nsmap[None] + "}"
    # <gpx> contains a <trk> element, which contains a <trkseg> element
    # FIXME rewrite this to iterate over tracks and segments
    trkseg = root.find(NS + "trk").find(NS + "trkseg")

    # Add a 'keep' attribute to each <trkpt> element in the <trkseg>
    # Also remove elevation data
    for pt in trkseg:
        pt.attrib['keep'] = "False"

    # We assume we need the first and last point
    # TODO make this configurable, to allow processing of only
    #      part of a track
    trkseg[0].attrib['keep'] = 'True'
    trkseg[-1].attrib['keep'] = 'True'

    smooth.process(trkseg, maxdistance, maxinterval)

    # Remove the unneeded trackpoints based on the 'keep' attribute
    m = len(trkseg)
    kill = list(filter(lambda pt: pt.attrib['keep'] == 'False', trkseg))
    for n in range(0, len(kill)):
        trkseg.remove(kill[n])
    n = len(trkseg)
    print("......", m, n)

    # Remove the 'keep' attribute
    for n in range(0, len(trkseg)):
        trkseg[n].attrib.pop('keep')

    # Write out the modified GPX file
    fh = open(outputfilename, 'w')
    xml = fh.write(etree.tostring(root, pretty_print=True, xml_declaration=True).decode('utf-8'))
    fh.close()








