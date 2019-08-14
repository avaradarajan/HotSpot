# TrafficAccidentHotspotGenerator.py
#
# Generates Hotspots from Traffic Accidents data using Spark and MapReduce
# Datapipe line - HDFS + Spark
# Data concepts - Machine Learning + Map Reduce
# Team Name: ANA
# Team Members : Anandh Varadarajan, Nithish Kolli, Abhiram Karri


from pyspark import SparkContext
from pyspark.sql import SparkSession
from geopy.geocoders import Nominatim
import csv
import pandas as pd
import sys
geolocator = Nominatim(user_agent="Abhi223")


# This function uses geopy api and get the name of the location from geo-coordinates
def get_geo_codes_api(lat, long):
    try:
        location = geolocator.reverse(float(lat), float(long))
    except:
        print("here", lat, long)
        return False
    try:
        if 'address' in location.raw:
            if 'suburb' in location.raw['address']:
                return location.raw['address']['suburb']
    except:
        print(lat, long)
    return False


# This Function reads the Geocodes and makes a tuple of Lat, Long and location
def read_geo_codes(locationFile = 'GB.txt'):
    codesdf = pd.read_csv(locationFile, sep="\t", header=None, error_bad_lines=False)
    lats = list(codesdf[4])
    longs = list(codesdf[5])
    locs = list(codesdf[1])
    keyValues = []
    for i in range(len(lats)):
        keyValues.append(((round(lats[i],2), round(longs[i],2)), locs[i]))
    return keyValues


# This function converts the tuple to a broadcast Variable
def set_broadcast_variable(sc):
    keyValuesList = read_geo_codes()
    keyMap = sc.parallelize(keyValuesList).collectAsMap()
    keyMapBroad = sc.broadcast(keyMap)
    return keyMapBroad


# This function searches for the latitude and longitude in the broadcast variable and stores it.
def set_location(x, keyMapBC):
    try:
        return (keyMapBC.value[round(float(x[4]), 2), round(float(x[3]), 2)], x)
    except:
        return (None, x)


# This function extracts the latitude, longitude and the number of accidents and casualties at the site.
def get_hotspot(x):
    noIncidents = len(x[1].data)
    noOfCasualties = 0
    if noIncidents == None:
        return [x[0], 0, x[1].data[0][4], x[1].data[0][3], noOfCasualties]
    else:
        for i in range(noIncidents):
            noOfCasualties += int(x[1].data[i][8])
        return [x[0], noIncidents, x[1].data[0][4], x[1].data[0][3], noOfCasualties]


# Main Function
# We are using Spark Data Pipeline and Map Reduce concept here
def analyze_uk_data(sc, dataLocation):
    dataRdd = sc.textFile(dataLocation).mapPartitions(lambda line: csv.reader(line)).map(lambda x: x[1:]) #parsing using csv,reader and then removing the unwanted first column.
    header = dataRdd.first()
    keyMapBC = set_broadcast_variable(sc)
    dataLocationRDD = dataRdd.filter(lambda x: x != header).map(lambda x: set_location(x, keyMapBC))

    groupedRDD = dataLocationRDD.groupByKey()

    hotspotRDD = groupedRDD.map(get_hotspot).sortBy(lambda a: -a[1])

    sparkDf = hotspotRDD.toDF()
    df = sparkDf.toPandas()
    df.to_csv('Hotspots10000.csv')


if __name__ == '__main__':
    # data_location = '/Users/nithishkolli/Work/Masters/S19/Big_Data_Analytics/Project/Accidents20052019.csv' # Main Data Set
    data_location = sys.argv[1]  # Test DataSet
    sc = SparkContext()
    spark = SparkSession(sc)
    analyze_uk_data(sc, data_location)
