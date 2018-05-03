import csv
import operator
import Tkinter as tk
from Tkconstants import *
from tkFileDialog import askopenfilename
import matplotlib.pyplot as plt

class FileReaderGUI:
	#TODO: Map timeList and fileList when tracking data
	#TODO: Make distructor for GUI
	#TODO: Make it so the GUI will stay open
	

	def __init__(self):
		self.timeList = []
		self.fileList = []
		self.finishedUpdate = False
		self.root = tk.Tk()
		self.root.title('')
		self.root.geometry("300x275")
		self.center(self.root)
		#Setting up Widgets
		#Listbox
		self.lbFrame = tk.Frame(self.root)
		self.yScroll = tk.Scrollbar(self.lbFrame, orient=tk.VERTICAL)
		self.lb = tk.Listbox(self.lbFrame,width=30,
								yscrollcommand = self.yScroll.set)
		self.yScroll['command'] = self.lb.yview
		self.deleteButton = tk.Button(self.lbFrame,text='Delete',command=self.deleteFile)
		self.deleteButton.pack(side = RIGHT,padx=5)
		self.yScroll.pack(side = RIGHT,fill=Y)
		self.lb.pack(side = RIGHT,fill=BOTH,expand=1,padx=5)
		self.lbFrame.pack(fill=BOTH,expand=1)

		#Input File text frame
		self.statusVar = tk.StringVar()
		self.status = tk.Label(self.root,textvariable=self.statusVar,fg='red')
		self.statusVar.set('')
		self.status.pack()

		#Input File text frame
		self.textFrame = tk.LabelFrame(self.root,labelanchor='n',text='Input # minutes then click Add File')
		self.e = tk.Entry(self.textFrame)
		self.textFrame.pack()
		self.e.grid(row=0,column=0,padx=2,pady=3)
		self.b1 = tk.Button(self.textFrame,text='Add File',command=self.getTimeInput)
		self.b1.grid(row=0,column=1)

		# Run button
		self.b2 = tk.Button(self.root,text='Run',command=self.finishedInput)
		self.b2.pack()
		self.e.focus_set()
		self.root.bind('<Return>', self.getTimeInput)

	def getTimeInput(self,event=None):
		inputString = self.e.get()
		self.e.delete(0,tk.END)
		if inputString:
			try:
				userInput = float(inputString)
				self.getFileName(userInput)
				self.statusVar.set('')
			except ValueError:
				self.statusVar.set('Input must be a numeric minute value')

	def getFileName(self,timeValue):
		filename = askopenfilename()
		if filename:
			self.statusVar.set('')
			self.fileList.append(filename)
			self.timeList.append(timeValue)
			filename = filename.split('/')
			displayOutput = str(timeValue)+'  '+filename[-1]
			self.lb.insert(len(self.fileList)-1,displayOutput)
			

	def finishedInput(self):
		if self.timeList:
			self.finishedUpdate = True
			self.statusVar.set('')
		else:
			self.statusVar.set('Cannot run data analysis without any files added')

	def updateFiles(self):
		while not self.finishedUpdate:
			self.root.update_idletasks()
			self.root.update()

	def center(self,toplevel):
		toplevel.update_idletasks()
		w = toplevel.winfo_screenwidth()
		h = toplevel.winfo_screenheight()
		size = tuple(int(_) for _ in (
								toplevel.geometry().split('+')[0].split('x')))
		x = w/2 - size[0]/2
		y = h/2 - size[1]/2
		toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))

	def deleteFile(self):
		currentIndex = self.lb.curselection()
		if currentIndex:
			self.lb.activate(currentIndex[0]+1)
			self.lb.delete(currentIndex)
			del self.timeList[currentIndex[0]]
			del self.fileList[currentIndex[0]]
		else:
			self.statusVar.set('Nothing Selected to Delete')

	def getFileList(self):
		return self.fileList

	def getTimeList(self):
		return self.timeList

def isInList(testVal,testList):
	for evalString in testList:
		if testVal == evalString:
			return True
	return False

