#!/usr/bin/python3

from pathlib import Path
from bs4 import BeautifulSoup
import csv
#import requests
import logging
import os, sys
from urllib.parse import urljoin
import requests
from urllib.parse import urlparse
from hashlib import md5 

from oauth2client.service_account import ServiceAccountCredentials
import apiclient
from apiclient.discovery import build
from apiclient.http import MediaFileUpload

##
if sys.version_info.major < 3:
	from urllib import url2pathname
else:
	from urllib.request import url2pathname
	

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None
##
import auth
SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'
authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
credentials = authInst.getCredentials()
http = credentials.authorize(httplib2.Http())

drive_service = discovery.build('drive', 'v3', http=http)
#creds = ServiceAccountCredentials.from_json_keyfile_name('internet-of-beans-e9d6a50b7d4a.json', ['https://www.googleapis.com/auth/drive'])
creds = authInst.getCredentials()
drive_api = build('drive', 'v3', credentials=creds)

#from gpiozero import LED, Button
#from time import sleep
#from signal import pause



#roaster_url = "http://192.168.1.104/logs/Log2/"
roaster_url = "http://127.0.0.1/logs/Log2/"
#test_roaster_url = "http://192.168.1.1/"
test_roaster_url = "http://127.0.0.1/"
data_path = str(Path("/var/cache/roaster"))


#### roast_file_processor ####

def getFloat(var):	  # this gets rid of the spaces and 'F' in the ETSP column
	var = var.replace(" ", "") 
	var = var.replace("F", "")
	var = var.replace("%", "")
	try:
		return float(var) 
	except:
		return 35055


def getInt(etspF):	  # this gets rid of the spaces and 'F' in the ETSP column
	return int(getFloat(etspF))	 # returns integer

def timestampIncr(ts):
	tsList = ts.split(":")
	sec = int(tsList[1])
	minutes = int(tsList[0])
	sec = sec+5
	while sec / 60 >= 1:
		minutes = minutes + 1
		sec = sec - 60
	# return "{02d}:{02d}".format(minutes, sec)
	if minutes < 10:
		if sec < 6 :
			return '0'+str(minutes)+':0'+str(sec)
		return '0'+str(minutes)+':'+str(sec)
	if sec < 6:
		return str(minutes)+':0'+str(sec)
	return str(minutes)+':'+str(sec)
	
def fileSplit(fileLocation, outputpath): #this is a csv read in file... var = csv.reader(file.csv)
	dayReader  = (csv.reader(open(fileLocation)))
	
	timestamp = '00:00'	 # this is the variable that'll go into the time colum, it increments by fives
	roastDate = 'none'
	past_heat1 = 0
	past_heat2 = 0
	Record = False
	roastNumber = 1
	lines = 0
	beansIn = False
	rampRate_streak = False
	i = 1
	outputFile = None

	for row in dayReader:
		mylist = row

		try:
			if mylist[4] == 'Bean Temp':	# header row test
				continue	# exit the iteration if the data in that row is not a number 
		except:
			#print ('out of bounds', mylist[0])
			continue
	
		beanT = getInt(mylist[4])	   # turn the Bean Temp string into beanT interger
		
		rampRate = getFloat(mylist[6])  # turn the ramprate string into ramprate float
		if rampRate == 35055:	# header row test
			continue	# exit the iteration if the data in that row is not a number
				
		coolFan = (mylist[7])		   # turn the ramprate string into ramprate float
		heatPower = (mylist[20])
		
		if (rampRate == 0.1) and (Record == False):	 # start roast record
			beansIn = True
			Record = True 
			rampRate_streak = True
			Record = True
			if roastDate == 'none':					 # only set if not a date 
				roastDate = row[0]
			roastDate = roastDate.replace("/", ".")	 # change slashes to periods so can be a filename
			if outputpath:
				csvfile = os.path.join(outputpath, str(roastDate) + '.roastnumber'+ '_'+ str(roastNumber)+ '.csv')
			else:
				csvfile = str(roastDate) + '.roastnumber'+ '_'+ str(roastNumber) + '.csv'
			outputFile = open(csvfile, 'w',  newline='')
			outputwriter = csv.writer(outputFile,  delimiter="\t")
			outputwriter.writerow(['Date:' + str(roastDate), 'Unit:F', 'CHARGE:00:00', 'TP:00:00',
					'DRYe:00:00', 'FCs:00:00', 'FCe:00:00', 'SCs:00:00', 'SCe:00:00', 'DROP:00:00',
					'COOL:00:00'])					  # places date at top
			outputwriter.writerow(('Time1', 'Time2' ,'BT', 'ET', 'Event','ETSP', 'HEAT'))   # places headers at top of colums 
		
		if (lines > 40) and (beanT < past_heat1) and (beanT < past_heat2) and (Record == True):
			Record = False			  # If its dropping, a roast is done
			outputFile.close()
			#upload(self, fname,date):
			#csvfile
			csvName = str(roastDate) + '.roastnumber'+ '_'+ str(roastNumber) + '.csv'
			upload(csvfile, roastDate, csvName)
			
			roastNumber = (roastNumber + 1)
			lines = 0
			timestamp = '00:00'

		if Record:
			outputwriter.writerow([timestamp, '' , getFloat(mylist[4]), getFloat(mylist[3]), '',
					getInt(mylist[5]), getInt(mylist[9]) ])
			timestamp = timestampIncr(timestamp)
			lines = lines + 1
		past_heat2 = past_heat1
		past_heat1 = beanT

	if outputFile is not None and not outputFile.closed:
		outputFile.close()


