import os

Directory = 'J:\\ETPShare\\NERC - TPL\\2013\\By hand\\N-2\\Violations\\'
ending = '.txt'

# Create ACCC Folder if it doesn't already exist
def Make_Folder(FolderName):
	try:
		os.makedirs(FolderName)
	except OSError:
		if not os.path.isdir(FolderName):
			raise
	return FolderName

def GetFileNames(Dir,End):
	for f in os.listdir(Dir):
		if f.endswith(End):
			FileNames.append(f[:-4])
			print "%s" % f
	return FileNames

DirectorySimplified = Make_Folder(Directory + "Simplified\\")
FileNames = []
FileNames = GetFileNames(Directory+"Originals\\",'Voltage.txt')

for Fname in FileNames:
	f=open(Directory+"Originals\\"+Fname+ending,'r')
	g=open(DirectorySimplified+Fname+'-S'+ending,'w')

	for i in range(0,7):
		line = f.readline()
		line = line.strip('\f')
		
		if ("BUS# X--" in line):
			g.write(line[43:])
		elif ("BUSES WITH VOLTAGE" in line):
#			g.write(line)
			print "Deleted"
		else:
			print line
			g.write(line)
			
	for line in f:
		if ("MT. DETAIL EMBEDDED IN" in line) or ("WECC" in line) or ("X--------- FROM BUS" in line) or ("BUS# X-- NAME --X BASKV" in line) or ("SUBSYSTEM LOADING CHECK" in line) or ("LOADINGS ABOVE" in line) or ("OUTPUT FOR AREA" in line) or ("* NONE *" in line) or (line == "\n"):
			print "Deleted"
		elif ("BUSES WITH VOLTAGE" in line):
#			g.write(line)
			print "Deleted"
		elif ("BUS# X--" in line):
			g.write(line[:39]+'\n')
		else:
			BaseKV1 = float(line[19:25])
			Voltage1 = float(line[26:32])
			print BaseKV1, Voltage1
			if (BaseKV1 == 500 and (Voltage1 > 1.1 or Voltage1 < 1)) or ((BaseKV1 >= 161 and BaseKV1 < 500) and (Voltage1 > 1.05 or Voltage1 < 0.93)) or ((BaseKV1 >= 50 and BaseKV1 < 161) and (Voltage1 > 1.05 or Voltage1 < 0.9)):
				print line
				g.write(line[:39]+'\n')
			else:
				print "Delete #1 \n"
			try:
				BaseKV2 = float(line[62:68])
				Voltage2 = float(line[69:75])
				print BaseKV2, Voltage2
				if (BaseKV2 == 500 and (Voltage2 > 1.1 or Voltage2 < 1)) or ((BaseKV2 >= 161 and BaseKV2 < 500) and (Voltage2 > 1.05 or Voltage2 < 0.93)) or ((BaseKV2 >= 50 and BaseKV2 < 161) and (Voltage2 > 1.05 or Voltage2 < 0.9)):
					print line
					g.write(line[43:])
				else:
					print "Delete #2 \n"
			except ValueError:
				print "No second value on last line"

	f.close()
	g.close()
