import re
import csv

import os
import sys

print(sys.argv)


def getInt(etspF):  # this gets rid of the spaces and 'F' in the ETSP column
    etspF = etspF.replace(" ", "")
    etspF = etspF.replace("F", "")
    etspF = etspF.replace("%", "")
    return int(float(etspF))  # returns interger


def getFloat(var):  # this gets rid of the spaces and 'F' in the ETSP column
    var = var.replace(" ", "")
    var = var.replace("F", "")
    var = var.replace("%", "")
    return float(var)  # returns float


def timestampIncr(ts):
    tsList = ts.split(":")
    sec = int(tsList[1])
    minutes = int(tsList[0])
    # print (str(sec))
    sec = sec + 5
    # print (str(sec))
    if ((sec / 60) == 1):
        minutes = minutes + 1
        sec = 0
    # print(str(minutes)+':'+str(sec))
    if (minutes < 10):
        if (sec < 6):
            return ('0' + str(minutes) + ':0' + str(sec))
        return ('0' + str(minutes) + ':' + str(sec))
    if (sec < 6):
        return (str(minutes) + ':0' + str(sec))
    return (str(minutes) + ':' + str(sec))


def timestampReset(ts):
    return ('00:00')


# for row in dayReader:
# if (roastDate == 'none', 'Date'):#only set if not a date
# roastDate = row[0]
# print (roastDate)
# print('Row #' + str(dayReader.line_num)+' ' + str(row))
# roastDate = roastDate.replace("/", ".") #change slashes to periods so can be a filename
# print (roastDate)

# ~~~~~~~~~~~~~~~~~
# ('Date:17.02.2015')
# ('time1', 'BT', 'ET', 'ETSP', 'HEAT')
# Convert Comma deliniation to Tabs

# ~~~~~~~~~~~~~~~~~~~


######PYSUDO CODE EXAMPLE###########
# import all files in .py folder (?)
# str filename = ''
# drop checker variables
#
# while rows in original file
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


def fileSplit(dayReader):  # this is a csv read in file... var = csv.reader(file.csv)
    # testing variable
    lastRow = ''  # apperently this *is* being used, but only for a UI convenience

    ###These are the semi-persistent variables that I need
    timestamp = '00:00'  # this is the variable that'll go into the time colum, it increments by fives
    # this is the variable that tracks the date for all roasts
    roastDate = 'none'
    # these track the last two tuple's of heat
    past_heat1 = 0
    past_heat2 = 0
    Record = False
    roastNumber = 1
    beans_cooldown = False
    cool_complete = False
    ######This outputs the file
    for row in dayReader:
        lastRow = ('Row #' + str(dayReader.line_num))
        mylist = row  # .split(",")
        if (mylist[4] == 'Bean Temp'):
            continue  # exit the iteration if the data in that row is not a number

        rampRate = getFloat(mylist[6])  # turn the ramprate string into ramprate float
        rampRate = getFloat(mylist[6])  # turn the ramprate string into ramprate float

        if ((beanT < 385) & (beanT > 340) & (beanT < past_heat1) & (
                beans_cooldown == False)):  # IF not picking up start of roast this line may need to be tweaked
            beans_cooldown = True
            print('Beans are in')
            Record = False  # If its dropping, a roast is done
        if ((beanT < 315) & (
                beanT > 295) & beans_cooldown):  # if a new set of beans caused the cooldown AND it's dropped to 300 #IF not picking up start of roast this line may need to be tweaked
            Record = True  # then start tracking
            # print ('past 300')
            beans_cooldown = False
            print('creating new roast file starting at ' + lastRow)
            if (roastDate == 'none', 'Date'):  # only set if not a date
                roastDate = row[0]
            # print (roastDate)
            # print('Row #' + str(dayReader.line_num)+' ' + str(row))
            roastDate = roastDate.replace("/", ".")  # change slashes to periods so can be a filename
            # print (roastDate)
            # Create the CSV file, and add header
            outputFile = open(str(roastDate) + '.roastnumber' + '_' + str(roastNumber) + '.csv', 'w', newline='')
            outputwriter = csv.writer(outputFile, delimiter="\t")
            outputwriter.writerow(
                ['Date:' + str(roastDate), 'Unit:F', 'CHARGE:00:00', 'TP:00:00', 'DRYe:00:00', 'FCs:00:00', 'FCe:00:00',
                 'SCs:00:00', 'SCe:00:00', 'DROP:00:00', 'COOL:00:00'])  # places date at top
            outputwriter.writerow(
                ('Time1', 'Time2', 'BT', 'ET', 'Event', 'ETSP', 'HEAT'))  # places headers at top of colums

        ###TEST QUALIFICATIONS####
        if ((beanT > past_heat1) & (
                beanT > past_heat2) & beans_cooldown):  ##if rise twice in a row, it isn't  cooling down
            beans_cooldown = False
        # print ('false Alarm')

        ####~~~~~~~~~~~~~~~~~~~####

        if (Record):  #
            # print ('.recorded line.')
            # The output will stop when the heat drops twice in a row
            # print ('' + str(timestamp) + time2 + ' ' +str(beanT) +' ' + str(mylist[3]) +' ' +mylist[5] + ' ' +mylist[9])
            outputwriter.writerow([timestamp, '', getFloat(mylist[4]), getFloat(mylist[3]), '', getInt(mylist[5]),
                                   getInt(mylist[9])])  # outputs the file
            timestamp = timestampIncr(timestamp)
            # closes the output
            beans_cooldown = False  # change this variable back to 'off'
            # timestamp = 0
            if ((beanT > past_heat1) & (beanT > past_heat2)):  ##Have to account for initial cooloff though
                cool_complete = True
            if ((beanT < past_heat1) & (
                    beanT < past_heat2) & cool_complete):  ##if drop twice in a row, it isn't  roasting anyore
                Record = False
                cool_complete = False
                timestamp = timestampReset(timestamp)
                print('stopping record at ' + lastRow)
                roastNumber = (roastNumber + 1)
                print('roast number ' + str(roastNumber - 1) + ' is stored.\n')
                outputFile.close()
        past_heat2 = past_heat1
        past_heat1 = beanT
    print(
        '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nFile processing complete! \nCheck your folder for the new files!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')


