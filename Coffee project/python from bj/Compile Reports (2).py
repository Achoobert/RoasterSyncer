import os

#from FixThermals import *
#from FixVoltages import *

Directory = 'J:\\ETPShare\\NERC - TPL\\2013\\By hand\\N-2\\Violations\\Simplified\\'
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
			FileNames.append(f)
			print "%s" % f
	return FileNames


FileNames = []
FileNames = GetFileNames(Directory,ending)
DocFile=open(Directory+'Compiled.doc','w')

for Fname in FileNames:
	ViolFile=open(Directory+Fname,'r')
	DocFile.write('\n\n'+Fname+'\n')
	
	for line in ViolFile:
		line = line.strip('\f')
		if '\f' in line:
			#line = line.rstrip()
			line = line[:91]+'\n'
			print("new page found")
			print(line)
		DocFile.write(line)

#	if "Voltage" in Fname:
#		DocFile.write('\f')
	ViolFile.close()
DocFile.close()
