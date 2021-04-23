#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import re
import csv

import os
import sys


def getInt(etspF): #this gets rid of the spaces and 'F' in the ETSP column
	etspF = etspF.replace(" ", "") 
	etspF = etspF.replace("F", "")
	etspF = etspF.replace("%", "")
	return int(float(etspF)) #returns interger
def getFloat(var): #this gets rid of the spaces and 'F' in the ETSP column
	var = var.replace(" ", "") 
	var = var.replace("F", "")
	var = var.replace("%", "")
	return float(var) #returns float
def timestampIncr(ts):
	tsList = ts.split(":")
	sec = int(tsList[1])
	minutes = int(tsList[0])
	#print (str(sec))
	sec = sec+5
	#print (str(sec))
	if((sec/60) == 1):
		minutes = minutes+1
		sec = 0
	#print(str(minutes)+':'+str(sec))
	if(minutes<10):
		if(sec<6):
			return ('0'+str(minutes)+':0'+str(sec))
		return ('0'+str(minutes)+':'+str(sec))
	if(sec<6):
		return (str(minutes)+':0'+str(sec))
	return (str(minutes)+':'+str(sec))
	
	
def timestampReset(ts):
	return ('00:00')
		
	



#for row in dayReader:
	#if (roastDate == 'none', 'Date'):#only set if not a date 
		#roastDate = row[0]
		#print (roastDate)
	#print('Row #' + str(dayReader.line_num)+' ' + str(row))
#roastDate = roastDate.replace("/", ".") #change slashes to periods so can be a filename
#print (roastDate)

#~~~~~~~~~~~~~~~~~
#('Date:17.02.2015')
#('time1', 'BT', 'ET', 'ETSP', 'HEAT')
#Convert Comma deliniation to Tabs

#~~~~~~~~~~~~~~~~~~~



######PYSUDO CODE EXAMPLE###########
#import all files in .py folder (?)
#str filename = ''
#drop checker variables
#
#while rows in original file
#	Parse the row
#	if 350-> 300 drop
#		filename = ('roast' + (x++) + date + '.csv') #filename is the 
#		outputwriter.writerow('time1', 'BT', 'ET', 'ETSP', 'HEAT') #Create csv header
#		record = True
#	If record
#		outputwriter.writerow(time++5, beantemp, enviro temp, etsp, heat) #output each line
#		If drop
#			record = False
#			Reset drop checker variables
#		>>save drop checker variables
######  EXAMPLE   END   ###########

#Ramp Rate is 6 
#cooling fan is 7

#determine cycle start and end: cooling fan column.  The fan turns on as soon as the cycle stops.  
#Also I see a drop from 32% to 14% “Power” at the beginning of the beginning of the cooling.  This would be just a double check because the power quickly returns to 32%.  
#Finally the Stirflex comes on at the start of the cycle – it also comes on mid-cycle so this would be a triple check but not a good way to guage the timing alone.  
#Finally the HeatPower drops suddenly from 5000% to 1450% and the Enviro SP drops to 200Fat the start of the cooling cycle.
#Those are my quick observations of the cycle.  Whether any of that matters depends on the purpose of the assignment.  If the purpose is simply to parse the file, 
#I would use the Cooling Fan and possible double check it with one of the others.

#Rien: colum 5. enviro sp, drops to idle temperature at start of roast. Old files in 150, new is 300. 
#At same time, power colum goes to 50%
#Also, ramp rate. Ramp rate won't change. 
#START roast: Ramprate == 0.1
#Ramp Rate is 6th index



