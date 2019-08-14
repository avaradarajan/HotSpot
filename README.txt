Team Name - ANA

Team Members - Anandh Varadarajan, Nithish Kolli, Abhiram Karri

Cluster - Google Cloud DataProc + Debian(1.3.33-debian9) as in assignment with bi

File Descriptions -

GetTweets.py - Gets the old tweets using API - Creates a csv file that is used for creating the training/test set.

generateLabels.py - Generate Labels for validation set - Needs d5.csv as input and it outputs labelsFinal.csv

fileIterator.py - Iterate big data files to merge them to one file for HDFS - Needs the twitter archive file directory

TweetClassifier.py - Read and Classify UK tweets using Big Data processing concepts -  Uses d5.csv and labelsFinal.csv for training model. 
                     Uses subData1.csv which is a subset of data for code verification. Outputs a coordinates.csv with coordinates for plotting.


TrafficAccidentHotspotGenerator.py - Generates Hotspots from Traffic Accidents data using Spark and MapReduce - Uses main UK records dataset along with geo information to identify hotspots
Here you can use subset of data for checking - ukgov10000.csv.

TrafficAccidentsUK.ipynb - This file analyses aspects of accidents with inline plots for visualization. Input file is the ukgov10000.csv

Data files -

GB.txt - List of UK place with Geocodes
subData1.csv - Data to be used for TweetClassifier.py
d5.csv - Training/Test set for machine learning model with more than 25k tweets. To be used for generateLabels.py and TweetClassifier.py
labelsFinal.csv - Labels generated from running generateLabels.py
nyc.csv - All tweets for NYC area in a particular timeframe
nypd.csv - All NYPD official records

Visualization of Hotspots -

UK_Map_Visualization.html - Needs the lat long coordinates from Hotspots.csv and plotting details from uk.json. Similarly for NYC.

Additional code/Files :

References File - List of all references for project
ReverseGeoCoding.py - Given a latitude longitude it gives place details 

