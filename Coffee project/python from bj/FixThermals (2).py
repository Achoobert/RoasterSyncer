import os

Directory = 'J:\\ETPShare\\NERC - TPL\\2013\\By hand\\N-2\\Violations\\'
# Fname = '2017HS_MTd_N-1-79A_Thermal'
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
FileNames = GetFileNames(Directory+"Originals\\",'Thermal.txt')

for Fname in FileNames:
	f=open(Directory+"Originals\\"+Fname+ending,'r')
	g=open(DirectorySimplified+Fname+'-S'+ending,'w')

	for i in range(0,9):
		line = f.readline()
		line = line.strip('\f')
		if ("OUTPUT FOR AREA" not in line):
			print line
			g.write(line)
	for line in f:
		if '\f' in line:	# To eliminate the "\f    PTI INTERACTIVE" at the end of the last line of thermal data
			line = line[:91]+'\n'
		if ("MT. DETAIL EMBEDDED IN" in line) or ("WECC" in line) or ("X--------- FROM BUS" in line) or ("BUS# X-- NAME --X BASKV" in line) or ("SUBSYSTEM LOADING CHECK" in line) or ("LOADINGS ABOVE" in line) or ("OUTPUT FOR AREA" in line) or ("* NONE *" in line) or (line == "\n"):
			print "Deleted"
		else:
			WriteIt = 0
			try:
				ierr = 0
				BaseKV1 = float(line[19:25])
				BaseKV2 = float(line[51:57])
				print BaseKV1,BaseKV2
			except ValueError:		# This happens if the Bus#... titles are encountered
				ierr = 1
				WriteIt = 1
				print "ValueError"
			if (not ierr):
				if (BaseKV1 >= 50) and (BaseKV2 >= 50):
					WriteIt = 1
			if WriteIt:
				g.write(line)

	f.close()
	g.close()
