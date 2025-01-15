#!/bin/env python3.12
### Sigh

import os
import glob
import argparse
import boto3
import password
import requests
import lb

from LogMe import LogMe

LOGSDIR = "./logs/"
OUTDIR  = "/leaderboard-JSON/"
S3BUCKET = "leaderboard.cihipi.com"
PREFIX = "json/"

parser = argparse.ArgumentParser(description='Updates AWS with any new output files')
parser.add_argument("--logname", help="Use a specific log file")
parser.add_argument("--forcePurge", action="store_true", help="Force an upload")
args = parser.parse_args()

# Initialise the logging
# Include a value for any PS1 scripts that need to run
if (args.logname):
	LogMe = LogMe (args.logname)
	ps1log = f"-logname {args.logname}"
else:
	LogMe = LogMe (LOGSDIR + os.path.basename(__file__) + ".log")
	ps1log = ""


if (lb.GOOGLEMAPS.find(password.googlemaps_api_10) > 0):
	LogMe.error ("Set to localhost for google maps - not uploading to AWS")
	exit ()

# Connect to s3 and verify bucket exists
try:
	s3 = boto3.resource('s3')
	s3_client = boto3.client('s3')

	if (not list(filter(lambda getMatchingBucket: getMatchingBucket.name == S3BUCKET, s3.buckets.all()))):
		LogMe.error  (f"Could not find S3 bucket {S3BUCKET}")
		exit
	bucket = s3.Bucket('leaderboard.cihipi.com')

except:
	LogMe.error (f"Could not connect to S3 bucket {S3BUCKET}")
	exit ()

bucketList = []
matchList = []
purgeCache = False

for b in list(bucket.objects.all()):
	if (b.key[:5] == "json/"):
		bucketList.append(b.key)

LogMe.progress (f"Connnected to AWS. Got {len(bucketList)} files in the bucket {S3BUCKET}. Syncing HTML files")

# Get all and any html files
localList = [f for f in os.listdir(OUTDIR) if f.endswith('.json')]

for curFile in localList:
	uploadFile = "No"
	fileType = "Unknown"
	s3Name = f"{PREFIX}{curFile}"

	if (curFile[-5:] == ".html"):
		fileType = "text/html"
	elif (curFile[-5:] == ".json"):
		fileType = "application/json"
	elif (curFile[-4:] == ".css"):
		fileType = "text/css"
	elif (curFile[-3:] == ".js"):
		fileType = "application/javascript"
	else:
		LogMe.error (f"Unsupported file type - {curFile}")
		exit ()
	
	curSize = os.path.getsize(os.path.join(OUTDIR,curFile))	

	if s3Name in bucketList:
		# If the local file matches the list of S3 bucket objects
		matchList.append (s3Name) 
	
		obj = s3.Object(S3BUCKET, key=s3Name)
		if (obj.content_length == curSize):
			# File is the same size on both local and remote
			LogMe.display (f"{curFile} is in sync {curSize} and {obj.content_length}")
		else:			
			# File is different sized
			uploadFile = "Updated"
	else:
		# New file
		uploadFile = "New"

	if (uploadFile != "No"):
		# Upload the file
		try:
			response = s3_client.upload_file(os.path.join(OUTDIR,curFile), S3BUCKET, s3Name, ExtraArgs={'ContentType': fileType})
			if (uploadFile == "Updated"):
				LogMe.progress (f"Updated {curFile} to {curSize} bytes")
			else:
				LogMe.yellow (f"Uploaded new file {curFile}")
		except:
			LogMe.error (f"Failed to upload {curFile}")
			exit ()			
		purgeCache = True

# Identify and clean up any S3 Orphans
for s3File in bucketList:
	if (s3File[-5:] == ".json") and (s3File not in matchList):
		try:
			s3_client.delete_object(Bucket=S3BUCKET, Key=s3File)
			LogMe.yellow (f"{s3File} has been deleted from AWS")
		except:
			LogMe.error (f"Failed to delete {s3File} from AWS")
			exit ()

if (purgeCache or args.forcePurge):
	headers = {
		'Content-Type':"application/json",
		'Authorization': f"Bearer {password.cloudflare_api}"
	}
	data = {
		'purge_everything': True
	}
	url = "https://api.cloudflare.com/client/v4/zones/c1872bd264c6a737ca7404718280d157/purge_cache"

	try:
		response = requests.post (url, json=data, headers=headers, timeout=10)
		if (response.status_code == 200):
			LogMe.progress ("Cloudflare cache purged")
		else:
			LogMe.error (f"Cloudflare returned {response.status_code}")
			exit ()
	except:
		LogMe.error (f"Cloudflare cache purge failed")
		exit ()

LogMe.progress ("AWS HTML sync completed")