class DataAnalyzer:
	def __init__(self,filename,timeValue,topNumber=100):
		self.rawData = []
		self.numRows = 0
		self.filename = filename
		self.timeValue = timeValue
		with open(filename, 'rU') as csvfile:
			reader = csv.reader(csvfile)
			self.titles = next(reader)
			for row in reader:
			 	self.rawData.append(row)
			 	self.numRows += 1
		self.sortData()
		assert self.numRows >= topNumber,'Must have data for listing top set'
		self.topNumber = topNumber
		self.grabHighLow(topNumber)
	
	def sortData(self):
		#Sorting for log2(WT0 FPKM)
		self.sortedLog2WT_Ascending = sorted(self.rawData, key=lambda rows: 
													(float(rows[4]),rows[0]))
		self.sortedLog2WT_Descending = sorted(self.rawData, key=lambda rows: 
													(-float(rows[4]),rows[0]))
		#Sorting for log2(MUT0 FPKM)
		self.sortedLog2MUT_Ascending = sorted(self.rawData, key=lambda rows:
													(float(rows[5]),rows[0]))
		self.sortedLog2MUT_Descending = sorted(self.rawData, key=lambda rows:
													(-float(rows[5]),rows[0]))
	def grabHighLow(self,topNumber):
		self.topNumber = topNumber
		self.sortedLog2WT_High = []
		WTHighListNames = []
		self.sortedLog2WT_Low = []
		WTLowListNames = []
		self.sortedLog2MUT_High = []
		self.sortedLog2MUT_Low = []
		self.sortedLog2MUT_High_Unique = []
		self.sortedLog2MUT_Low_Unique = []

		data_length = len(self.sortedLog2WT_Ascending)
		for i in range(0,topNumber):
			self.sortedLog2WT_Low.append(self.sortedLog2WT_Ascending[i])
			self.sortedLog2MUT_Low.append(self.sortedLog2MUT_Ascending[i])
			WTLowListNames.append(self.sortedLog2WT_Ascending[i][0])
			self.sortedLog2WT_High.append(self.sortedLog2WT_Descending[i])
			self.sortedLog2MUT_High.append(self.sortedLog2MUT_Descending[i])
			WTHighListNames.append(self.sortedLog2WT_Descending[i][0])
		for i in range(0,topNumber):
			if not isInList(self.sortedLog2MUT_Ascending[i][0],WTLowListNames):
				self.sortedLog2MUT_Low_Unique.append(self.sortedLog2MUT_Ascending[i])
			if not isInList(self.sortedLog2MUT_Descending[i][0],WTHighListNames):
				self.sortedLog2MUT_High_Unique.append(self.sortedLog2MUT_Descending[i])

	def getTitles(self):
		return self.titles
	def getTopNumber(self):
		return self.topNumber
	def getRawData(self):
		return self.rawData
	def getSortedLog2WTAscending(self):
		return self.sortedLog2WT_Ascending
	def getSortedLog2WTDescending(self):
		return self.sortedLog2WT_Descending
	def getSortedLog2MutAscending(self):
		return self.sortedLog2WT_Ascending
	def getSortedLog2MutDescending(self):
		return self.sortedLog2WT_Descending
	def getHighSortedLog2WT(self):
		return self.sortedLog2WT_High
	def getLowSortedLog2WT(self):
		return self.sortedLog2WT_Low
	def getHighSortedLog2MUT(self):
		return self.sortedLog2MUT_High
	def getLowSortedLog2MUT(self):
		return self.sortedLog2MUT_Low
	def getUniqueHighSortedLog2MUT(self):
		return self.sortedLog2MUT_High_Unique
	def getUniqueLowSortedLog2MUT(self):
		return self.sortedLog2MUT_Low_Unique

