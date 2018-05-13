import csv
import operator
import Tkinter as tk
from Tkconstants import *
from tkFileDialog import askopenfilename
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import time
import sys


class FileReaderGUI:
	#Initiliaze class variables
	timeList = []
	fileList = []
	selectedList = []
	deselectedList =[]
	finishedUpdate = False

	def __init__(self):
		self.root = tk.Tk()
		self.root.title('')
		self.root.geometry("300x275")
		self.center(self.root)
		#Setting up Widgets
		#Input Frame
		self.inputFrame = tk.Frame(self.root)
		#Listbox
		self.lbFrame = tk.Frame(self.inputFrame)
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
		self.status = tk.Label(self.inputFrame,textvariable=self.statusVar,fg='red')
		self.statusVar.set('')
		self.status.pack()

		#Input File text frame
		self.textFrame = tk.LabelFrame(self.inputFrame,labelanchor='n',text='Input # minutes then click Add File')
		self.e = tk.Entry(self.textFrame)
		self.textFrame.pack()
		self.e.grid(row=0,column=0,padx=2,pady=3)
		self.b1 = tk.Button(self.textFrame,text='Add File',command=self.getTimeInput)
		self.b1.grid(row=0,column=1)

		# Run button
		self.b2 = tk.Button(self.inputFrame,text='Analyze Data',command=self.finishedInput)
		self.b2.pack()
		self.e.focus_set()
		self.root.bind('<Return>', self.getTimeInput)
		self.inputFrame.pack(side=LEFT,fill=BOTH,expand=1)

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
			# self.finishedUpdate = True
			self.statusVar.set('')
			self.dataTracker = runAnalysis(self.timeList,self.fileList)

			#Resize the screen
			self.root.geometry("1000x275")
			self.center(self.root)

			#DataFrame
			self.outputFrame = tk.Frame(self.root)
			self.dataSelectionFrame = tk.Frame(self.outputFrame)
			#DataSelectBox with y-scroll
			self.yDataDeselectedScroll = tk.Scrollbar(self.dataSelectionFrame, orient=tk.VERTICAL)
			self.dataDeselectedBox = tk.Listbox(self.dataSelectionFrame,width=30,
									yscrollcommand = self.yDataDeselectedScroll.set)
			self.yDataDeselectedScroll['command'] = self.dataDeselectedBox.yview

			#DataDeselectBox with y-scroll
			self.yDataSelectedScroll = tk.Scrollbar(self.dataSelectionFrame, orient=tk.VERTICAL)
			self.dataSelectedBox = tk.Listbox(self.dataSelectionFrame,width=30,yscrollcommand = self.yDataSelectedScroll.set)
			self.yDataSelectedScroll['command'] = self.dataSelectedBox.yview

			#Select/Deselct data frame
			self.selectionFrame = tk.Frame(self.dataSelectionFrame)
			#Select Button
			self.selectButton = tk.Button(self.selectionFrame,text='>>',command=self.selectData)
			self.selectButton.pack(side = TOP,padx=5)
			#Deselect Button
			self.deselectButton = tk.Button(self.selectionFrame,text='<<',command=self.deselectData)
			self.deselectButton.pack(side = TOP,padx=5)

			#CSV Output Frame
			self.CSVOutFrame = tk.LabelFrame(self.outputFrame,labelanchor='n',text='Add filename (default is "output")')
			self.CSVFileEntry = tk.Entry(self.CSVOutFrame)
			self.CSVButton = tk.Button(self.CSVOutFrame,text='CSV Output',command=self.outputCSV)
			self.CSVButton.pack(side=RIGHT)
			self.CSVFileEntry.pack(side=RIGHT)
			
			#Packing
			self.yDataSelectedScroll.pack(side = RIGHT,fill=Y)
			self.dataSelectedBox.pack(side = RIGHT,fill=BOTH,expand=1,padx=5,pady=5)
			self.selectionFrame.pack(side=RIGHT)
			self.yDataDeselectedScroll.pack(side = RIGHT,fill=Y)
			
			self.dataDeselectedBox.pack(side = RIGHT,fill=BOTH,expand=1,padx=5,pady=5)
			self.dataSelectionFrame.pack(side=TOP,fill=BOTH,expand=1)
			self.CSVOutFrame.pack(side=TOP,pady=5)
			self.outputFrame.pack(side=RIGHT,fill=BOTH,expand=1)

			self.addDataSets(self.dataTracker)
		else:
			self.statusVar.set('Cannot run data analysis without any files added')

	def addDataSets(self,dataTracker):
		nameList = ['High_Tracked_Dataset','Low_Tracked_Dataset','High_Persistent_Tracked_Dataset','Low_Persistent_Tracked_Dataset']

		#Loop after the nameList and add all to the deselected box and list
		for idx, name in enumerate(nameList):
			self.dataDeselectedBox.insert(idx,name)
			self.deselectedList.append(name)

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

	def selectData(self):
		currentIndex = self.dataDeselectedBox.curselection()
		if currentIndex:
			currDataSet = self.dataDeselectedBox.get(currentIndex)
			self.dataSelectedBox.insert(END,currDataSet)
			self.selectedList.append(self.deselectedList[currentIndex[0]])
			self.dataDeselectedBox.activate(currentIndex[0]+1)
			self.dataDeselectedBox.delete(currentIndex)
			del self.deselectedList[currentIndex[0]]
		else:
			self.statusVar.set('Nothing Selected to Move')
		return

	def deselectData(self):
		currentIndex = self.dataSelectedBox.curselection()
		if currentIndex:
			currDataSet = self.dataSelectedBox.get(currentIndex)
			self.dataDeselectedBox.insert(END,currDataSet)
			self.deselectedList.append(self.selectedList[currentIndex[0]])
			self.dataSelectedBox.activate(currentIndex[0]+1)
			self.dataSelectedBox.delete(currentIndex)
			del self.selectedList[currentIndex[0]]
		else:
			self.statusVar.set('Nothing Selected to Move')
		return

	def outputCSV(self):
		filename = self.CSVFileEntry.get()
		self.CSVFileEntry.delete(0,tk.END)
		if filename:
			filename = filename + '.csv'
		else:
			filename = 'output.csv'
		CSVGenerator(self.dataTracker,filename,self.selectedList)

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
		#Initialize variables
		self.rawData = []
		self.numRows = 0
		self.filename = filename
		self.timeValue = timeValue

		#Read in the data from the csvfile provided
		with open(filename, 'rU') as csvfile:
			reader = csv.reader(csvfile)
			self.titles = next(reader)
			for row in reader:
			 	self.rawData.append(row)
			 	self.numRows += 1

		#Sort all of the data
		self.sortData()
		#Check that there is enough data to fill the top list before assigning
		assert self.numRows >= topNumber,'Must have data for listing top set'
		self.topNumber = topNumber

		#Grap the highest and lowest datasets
		self.grabHighLow()

	def sortData(self):
		#Sorting for log2(WT0 FPKM) first and then gene name second
		self.sortedLog2WT_Ascending = sorted(self.rawData, key=lambda rows: 
													(float(rows[4]),rows[0]))
		self.sortedLog2WT_Descending = sorted(self.rawData, key=lambda rows: 
													(-float(rows[4]),rows[0]))
		#Sorting for log2(MUT0 FPKM) first and then gene name second
		self.sortedLog2MUT_Ascending = sorted(self.rawData, key=lambda rows:
													(float(rows[5]),rows[0]))
		self.sortedLog2MUT_Descending = sorted(self.rawData, key=lambda rows:
													(-float(rows[5]),rows[0]))
	
	def grabHighLow(self):
		#Initialize the internal datasets
		self.sortedLog2WT_High = []
		self.sortedLog2WT_Low = []
		self.sortedLog2MUT_High = []
		self.sortedLog2MUT_Low = []
		self.sortedLog2MUT_High_Unique = []
		self.sortedLog2MUT_Low_Unique = []

		#Generate temporary name lists
		WTHighListNames = []
		WTLowListNames = []
		data_length = len(self.sortedLog2WT_Ascending)
		for i in range(0,self.topNumber):
			#Record all of the lowest log2 values for WT and MUT
			self.sortedLog2WT_Low.append(self.sortedLog2WT_Ascending[i])
			self.sortedLog2MUT_Low.append(self.sortedLog2MUT_Ascending[i])
			WTLowListNames.append(self.sortedLog2WT_Ascending[i][0])

			self.sortedLog2WT_High.append(self.sortedLog2WT_Descending[i])
			self.sortedLog2MUT_High.append(self.sortedLog2MUT_Descending[i])
			WTHighListNames.append(self.sortedLog2WT_Descending[i][0])

		#Make a list of MUT vals that don't exist in the corresponding WT list
		for i in range(0,self.topNumber):
			if not isInList(self.sortedLog2MUT_Ascending[i][0],
							WTLowListNames):
				self.sortedLog2MUT_Low_Unique.append(self.sortedLog2MUT_Ascending[i])

			if not isInList(self.sortedLog2MUT_Descending[i][0],
							WTHighListNames):
				self.sortedLog2MUT_High_Unique.append(self.sortedLog2MUT_Descending[i])

	#Get functions for all of the different datasets
	def getFilename(self):
		return self.filename
	def getTimeValue(self):
		return self.timeValue
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
	def getSortedLog2MUTAscending(self):
		return self.sortedLog2MUT_Ascending
	def getSortedLog2MUTDescending(self):
		return self.sortedLog2MUT_Descending
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
	def __init__(self, dataAnalyzerList):
		#Create an class dataList from input provided
		self.dataAnalyzerList = dataAnalyzerList

		#Track the data over the course of the time range
		self.trackUniqueData()

		#Filter out data that is not siginificant over the full time range
		self.filterNonSignifigantData()
		# self.getAllData()

	def trackUniqueData(self):
		#Initialize class variables
		self.trackedDataSet_High = []
		self.trackedDataSet_Low = []

		MUTHighListNames = []
		MUTLowListNames = []

		#Loop over all of the dataAnlyzers in the list
		for dataAnalyzer in self.dataAnalyzerList:
			#If data name is not in the high list already, add it in
			for datapoint in dataAnalyzer.getUniqueHighSortedLog2MUT():
				if not isInList(datapoint[0],MUTHighListNames):
					MUTHighListNames.append(datapoint[0])
			#If data name is not in the low list already, add it in
			for datapoint in dataAnalyzer.getUniqueLowSortedLog2MUT():
				if not isInList(datapoint[0],MUTLowListNames):
					MUTLowListNames.append(datapoint[0])

		#Loop through list of all the data to track
		for dataName in MUTHighListNames:
			trackedDataGroup = []
			#If the dataName exists in any of the dataAnalyzers raw data, include it in the datagroup
			for dataAnalyzer in self.dataAnalyzerList:
				rawData = dataAnalyzer.getRawData()
				for rawDatapoint in rawData:
					labeledData = []
					if rawDatapoint[0] == dataName:
						labeledData.append(dataAnalyzer.getTimeValue())
						labeledData.extend(rawDatapoint)
						trackedDataGroup.append(labeledData)
						break
			#Append the datagroup into the larger dataset
			self.trackedDataSet_High.append(trackedDataGroup)

		#Loop through list of all the data to track
		for dataName in MUTLowListNames:
			trackedDataGroup = []
			#If the dataName exists in any of the dataAnalyzers raw data, include it in the datagroup
			for dataAnalyzer in self.dataAnalyzerList:
				rawData = dataAnalyzer.getRawData()
				for rawDatapoint in rawData:
					labeledData = []
					if rawDatapoint[0] == dataName:
						labeledData.append(dataAnalyzer.getTimeValue())
						labeledData.extend(rawDatapoint)
						trackedDataGroup.append(labeledData)
						break
			#Append the datagroup into the larger dataset
			self.trackedDataSet_Low.append(trackedDataGroup)

	# def getAllData(self):
	# 	rawDataList = []
	# 	for dataAnalyzer in self.dataAnalyzerList:
	# 		rawData = dataAnalyzer.getRawData()
	# 		rawDataNames = [datapoint[0] for datapoint in rawDataList]
	# 		for datapoint in rawData:
	# 			if not isInList(datapoint[0],rawDataNames):
	# 				rawDataList.append(datapoint[0])
	# 	self.allRawData = []
	# 	for name in rawDataList:
	# 		dataSet = []
	# 		for dataAnalyzer in self.dataAnalyzerList:
	# 			rawData = dataAnalyzer.getRawData()
	# 			dataNames = [datapoint[0] for datapoint in rawData]
	# 			if isInList(name,dataNames):
	# 				for rawDatapoint in rawData:
	# 					if rawDatapoint[0] == name:
	# 						dataSet.append(rawDatapoint)
	# 						break
	# 		# self.allRawData.append(dataSet)

	def filterNonSignifigantData(self):
		#Get the length of the data analyzer list
		lengthList = len(self.dataAnalyzerList)

		#Initialize class members
		self.persistentTrackedData_Low =[]
		self.persistentTrackedData_High = []

		#Get all the datagroups that are significant during the full time range
		for dataset in self.trackedDataSet_Low:
			if len(dataset)==lengthList:
				self.persistentTrackedData_Low.append(dataset)

		for dataset in self.trackedDataSet_High:
			if len(dataset)==lengthList:
				self.persistentTrackedData_High.append(dataset)
				
	def getTrackedDataHigh(self):
		return self.trackedDataSet_High
	def getTrackedDataLow(self):
		return self.trackedDataSet_Low
	def getPersistentTrackedDataLow(self):
		return self.persistentTrackedData_Low
	def getPersistentTrackedDataHigh(self):
		return self.persistentTrackedData_High

