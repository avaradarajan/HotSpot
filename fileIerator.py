##########################################################################
## FileIterator.py v0.1
##
## Iterate through files from twitter archive and merge all tweet files together
## Currently these are collected hour and day wise, so we had to merge all json files together and then convert all to a CSV
## For each day, 18GB of data was generated

## Team Name: ANA
## Team Members : Anandh Varadarajan, Nithish Kolli, Abhiram Karri
##########################################################################

import os
# code to merge all the json files in the tweets after extracting them
def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r


s = list_files('C:\\Users\\Abhiram Karri\\Downloads\\BD Data\\twitter-stream-2017-07-01\\2017\\07\\01')
# print(s)

import shutil

outfilename = 'C:\\Users\\Abhiram Karri\\Downloads\\BD Data\\twitter-stream-2017-07-01\\2017\\07\\01\\final.json'

with open(outfilename, 'wb') as outfile:
    for filename in s:
        if filename == outfilename:
         continue
        with open(filename, 'rb') as readfile:
            shutil.copyfileobj(readfile, outfile)