class DataTracker:
	"""docstring for ClassName"""
	def __init__(self, dataAnalyzerList):
		self.dataAnalyzerList = dataAnalyzerList
		self.trackedDataSet = []
		self.trackUniqueData()
		self.findPersistentData()

	def trackUniqueData(self):
		self.trackedUniqueHighNames = []
		self.trackedUniqueLowNames = []
		self.trackedUniqueLog2MUT_High = []
		self.trackedUniqueLog2MUT_Low = []
		self.trackedDataSet_High = []
		self.trackedDataSet_Low = []
		for dataAnalyzer in self.dataAnalyzerList:
			sortedLog2MUT_High_Unique = (
									dataAnalyzer.getUniqueHighSortedLog2MUT())
			sortedLog2MUT_Low_Unique = dataAnalyzer.getUniqueLowSortedLog2MUT()
			WTHighListNames = [datapoint[0] for datapoint in 
												self.trackedUniqueLog2MUT_High]
			WTLowListNames = [datapoint[0] for datapoint in 
												self.trackedUniqueLog2MUT_Low]
			for datapoint in sortedLog2MUT_High_Unique:
				if not isInList(datapoint[0],WTHighListNames):
					self.trackedUniqueLog2MUT_High.append(datapoint)
			for datapoint in sortedLog2MUT_Low_Unique:
				if not isInList(datapoint[0],WTLowListNames):
					self.trackedUniqueLog2MUT_Low.append(datapoint)
		for trackDatapoint in self.trackedUniqueLog2MUT_High:
			trackedDataGroup = []
			for dataAnalyzer in self.dataAnalyzerList:
				rawData = dataAnalyzer.getRawData()
				for rawDatapoint in rawData:
					if rawDatapoint[0] == trackDatapoint[0]:
						trackedDataGroup.append(rawDatapoint)
						break
			self.trackedDataSet_High.append(trackedDataGroup)
		for trackDatapoint in self.trackedUniqueLog2MUT_Low:
			trackedDataGroup = []
			for dataAnalyzer in self.dataAnalyzerList:
				rawData = dataAnalyzer.getRawData()
				for rawDatapoint in rawData:
					if rawDatapoint[0] == trackDatapoint[0]:
						trackedDataGroup.append(rawDatapoint)
						break
			self.trackedDataSet_Low.append(trackedDataGroup)

	def findPersistentData(self):
		self.persistentTrackedData_High = []
		for dataset in self.trackedDataSet_High:
			if len(dataset)==3:
				self.persistentTrackedData_High.append(dataset)
		self.persistentTrackedData_Low = []
		for dataset in self.trackedDataSet_Low:
			if len(dataset)==3:
				self.persistentTrackedData_Low.append(dataset)
				
	def getTrackedDataHigh(self):
		return self.trackedDataSet_High
	def getTrackedDataLow(self):
		return self.trackedDataSet_Low

class CSVGenerator:
	"""docstring for ClassName"""
	def __init__(self, dataTracker,filename):
		self.dataTracker = dataTracker
		try:
			os.remove(filename)
		except:
			pass

		self.csvfile = open(filename, 'w+')
		self.csvwriter = csv.writer(self.csvfile, delimiter=',')
		self.writeToFile()

		# self.DataTracker.trackedUniqueHighNames
		# self.DataTracker.trackedUniqueLowNames
		# self.DataTracker.trackedUniqueLog2MUT_High
		# self.DataTracker.trackedUniqueLog2MUT_Low
		# self.DataTracker.trackedDataSet_High
		# self.DataTracker.trackedDataSet_Low
		# self.DataTracker.persistentTrackedData_High
		

	def writeToFile(self):
		self.writeMultDataSet(self.dataTracker.persistentTrackedData_High,'persistentTrackedData_High')
		self.writeMultDataSet(self.dataTracker.persistentTrackedData_Low,'persistentTrackedData_Low')
		self.closeFile()

	def writeTitle(self):
		self.csvwriter.writerow(['Time [min]','Test ID','Gene','Locus','Status','log2(WT0 FPKM)','log2(MUT0 FPKM)','log2(Ratio)','q Value','Significant'])

	def writeMultDataSet(self,dataCluster,title):
		self.csvwriter.writerow([title])
		self.writeTitle()
		for dataGroup in dataCluster:
			counter = 0
			for datapoint in dataGroup:
				dataRow=[self.dataTracker.dataAnalyzerList[counter].timeValue]
				dataRow.extend(datapoint)
				self.csvwriter.writerow(dataRow)
				counter+=1
		self.csvwriter.writerow('')
		
	def closeFile(self):
		self.csvfile.close()


if __name__ == "__main__":
	fileReader = FileReaderGUI()
	fileReader.updateFiles()

	dataAnalyzerList = [DataAnalyzer(fileList[i],timeList[i]) for i in range(len(fileList))]
	dataTracker = DataTracker(dataAnalyzerList)

	csvGen = CSVGenerator(dataTracker,'test.csv')