# print ('Last Row expectede be 1436.... ' + lastRow +' ' +  str(timestamp) + '  '+ str(beanT) + '  '+ str(past_heat1) + '  '+ str(past_heat2))


# THIS IS TO SIMPOLE REFORMAT THE ENTIRE CSV
# IT DOES NOT SPLIT THEM
def fileFormat(dayReader, var):  # this is a csv read in file... var = csv.reader(file.csv)
    # testing variable
    lastRow = ''  # apperently this *is* being used, but only for a UI convenience

    ###These are the semi-persistent variables that I need
    timestamp = '00:00'  # this is the variable that'll go into the time colum, it increments by fives
    # this is the variable that tracks the date for all roasts
    roastDate = 'none'
    # these track the last two tuple's of heat
    past_heat1 = 0
    past_heat2 = 0
    Record = False
    filemade = False
    roastNumber = 1
    beans_cooldown = False
    cool_complete = False
    ######This outputs the file
    for row in dayReader:
        lastRow = ('Row #' + str(dayReader.line_num))
        mylist = row  # .split(",")
        # print (mylist)
        if (mylist[4] == 'Bean Temp'):  # this is highly specific
            continue  # exit the iteration if the data in that row is not a number

        beanT = getInt(mylist[4])  # turn the Bean Temp string into beanT interger

        if (
                filemade == False):  # if a new set of beans caused the cooldown AND it's dropped to 300 #IF not picking up start of roast this line may need to be tweaked
            Record = True  # then start tracking
            if (roastDate == 'none', 'Date'):  # only set if not a date
                roastDate = row[0]
            print('creating new file for ' + roastDate)
            roastDate = roastDate.replace("/", ".")  # change slashes to periods so can be a filename

            # Create the CSV file, and add header
            outputFile = open(str(roastDate) + '.csv', 'w', newline='')
            outputwriter = csv.writer(outputFile, delimiter="\t")
            # header
            outputwriter.writerow(
                ['Date:' + str(roastDate), 'Unit:F', 'CHARGE:00:00', 'TP:00:00', 'DRYe:00:00', 'FCs:00:00', 'FCe:00:00',
                 'SCs:00:00', 'SCe:00:00', 'DROP:00:00', 'COOL:00:00'])  # places date at top
            outputwriter.writerow(
                ('Time1', 'Time2', 'BT', 'ET', 'Event', 'ETSP', 'HEAT'))  # places headers at top of colums
            filemade = True

        if (Record):  #
            # print ('.recorded line.')
            # The output will stop when the heat drops twice in a row
            # print ('' + str(timestamp) + time2 + ' ' +str(beanT) +' ' + str(mylist[3]) +' ' +mylist[5] + ' ' +mylist[9])
            outputwriter.writerow([timestamp, '', getFloat(mylist[4]), getFloat(mylist[3]), '', getInt(mylist[5]),
                                   getInt(mylist[9])])  # outputs the file
            timestamp = timestampIncr(timestamp)
            # closes the output
            beans_cooldown = False  # change this variable back to 'off'
        # timestamp = 0
        # if((beanT > past_heat1) & (beanT > past_heat2)):##Have to account for initial cooloff though
        # cool_complete = True
        # if((beanT < past_heat1) & (beanT < past_heat2) & cool_complete): ##if drop twice in a row, it isn't  roasting anyore
        # Record =  False
        # cool_complete = False
        # timestamp = timestampReset(timestamp)
        # print ('stopping record at ' + lastRow)
        # roastNumber = (roastNumber+1)
        # print ( 'roast number ' + str(roastNumber-1) + ' is stored.\n')
        # outputFile.close()
        past_heat2 = past_heat1
        past_heat1 = beanT
    print(str(var), ".csv has been processed successfully")


# print ('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nFile processing complete! \nCheck your folder for the new files!\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# print ('Last Row expectede be 1436.... ' + lastRow +' ' +  str(timestamp) + '  '+ str(beanT) + '  '+ str(past_heat1) + '  '+ str(past_heat2))

userinput = ''

# GetFileNames()
# print (os.listdir())

# fileFormat(csv.reader(open('16080600.csv')))
while (True):
    print('Press enter to bulk convert all .csv files with numbers from 1000000-200000000. ')
    userinput = input('Type your input here>> ')

    # print (type(userinput))
    # print (userinput)

    if (userinput == 'exit'):
        exit()
    filecount = 0
    i = 10000000
    # fileFormat(csv.reader(open('16080600.csv')))
    while ((i <= 20000000)):
        # filename = (str(i), '.csv')
        try:
            # print(str(i) + '.csv')
            # print ('trying imported file')
            fileFormat(csv.reader(open((str(i) + '.csv'))), i)
            filecount = filecount + 1
        # print ('Sucessfuly imported file')
        except:
            # print ('error (filename may be mistyped)')
            pass
        i = i + 100
    # print (i)
    print('total files converted: ' + str(filecount))
