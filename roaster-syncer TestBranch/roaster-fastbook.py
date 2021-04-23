# !/usr/bin/python3

from pathlib import Path
from bs4 import BeautifulSoup
import csv
# import requests
import logging
import os, sys
import datetime

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
	
# create our logger file for first time run on new machine
f=open("offlineFiles.txt")
f.close() 

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



def getGoogleConnection():
	try:
		global drive_service 
		drive_service = discovery.build('drive', 'v3', http=http)
		# creds = ServiceAccountCredentials.from_json_keyfile_name('internet-of-beans-e9d6a50b7d4a.json', ['https://www.googleapis.com/auth/drive'])
		global creds
		creds = authInst.getCredentials()
		global drive_api 
		drive_api = build('drive', 'v3', credentials=creds)
		googleOk()
	except Exception as e:
		report_print.set(str('\nThere may be problem connecting to Google, Check Internet Connection\n'))
		print("There's a problem!")
		print(str(e))
		googleBad()
		return False # exit the function to avoid trying to upload....
	# if it worked, try to sync any offline files
	f=open("offlineFiles.txt", "r")
	#file.write("\n"+str(file_name) + ', '+str(date) + ', '+str(uploadLabel) )
	retryLines = ''
	f1 = f.readlines()
	fDelete=open("offlineFiles.txt", "w")
	fDelete.close() 
	for line in f1:
		if (len(line) < 2):
			print("Uploading Offline Files")
			report_print.set(str('Uploaded Offline Files\n'))
			continue
		lineList = line.split(",")
		success = upload(os.path.join(lineList[0]),str(lineList[1]),str(lineList[2]))
		print ("uploading " + lineList[2] + " Worked: " + str(success)) #upload(csvfile, roastDate, csvName)
	#clear the file
	
# Logger variables and functions
# [{"date":7.1, "roasts":7},{"date":7.3, "roasts":4}]
logDates = []
# Storing newly made roasts for logs
# Also used to decide which files to upload
def addRoast(inputDate):
	# find if day exists, and it's index
	for entry in logDates:
		if (entry['date'] == inputDate):
			# Update 
			entry['roasts'] = (entry['roasts'] +1)
			return True
	# or insert
	new = {"date":inputDate, "roasts":1}
	logDates.append(new)

# List of roast files that successfully uploaded
# Can compare uploadedFiles against (processed) roastDate
# 
logUploads = []
def addUpload(inputDate):
	# find if day exists, and it's index
	for entry in logUploads:
		if (entry['date'] == inputDate):
			# Update 
			entry['roasts'] = (entry['roasts'] +1)
			return True
	# or insert
	new = {"date":inputDate, "roasts":1}
	logUploads.append(new)
		
#def getFloat(var):

#roaster_url = "http://192.168.1.104/logs/Log2/"
roaster_url = "http://127.0.0.1/logs/Log2/"
#test_roaster_url = "http://192.168.1.1/"
test_roaster_url = "http://127.0.0.1/"
try:
    os.makedirs("/var/cache/roaster")
    os.makedirs("/var/cache/roaster/input")
    os.makedirs("/var/cache/roaster/process")
    data_path = str(Path("/var/cache/roaster"))
except FileExistsError:
    data_path = str(Path("/var/cache/roaster"))
    pass

reportData = "No Data"


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
			
			# send day to count LOGGER 
			# will add roast, will add day if not exist
			addRoast(roastDate)
			
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
	update = ''
	try:
		# Timeout may have to be VERY long!!!
		response = requests.get(kb_url, timeout=40.10)
		if response.status_code == 200:
			print ('Connected to Roaster')
			roasterOk()
			report_print.set('\n'+str(report_print.get())+ 'Connected to Roaster!')
			return response.text
	except requests.exceptions.ConnectionError as ece:
		print('Connection to roaster: \n'+ str(ece) + "\n")
		update =('Connection to roaster: error, see console')
		roasterBad()
		pass
	except requests.exceptions.Timeout as et:
		print('timeout')
		update =('timeout, see console')
		roasterBad()
		pass
	except requests.exceptions.RequestException as e:
		print('Exeption' + str(e))
		update = ('Exeption, see console')
		roasterBad()
		pass
	report_print.set('\n'+str(report_print.get())+ update)
	updateImage()
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
	try:
		response = requests_session.get(url, timeout=40.1)
	except:
		print('Error connecting to roaster file')
		report_print.set('\n'+str(report_print.get())+ 'Error connecting to roaster file')
		pass
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
	#print('creating folder	')
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
	try:
		drive_service
	except NameError:
		# save the non-uploaded file's details
		with open("offlineFiles.txt", "a") as file:
			file.write("\n"+str(file_name) + ','+str(date) + ','+str(uploadLabel) )
		return False

	## TESTING MODE HERE ##
	if fileNew(uploadLabel):
		try:
			folder_id = getFolder(date)
		except:
			with open("offlineFiles.txt", "a") as file:
				file.write("\n"+str(file_name) + ','+str(date) + ','+str(uploadLabel) )
			return False
		body = {'name': uploadLabel, 'parents': [folder_id]} #, 'parents': [folder_id]
		media = MediaFileUpload(filename= file_name, mimetype = 'text/html')
		fiahl = drive_api.files().create(body=body, media_body=media).execute()
	# TODO: Test if it succeeded
	addUpload(date)
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