def fileSplit(dayReader, outputpath=None): #this is a csv read in file... var = csv.reader(file.csv)
	#testing variable
	lastRow = '' #apperently this *is* being used, but only for a UI convenience
	
	###These are the semi-persistent variables that I need
	timestamp = '00:00' #this is the variable that'll go into the time colum, it increments by fives
	#this is the variable that tracks the date for all roasts
	roastDate = 'none'
	#these track the last two tuple's of heat
	past_heat1 = 0
	past_heat2 = 0
	#past_rampRate = 0.0
	Record = False
	roastNumber = 1
	lines = 0
	beansIn = False
	rampRate_streak = False
	i = 1
	######This outputs the file
	for row in dayReader:
		lastRow = ('Row #' + str(dayReader.line_num))
		mylist = row#.split(",")
		if (mylist[4] == 'Bean Temp'):
			continue #exit the iteration if the data in that row is not a number
	
		beanT = getInt(mylist[4])#turn the Bean Temp string into beanT interger
		rampRate = getFloat(mylist[6])#turn the ramprate string into ramprate float
		coolFan = (mylist[7])#turn the ramprate string into ramprate float
		heatPower = (mylist[20])
		
		if ((rampRate == 0.1) & (Record == False)): #start roast record
			beansIn = True
			Record = True 
			rampRate_streak = True
			#print ('Beans are in')
			Record = True
			print ('creating roast file ' +str(roastNumber)+' starting at ' + lastRow)
			if (roastDate == 'none', 'Date'):#only set if not a date 
				roastDate = row[0]
				#print (roastDate)
				#print('Row #' + str(dayReader.line_num)+' ' + str(row))
			roastDate = roastDate.replace("/", ".") #change slashes to periods so can be a filename
			#print (roastDate)
			#Create the CSV file, and add header
			if outputpath:
				csvfile = os.path.join(outputpath, str(roastDate) + '.roastnumber'+ '_'+ str(roastNumber)+ '.csv')
			else:
				csvfile = str(roastDate) + '.roastnumber'+ '_'+ str(roastNumber)+ '.csv'
			outputFile = open(csvfile, 'w',  newline='')
			outputwriter = csv.writer(outputFile,  delimiter="\t")
			outputwriter.writerow(['Date:' + str(roastDate), 'Unit:F' ,'CHARGE:00:00' ,'TP:00:00' ,'DRYe:00:00' ,'FCs:00:00' ,'FCe:00:00' ,'SCs:00:00' ,'SCe:00:00' ,'DROP:00:00' ,'COOL:00:00' ])#places date at top
			outputwriter.writerow(('Time1', 'Time2' ,'BT', 'ET', 'Event','ETSP', 'HEAT'))#places headers at top of colums 
		
		if ((lines > 40) & (beanT < past_heat1) & (beanT < past_heat2) & (Record == True)): #
			#  && ((past_heat1 - past_heat2) < 10?????) if@350 and if dropping and if dropping FAST
			#beans_cooldown = True
			Record = False # If its dropping, a roast is done
			print ('ending roast file ' +str(roastNumber)+' at ' + lastRow + ' with '+ str(lines) +' saved')
			outputFile.close()
			roastNumber = (roastNumber + 1)
			lines = 0
			timestamp = '00:00'
			
		
		
		#if((Record) & (heatPower == "14.50%")): #if a new set of beans caused the cooldown AND it's dropped to 300 #IF not picking up start of roast this line may need to be tweaked
			#Record == (False)
			#if(Record == False): 
				#outputFile.close()
			#Record == (False)
			#roastNumber = (roastNumber + 1)
			#continue
			
		###TEST QUALIFICATIONS####
		#if((beanT > past_heat1) & (beanT > past_heat2) & beans_cooldown): ##if rise twice in a row, it isn't  cooling down
		#	beans_cooldown =  False
			#print ('false Alarm')
	
		####~~~~~~~~~~~~~~~~~~~####
			
		if(Record): #
			#print ('.recorded line.')
			#The output will stop when the heat drops twice in a row
			#print ('' + str(timestamp) + time2 + ' ' +str(beanT) +' ' + str(mylist[3]) +' ' +mylist[5] + ' ' +mylist[9])
			outputwriter.writerow([timestamp, '' , getFloat(mylist[4]), getFloat(mylist[3]), '', getInt(mylist[5]), getInt(mylist[9]) ])#outputs the file
			timestamp = timestampIncr(timestamp)
			lines = lines +1
			 #closes the output
			#beans_cooldown = False #change this variable back to 'off' 
			#timestamp = 0
			#if((beanT > past_heat1) & (beanT > past_heat2)):##Have to account for initial cooloff though
			#	cool_complete = True
			#if((beanT < past_heat1) & (beanT < past_heat2) & cool_complete): ##if drop twice in a row, it isn't  roasting anyore 
			#	Record =  False
			#	cool_complete = False
			#	timestamp = timestampReset(timestamp)
			#	print ('stopping record at ' + lastRow)
			#	roastNumber = (roastNumber+1)
			#	print ( 'roast number ' + str(roastNumber-1) + ' is stored.\n')
			#	outputFile.close()
		#past_rampRate = rampRate
		past_heat2 = past_heat1
		past_heat1 = beanT
	print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nFile processing of '+ str(roastDate) +' complete! \nCheck your folder for the new files!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	#print ('Last Row expectede be 1436.... ' + lastRow +' ' +  str(timestamp) + '  '+ str(beanT) + '  '+ str(past_heat1) + '  '+ str(past_heat2))



#GetFileNames()
#print (os.listdir())

def main(argv):
	userinput = ''
	while(True):
		print (sys.argv)
		print ('Press enter to bulk convert all .csv files with numbers from 1000000-200000000. ')
		print ('WARNING\n If you have 20xx.0x.0x.roastnumber_#.csv files currently in this folder \n they WILL be overwritten... deleting your changes!!!! \nWARNING')
		userinput =  input('press Enter when you\'re sure about this>> ')
		
		#print (type(userinput))
		#print (userinput)
			
		if(userinput == 'exit'):
			exit()
		filecount = 0
		i = 10000000
		fileSplit(csv.reader(open('16080600.csv')))
		while((i <= 20000000)):
			#filename = (str(i), '.csv')
			try:
				#print(str(i) + '.csv')
				#print ('trying imported file') 
				fileSplit(csv.reader(open((str(i)+ '.csv'))))
				filecount = filecount+1
				print ('Sucessfuly imported file') 
			except:
				#print ('error (filename may be mistyped)')
				pass
			i = i+100
			#print (i)
		print ('total files converted: ' + str(filecount))

if __name__ == "__main__":
    main(sys.argv[1:])