#### get_roast_file ####

def get_roaster_page(kb_url):
	try:
		response = requests.get(kb_url, timeout=10.0)
		if response.status_code == 200:
			return response.text
	except requests.exceptions.ConnectionError as ece:
		pass
	except requests.exceptions.Timeout as et:
		pass
	except requests.exceptions.RequestException as e:
		pass
	return None

def get_file_list(url):
	page = get_roaster_page(url)
	if page:
		soup = BeautifulSoup(page, 'html.parser')
		
		csvArr = []
		linkArray = ([node.get('href') for node in soup.find_all('a')])
		for i in range(len(linkArray)):
			if (linkArray[i].rsplit('.', 1)[-1] == 'CSV'):
				csvArr.append(url + linkArray[i])
		return (csvArr)
		#return [url + node.get('href') for node in soup.find_all('a')]
	else:
		return None

def get_roaster_file(url, csvfile):
	downloadfile = None

	requests_session = requests.session()
	response = requests_session.get(url, timeout=10.1)
	if response.status_code == 200:
		with open(csvfile, 'wb') as f:
			f.write(response.content)
			downloadfile = csvfile
	return downloadfile

def get_roaster_files():
	checksums = {}
	for f in os.listdir(os.path.join(data_path, "input")):
		fpath = os.path.join(data_path, "input", f)
		if os.path.exists(fpath):
			with open(fpath) as fh:
				#m = md5.new(fh.read())
				m = md5(fh.read().encode('utf-8'))
			checksums[f] = m.digest()
			
	results = []
	for url in (roaster_url, test_roaster_url):
		filelist = get_file_list(url)
		if filelist:
			base_url = url
			break

	if filelist is not None:
		for csvfile in filelist:
			#change the file
			name = (csvfile.rsplit('/', 1)[-1])
			input_file = os.path.join(data_path, "input", name)
			url = urljoin(base_url, csvfile)
			if get_roaster_file(url, input_file) is None:
				return None
			with open(input_file) as fh:
				#m = md5.new(fh.read())
				m = md5(fh.read().encode('utf-8'))
				if checksums.get(csvfile, 0) != m.digest():
					fileLocation = (os.path.join(data_path,'input',(csvfile.rsplit('/', 1)[-1])))
					#fileSplit(csv.reader(fh), os.path.join(data_path, "process"))
					fileSplit(fileLocation, os.path.join(data_path, "process"))
					results.append(csvfile)
	else:
		return None

	return results


#### Google API code ####

#class UpLoader(object):
def createFolder(name):
	print('creating folder')
	folder_id = "1JvI49SnEQTc0GwswKINLnpv72hCV2CBY"
	file_metadata = {
	'name': name, 'parents': [folder_id],
	'mimeType': 'application/vnd.google-apps.folder'
	}
	file = drive_service.files().create(body=file_metadata,
										fields='id').execute()
	print ('Folder ID: %s' % file.get('id'))
	return (file.get('id'))
	
def __init__(self, jsonfile = "client_secret.json"):
	self.creds = ServiceAccountCredentials.from_json_keyfile_name(jsonfile, ['https://www.googleapis.com/auth/drive'])
	self.drive_api = build('drive', 'v3', credentials=creds)
	
def upload( file_name, date, uploadLabel):
	if fileNew(uploadLabel):
		folder_id = getFolder(date)
		body = {'name': uploadLabel, 'parents': [folder_id]} #, 'parents': [folder_id]
		media = MediaFileUpload(filename= file_name, mimetype = 'text/html')
		fiahl = drive_api.files().create(body=body, media_body=media).execute()
	# TODO: Test if it succeeded
	return True
def fileNew(name):
	query = ("name = '"+name+"'") #or 'contains'?
	size = 1
	try:
		results = drive_service.files().list(pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
		items = results.get('files', [])
		if not items:
			return True
		else:
			for item in items:
				return False
	except:
		return True
	
def getFolder(date):
	query = ("name = '"+date+"'") #or 'contains'?
	size = 1
	try:
		results = drive_service.files().list(pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
		items = results.get('files', [])
		if not items:
			return(createFolder(date))
		else:
			for item in items:
				return(item['id'])
	except:
		return(createFolder(date))
	


def transfer_files():
	checksums = {}

	for f in os.listdir(Path(data_path,"process")):
		fpath = os.join(data_path, 'process', f)
		if os.path.exists(fpath):
			with open(fpath) as fh:
				m = md5.new(fh.read())
			checksums[f] = m.digest()
	uploader = UpLoader()
	files = get_roaster_files()
	if files is None:
		return 1
	for f in os.listdir(os.join.path(data_path, "process")):
		fpath = os.join(data_path, 'process', f)
		if os.path.exists(fpath):
			with open(fpath) as fh:
				m = md5.new(fh.read())
			if checksums.get(f, 0) != m.digest():
				if not uploader.upload(f, fpath):
					return 2
	return 0

#### raspberrypi_roaster ####

#for d in ('process', 'input'):
#	dname = os.join(data_path, d)
#	if not os.path.exists(dname):
#		os.makedirs(dname)

#led = LED(5)
#button = Button(13, )

files = get_roaster_files()
print ('These files are downloaded:')
print (files)
#r = transfer_files()

#pause()