class CSVGenerator:
	def __init__(self, dataTracker,filename,dataNameList):
		self.dataTracker = dataTracker
		try:
			os.remove(filename)
		except:
			pass

		self.csvfile = open(filename, 'w+')
		self.csvwriter = csv.writer(self.csvfile, delimiter=',')
		self.writeToFile(dataNameList)

	def writeToFile(self,dataNameList):
		#Call functions for writing all the neccessary data
		nameList = ['High_Tracked_Dataset','Low_Tracked_Dataset','High_Persistent_Tracked_Dataset','Low_Persistent_Tracked_Dataset']
		for dataName in dataNameList:
			if dataName == 'High_Persistent_Tracked_Dataset':
				self.writeMultDataSet(self.dataTracker.getPersistentTrackedDataHigh(),
					'High_Persistent_Tracked_Dataset')
			if dataName == 'Low_Persistent_Tracked_Dataset':
				self.writeMultDataSet(self.dataTracker.getPersistentTrackedDataLow(),'Low_Persistent_Tracked_Dataset')
			if dataName == 'High_Tracked_Dataset':
				self.writeMultDataSet(self.dataTracker.getTrackedDataHigh(),
					'High_Tracked_Dataset')
			if dataName == 'Low_Tracked_Dataset':
				self.writeMultDataSet(self.dataTracker.getTrackedDataLow(),
					'Low_Tracked_Dataset')
		self.closeFile()

	def writeColumnTitles(self):
		#Write the column titles
		self.csvwriter.writerow(['Time [min]','Test ID','Gene','Locus','Status','log2(WT FPKM)','log2(MUT FPKM)','log2(Ratio)','q Value','Significant'])

	def writeMultDataSet(self,dataCluster,title):
		#Write a data set with multiple datapoints in each
		self.csvwriter.writerow([title])
		self.writeColumnTitles()
		for dataGroup in dataCluster:
			for datapoint in dataGroup:
				self.csvwriter.writerow(datapoint)
		self.csvwriter.writerow('')
		
	def closeFile(self):
		self.csvfile.close()