def google_init():
	try:
		response = requests.get('https://www.googleapis.com/auth/drive', timeout=8.10)
		if response.status_code == 200:
			print ('Connected to Google!')
			#googleOk()
			reportData = ('Connected to Google!\n')
			#report_print.set(reportData)
	except requests.exceptions.ConnectionError as ece:
		print('connection to google: error')
		reportData = ('google: connection error')
		pass
	except requests.exceptions.Timeout as et:
		print('timeout to google')
		reportData = ('timeout to google')
		pass
	except requests.exceptions.RequestException as e:
		print('Exeption connecting to google')
		reportData = ('Exeption connecting to google')
		pass
	updateImage()
	report_print.set('\n'+str(report_print.get())+ reportData)



## create a gui for reviewing status of upload ##
import tkinter as tk
from tkinter import StringVar
from tkinter import *

root = tk.Tk()

frame = tk.Canvas(root, width=300, height=25)
frame.pack()
report_print = StringVar()
update = Label(root, textvariable=report_print).pack()
frame.create_window(0, 0, window=update)

def run():
    #clear the report label
    report_print.set(str('')) #
    google_init()
    files = get_roaster_files()
    print ('These files are downloaded:')
    printReport()
    print (files)


def printReport():
    reportData = ('\nResult:')
    # for element in  files: #I don't like how this array displays, we'll use it to decide if uploads need to happen?
    
    reportData = (reportData + "\nThese files have been gotten from roaster:")
    for element in  logDates:
       reportData = (reportData + "\n date " + str(element['date'])+ " with " + str(element['roasts'])+ " roasts ")
    
    reportData = (reportData + "\n\n These files have been uploaded:")
    for element in  logUploads:
       reportData = (reportData + "\n date " + str(element['date'])+ " with " + str(element['roasts'])+ " roasts")
    #reportData = (files + '\n These files are downloaded:')
    print (logDates)
    print (logUploads)
    report_print.set(str(report_print.get())+ str(reportData))
    currentDT = datetime.datetime.now()
    with open("roasterLog.txt", "a") as file:
        file.write("\n\n  "+str(currentDT) + str(report_print.get()))
def refresh():
	report_print.set(str('')) #    
	getGoogleConnection()
	google_init()
	get_roaster_page(roaster_url)
	updateImage()  
	printReport()
    #frame.create_window(10, 10, window=report)

buttonExit = tk.Button(root, text='Exit Application', command=root.destroy)
buttonRun = tk.Button(root, text='Run', command=run)
buttonRefresh = tk.Button(root, text='Refresh', command=refresh)
frame.create_window(220, 15, window=buttonExit)
frame.create_window(35, 15, window=buttonRun)
frame.create_window(115, 15, window=buttonRefresh)




#frame = Frame(root, width=100, height=100)
# These are not nessicary?
#frame.bind("<Button-1>", callback)
#frame.bind("<Button-2>", callback)
#frame.bind("<Button-3>", callback)

reporttext = StringVar()
report = Label(root, textvariable=reporttext).pack()
#reporttext.set("report Text will appear here!")

################ Image control area ############## 
# Set base photo options w/ paths here
loading = PhotoImage(file="img/loading.gif")      
baseImg = PhotoImage(file="img/base.gif")   
gConImg = PhotoImage(file="img/gCon.gif")  
rConImg = PhotoImage(file="img/rCon.gif")  
noConImg = PhotoImage(file="img/noCon.gif")  
imageLoad = loading     

# Sets location for the image slot
panel = tk.Label(root, image=imageLoad)
panel.pack(side="bottom", fill="both", expand="yes")

#boolians
rCon = False
gCon = False

def roasterOk():
    global rCon, gCon
    rCon = True
    updateImage()
def roasterBad():
	global rCon, gCon
	rCon = False
	updateImage()	 
def googleOk():
    global gCon, rCon
    gCon = True
    updateImage()
def googleBad():
    global gCon, rCon
    gCon = False
    #DO NOT updateImage() here, is loop 
    
def updateImage():
    if (gCon and rCon):
        #set image to all OK
        panel.configure(image=baseImg)
        panel.image = baseImg
    elif (gCon):
        #google okay
        panel.configure(image=gConImg)
        panel.image = gConImg
    elif (rCon):
        #roaster okay
        panel.configure(image=rConImg)
        panel.image = rConImg
        getGoogleConnection() # check if google can be connected
    else:
        #none okay
        panel.configure(image=noConImg)
        panel.image = noConImg
        getGoogleConnection() # check if google can be connected


############### End Image Control ############

# start googleConnection after tracking variables are init-ed 
# has to be done globally, can't be restarted mid-process like the roaster connection?
getGoogleConnection()

frame.pack()
root.mainloop()





