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


class FileReaderGUI:
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
					if rawDatapoint[0] == dataName:
						rawDatapoint.append(dataAnalyzer.getTimeValue())
						trackedDataGroup.append(rawDatapoint)
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
					if rawDatapoint[0] == dataName:
						rawDatapoint.append(dataAnalyzer.getTimeValue())
						trackedDataGroup.append(rawDatapoint)
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

		#Get all the datagroups that are significant during the full tiem range
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
	def __init__(self, dataTracker,filename):
		self.dataTracker = dataTracker
		try:
			os.remove(filename)
		except:
			pass

		self.csvfile = open(filename, 'w+')
		self.csvwriter = csv.writer(self.csvfile, delimiter=',')
		self.writeToFile()

	def writeToFile(self):
		#Call functions for writing all the neccessary data
		self.writeMultDataSet(self.dataTracker.persistentTrackedData_High,'persistentTrackedData_High')
		self.writeMultDataSet(self.dataTracker.persistentTrackedData_Low,'persistentTrackedData_Low')
		self.closeFile()

	def writeColumnTitles(self):
		#Write the column titles
		self.csvwriter.writerow(['Time [min]','Test ID','Gene','Locus','Status','log2(WT FPKM)','log2(MUT FPKM)','log2(Ratio)','q Value','Significant'])

	def writeMultDataSet(self,dataCluster,title):
		#Write a data set with multiple datapoints in each
		self.csvwriter.writerow([title])
		self.writeColumnTitles()
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
	fileList = fileReader.getFileList()
	timeList = fileReader.getTimeList()
	# fileList = ['/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_0.csv', '/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_15.csv', '/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_2.csv']
	# timeList = [0.0, 15.0, 120.0]

	dataAnalyzerList = [DataAnalyzer(fileList[i],timeList[i]) for i in range(len(fileList))]
	dataTracker = DataTracker(dataAnalyzerList)

	csvGen = CSVGenerator(dataTracker,'test.csv')