def runAnalysis(timeList,fileList):
	dataAnalyzerList = [DataAnalyzer(fileList[i],timeList[i]) for i in range(len(fileList))]
	return DataTracker(dataAnalyzerList)

def main():
	DEBUG = False
	for arg in sys.argv[1:]:
		if arg.lower() == 'debug':
			DEBUG = True

	if DEBUG:
		fileList = ['/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_0.csv', '/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_15.csv', '/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_2.csv']
		timeList = [0.0, 15.0, 120.0]
		runAnalysis(timeList,fileList)
	else:
		fileReader = FileReaderGUI()
		fileReader.updateFiles()
		# fileList = fileReader.getFileList()
		# timeList = fileReader.getTimeList()

	if False:
		dataAnalyzerList = [DataAnalyzer(fileList[i],timeList[i]) for i in range(len(fileList))]
		dataTracker = DataTracker(dataAnalyzerList)

		csvGen = CSVGenerator(dataTracker,'test.csv')

	
		persistentTrackedData_High = dataTracker.persistentTrackedData_High
		heatMapArray = np.zeros((len(persistentTrackedData_High),len(persistentTrackedData_High[0])))
		i = 0;
		j = 0;
		titles = []
		for dataGroup in persistentTrackedData_High:
			j = 0
			titles.append(persistentTrackedData_High[i][j][0])
			for datapoint in dataGroup:
				heatMapArray[i][j] = persistentTrackedData_High[i][j][5]
				j+= 1
			i+=1

		colors =  [(0, 0, 0.5),(1, 1, 0)]
		cm = LinearSegmentedColormap.from_list(
	    'PrincessPerfection', colors, N=100)

		plt.ioff()
		fig, ax = plt.subplots()
		heatmap = ax.imshow(heatMapArray,interpolation='nearest', cmap=cm)
		plt.colorbar(heatmap)

		# We want to show all ticks...
		ax.set_xticks(np.arange(len(timeList)))
		ax.set_yticks(np.arange(len(titles)))
		# ... and label them with the respective list entries
		ax.set_xticklabels(timeList)
		ax.set_yticklabels(titles)

		# Rotate the tick labels and set their alignment.
		plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
		         rotation_mode="anchor")

		# Loop over data dimensions and create text annotations.
		# for i in range(len(timeList)):
		#     for j in range(len(titles)):
		#         text = ax.text(j, i, heatMapArray[i, j],
		#                        ha="center", va="center", color="w")

		ax.set_title("Heat Map")
		fig.tight_layout()
		plt.show()
		# while 1:
		# 	time.sleep(10)


if __name__ == "__main__":
	main()
	