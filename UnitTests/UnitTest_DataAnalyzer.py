import unittest
import pandas as pd
import sys
sys.path.insert(0, '/Users/kywoodard/Documents/WhereTheWildTypesAre/')
from SortingScript import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
	def setUp(self):
		filePathList = [
		'/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_0.csv',
		'/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_15.csv',
		'/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_2.csv',
		]
		timeList = [0.0, 15.0, 120.0]

		self.DA_List = [DataAnalyzer(filePathList[i],timeList[i]) for i in range(len(filePathList))]

		#Use a different CSV Reader (Pandas) to verify that the some amount of data was read in
		self.numPandaRows = []
		self.numPandaCols = []
		self.pandaData = []
		for filePath in filePathList:
			df = pd.read_csv(filePath,header=None)
			shape = df.shape
			self.numPandaRows.append(shape[0]-1)
			self.numPandaCols.append(shape[1])
			self.pandaData.append(df)

	#TODO: Check back in on the replecated date naming for the data files
	# def checkRawDataUnique(self,dataAnalyzer):
		# for i in range(len(dataAnalyzer.rawData)):
		# 	for j in range(i+1,len(dataAnalyzer.rawData)):
		# 		if dataAnalyzer.rawData[i][0] == dataAnalyzer.rawData[j][0]:
		# 			print i, dataAnalyzer.rawData[i][0]
		# 			print j, dataAnalyzer.rawData[j][0]
		# 			print dataAnalyzer.numRows
		# 			assert dataAnalyzer.rawData[i][0] != dataAnalyzer.rawData[j][0], 'Raw data from file has to all have unique names'

	def checkSorted(self,data,columnNum,sortedAscending = 1):
		#If the list should be ascending as it goes down (lowest values first)
		if sortedAscending:
			#Get the first datapoints value
			oldValue = float(data[0][columnNum])
			#Loop through checking that the new value is always greater
			for datapoint in data:
				if float(datapoint[columnNum]) < oldValue:
					return 0
				#Reset the old value
				oldValue = float(datapoint[columnNum])

		#If the list should be ascending as it goes down (highest values first)
		else:
			#Get the first datapoints value
			oldValue = float(data[0][columnNum])
			#Loop through checking that the new value is always greater
			for datapoint in data:
				if float(datapoint[columnNum]) > oldValue:
					return 0
				#Reset the old value
				oldValue = float(datapoint[columnNum])
		return 1

	def test_checkTitles(self):
		# Check for each of the dataAnlyzers created
		oldAnalyzer = []
		for dataAnalyzer in self.DA_List:
			self.assertTrue(oldAnalyzer != dataAnalyzer, 'dataAnalyzer is the same as last check')
			oldAnalyzer = dataAnalyzer
			#Create all of the appropriate titl lists
			all_titles = []
			pre_titles = ['Test ID', 'Gene', 'Locus', 'Status']
			mod_titles = ['log2(WT0 FPKM)', 'log2(MUT0 FPKM)']
			post_titles = ['log2(Ratio)', 'q Value', 'Significant']
			all_titles.extend(pre_titles)
			all_titles.extend(mod_titles)
			all_titles.extend(post_titles)

			#Get the titles from the analyzer
			titles = dataAnalyzer.getTitles()
			self.assertEqual(len(all_titles),len(titles),'Titles are not correct length')

			#Check the first 4 titles
			self.assertEqual(pre_titles,titles[0:4],'Titles are not of standard form')
			#Check 
			self.assertEqual(mod_titles[0][0:7],titles[4][0:7],'Titles are not of standard form')
			self.assertEqual(mod_titles[1][0:8],titles[5][0:8],'Titles are not of standard form')
			self.assertEqual(post_titles,titles[6:9],'Titles are not of standard form')

	def test_RawData(self):
		# Check for each of the dataAnlyzers created
		index = 0
		oldAnalyzer = []
		for dataAnalyzer in self.DA_List:
			self.assertTrue(oldAnalyzer != dataAnalyzer, 'dataAnalyzer is the same as last check')
			oldAnalyzer = dataAnalyzer
			#Get the raw data
			rawData = dataAnalyzer.getRawData()

			#Check that the rawData is not empty
			num_datapoints = len(rawData)
			lengthFirstDatapoint = len(rawData[0])
			self.assertEqual(num_datapoints,(self.numPandaRows[index]), 'Panda read a different row count than CSV Reader')
			self.assertTrue(lengthFirstDatapoint != self.numPandaCols, 'Panda read a different column count than CSV Reader')

			#Check that all of the datapoints have the same length

			data_index = 1
			for datapoint in rawData:
				self.assertTrue( len(datapoint) == lengthFirstDatapoint, 'All datapoints need to have the same length')

				#Compare all the datapoints to the panda data to verify they were read in correctly
				col_index = 0
				for testVal in datapoint:
					self.assertEqual(testVal,self.pandaData[index][col_index][data_index], 'All datapoints need to match pandas data')
					col_index+=1
				data_index+=1
			index+=1
	
	def test_SortedData(self):
		# Check for each of the dataAnlyzers created
		index = 0
		oldAnalyzer = []
		for dataAnalyzer in self.DA_List:
			self.assertTrue(oldAnalyzer != dataAnalyzer, 'dataAnalyzer is the same as last check')
			oldAnalyzer = dataAnalyzer
			#Define columns to find the appropriate log2 values for WT and MUT
			WTcol = 4
			MUTcol = 5

			#Check the lengths of sorted lists
			self.assertEqual(self.numPandaRows[index],len(dataAnalyzer.getSortedLog2WTAscending()),'sortedLog2WTAscending lost data while being sorted')
			self.assertEqual(self.numPandaRows[index],len(dataAnalyzer.getSortedLog2WTDescending()),'sortedLog2WTDescending lost data while being sorted')
			self.assertEqual(self.numPandaRows[index],len(dataAnalyzer.getSortedLog2MUTAscending()),'sortedLog2MUTAscending lost data while being sorted')
			self.assertEqual(self.numPandaRows[index],len(dataAnalyzer.getSortedLog2MUTDescending()),'sortedLog2MUTDescending lost data while being sorted')

			#Check if each of the lists Ascending/Descending is sorted properly
			self.assertTrue( self.checkSorted(dataAnalyzer.getSortedLog2WTAscending(),WTcol,1), 'sortedLog2WTAscending is not properly sorted')
			self.assertTrue( self.checkSorted(dataAnalyzer.getSortedLog2WTDescending(),WTcol,0), 'sortedLog2WTDescending is not properly sorted')
			self.assertTrue( self.checkSorted(dataAnalyzer.getSortedLog2MUTAscending(),MUTcol,1), 'sortedLog2MUTAscending is not properly sorted')
			self.assertTrue( self.checkSorted(dataAnalyzer.getSortedLog2MUTDescending(),MUTcol,0), 'sortedLog2MUTDescending is not properly sorted')

			#Check nonsorted lists to verify the checkSorted script is working
			rawData = dataAnalyzer.getRawData()
			datapoints = 100
			for i in range(0,len(rawData),datapoints):
				self.assertFalse( self.checkSorted(rawData[i:i+datapoints],WTcol,1), 'rawData should not be sorted')
				self.assertFalse( self.checkSorted(rawData[i:i+datapoints],WTcol,0), 'rawData should not be sorted')
				self.assertFalse( self.checkSorted(rawData[i:i+datapoints],MUTcol,1), 'rawData should not be sorted')
				self.assertFalse( self.checkSorted(rawData[i:i+datapoints],MUTcol,0), 'rawData should not be sorted')	

			index += 1	

	def test_PulledHighLow(self):
		# Check for each of the dataAnlyzers created
		oldAnalyzer = []
		for dataAnalyzer in self.DA_List:
			self.assertTrue(oldAnalyzer != dataAnalyzer, 'dataAnalyzer is the same as last check')
			oldAnalyzer = dataAnalyzer
			#Get topNumber and sorted lists
			topNumber = dataAnalyzer.getTopNumber()
			sortedLog2WTAscending = dataAnalyzer.getSortedLog2WTAscending()
			sortedLog2WTDescending = dataAnalyzer.getSortedLog2WTDescending()
			sortedLog2MUTAscending = dataAnalyzer.getSortedLog2MUTAscending()
			sortedLog2MUTDescending = dataAnalyzer.getSortedLog2MUTDescending()

			sortedLog2WT_High = dataAnalyzer.getHighSortedLog2WT()
			sortedLog2WT_Low = dataAnalyzer.getLowSortedLog2WT()
			sortedLog2MUT_High = dataAnalyzer.getHighSortedLog2MUT()
			sortedLog2MUT_Low = dataAnalyzer.getLowSortedLog2MUT()

			#Verify that the data lists are the appropriate length
			self.assertTrue( len(sortedLog2WT_High) == topNumber, 'sortedLog2WT_High is not correct length')
			self.assertTrue( len(sortedLog2WT_Low) == topNumber, 'sortedLog2WT_Low is not correct length')
			self.assertTrue( len(sortedLog2MUT_High) == topNumber, 'sortedLog2MUT_High is not correct length')
			self.assertTrue( len(sortedLog2MUT_Low) == topNumber, 'sortedLog2MUT_Low is not correct length')

			#Check all of the top lists to verify they match with their corresponding sorted list
			for i in range(topNumber):
				self.assertTrue( sortedLog2WTDescending[i] == sortedLog2WT_High[i], 'sortedLog2WT_High does not match sorted list')
				self.assertTrue( sortedLog2WTAscending[i] == sortedLog2WT_Low[i], 'sortedLog2WT_Low does not match sorted list')
				self.assertTrue( sortedLog2MUTDescending[i] == sortedLog2MUT_High[i], 'sortedLog2MUT_High does not match sorted list')
				self.assertTrue( sortedLog2MUTAscending[i] == sortedLog2MUT_Low[i], 'sortedLog2MUT_Low does not match sorted list')

	def test_UniqueValues(self):
		# Check for each of the dataAnlyzers created
		oldAnalyzer = []
		for dataAnalyzer in self.DA_List:
			self.assertTrue(oldAnalyzer != dataAnalyzer, 'dataAnalyzer is the same as last check')
			oldAnalyzer = dataAnalyzer

			#Loop through Unique High MUT list and High WT List making sure none of the values match
			for uniqueData in dataAnalyzer.getUniqueHighSortedLog2MUT():
				for testData in dataAnalyzer.getHighSortedLog2WT():
					self.assertTrue( uniqueData != testData, 'getUniqueHighSortedLog2MUT has one or more values belonging to getHighSortedLog2MWT as well')

			#Check that the Unique High MUT list exists in the high sorted list
			for uniqueData in dataAnalyzer.getUniqueHighSortedLog2MUT():
				check = False
				for testData in dataAnalyzer.getHighSortedLog2MUT():
					if testData == uniqueData:
						check = True
						break
				self.assertTrue( check, 'getUniqueHighSortedLog2MUT has one or more values not belonging to getHighSortedLog2MUT')

			#Loop through Unique Low MUT list and Low WT List making sure none of the values match
			for uniqueData in dataAnalyzer.getUniqueLowSortedLog2MUT():
				for testData in dataAnalyzer.getLowSortedLog2WT():
					self.assertTrue( uniqueData != testData, 'getUniqueLowSortedLog2MUT has non unique values')

			#Check that the Unique Low MUT list exists in the low sorted list
			for uniqueData in dataAnalyzer.getUniqueLowSortedLog2MUT():
				check = False
				for testData in dataAnalyzer.getLowSortedLog2MUT():
					if testData == uniqueData:
						check = True
				self.assertTrue( check, 'getUniqueLowSortedLog2MUT has values not belonging to getLowSortedLog2MUT')

if __name__ == '__main__':
	print "DataAnalyzer Unit Test:"
	unittest.main()
