from SortingScript import DataAnalyzer
import unittest

#TODO: Incorporate the data from the excel file output

class TestDataAnalyzer(unittest.TestCase):
	def setUp(self):
		filePathList = [
		'/Users/kywoodard/Documents/MarMar_SideProject/WTvsMut_15.csv',
		'/Users/kywoodard/Documents/MarMar_SideProject/WTvsMut_2.csv',
		'/Users/kywoodard/Documents/MarMar_SideProject/WTvsMut_0.csv']
		self.DA_List = [DataAnalyzer(filePathList[i]) for i in range(3)]
	#TODO: Check back in on the replecated date naming for the data files
	# def checkRawDataUnique(self,dataAnalyzer):
		# for i in range(len(dataAnalyzer.rawData)):
		# 	for j in range(i+1,len(dataAnalyzer.rawData)):
		# 		if dataAnalyzer.rawData[i][0] == dataAnalyzer.rawData[j][0]:
		# 			print i, dataAnalyzer.rawData[i][0]
		# 			print j, dataAnalyzer.rawData[j][0]
		# 			print dataAnalyzer.numRows
		# 			assert dataAnalyzer.rawData[i][0] != dataAnalyzer.rawData[j][0], 'Raw data from file has to all have unique names'

	#If sortLowToHigh is 1, the data is checked with low values expected first
	def checkSorted(self,data,columnNum,sortLowToHigh = 1):
		oldValue = float(data[0][columnNum])
		for datapoint in data:
			if sortLowToHigh == 1 and float(datapoint[columnNum]) < oldValue:
				return 0
			if sortLowToHigh == 0 and float(datapoint[columnNum]) > oldValue:
				return 0
			oldValue = float(datapoint[columnNum])
		return 1

	def test_checkTitles(self):
		for dataAnalyzer in self.DA_List:
			pre_titles = ['Test ID', 'Gene', 'Locus', 'Status']
			mod_titles = ['log2(WT0 FPKM)', 'log2(MUT0 FPKM)']
			post_titles = ['log2(Ratio)', 'q Value', 'Significant']
			titles = dataAnalyzer.getTitles()
			self.assertEqual(pre_titles,titles[0:4],'Titles are not of standar form')
			self.assertEqual(mod_titles[0][0:7],titles[4][0:7],'Titles are not of standar form')
			self.assertEqual(mod_titles[1][0:8],titles[5][0:8],'Titles are not of standar form')
			self.assertEqual(post_titles,titles[6:9],'Titles are not of standar form')

	def test_RawDataExists(self):
		for dataAnalyzer in self.DA_List:
			rawData = dataAnalyzer.getRawData()
			num_datapoints = len(rawData)
			self.assertTrue(num_datapoints != 0, 'The file must not be empty')
			lengthFirstDatapoint = len(rawData[0])
			for datapoint in rawData:
				self.assertTrue( len(datapoint) == lengthFirstDatapoint, 'All datapoints need to have the same length')
	
	def test_SortedData(self):
		for dataAnalyzer in self.DA_List:
			sortedLog2WT = dataAnalyzer.getSortedLog2WT()
			self.assertTrue( self.checkSorted(sortedLog2WT,4,1), 'sortedLog2WT is not properly sorted')
			sortedLog2MUT = dataAnalyzer.getSortedLog2MUT()
			self.assertTrue( self.checkSorted(sortedLog2MUT,5,1), 'sortedLog2MUT is not properly sorted')

	def test_PulledHighLow(self):
		for dataAnalyzer in self.DA_List:
			sortedLog2WT_High = dataAnalyzer.getHighSortedLog2WT()
			WTcol = 4
			MUTcol = 5
			self.assertTrue( self.checkSorted(sortedLog2WT_High,WTcol,0), 'sortedLog2WT_High is not properly sorted')
			sortedLog2WT_Low = dataAnalyzer.getLowSortedLog2WT()
			self.assertTrue( self.checkSorted(sortedLog2WT_Low,WTcol,1), 'sortedLog2WT_Low is not properly sorted')
			sortedLog2MUT_High = dataAnalyzer.getHighSortedLog2MUT()
			self.assertTrue( self.checkSorted(sortedLog2MUT_High,MUTcol,0), 'sortedLog2MUT_High is not properly sorted')
			sortedLog2MUT_Low = dataAnalyzer.getLowSortedLog2MUT()
			self.assertTrue( self.checkSorted(sortedLog2MUT_Low,MUTcol,1), 'sortedLog2MUT_Low is not properly sorted')

			topNumber = dataAnalyzer.getTopNumber()
			sortedLog2WT = dataAnalyzer.getSortedLog2WT()
			sortedLog2MUT = dataAnalyzer.getSortedLog2MUT()

			self.assertTrue( len(sortedLog2WT_High) == topNumber, 'sortedLog2WT_High is not correct length')
			self.assertTrue( len(sortedLog2WT_Low) == topNumber, 'sortedLog2WT_Low is not correct length')
			self.assertTrue( len(sortedLog2MUT_High) == topNumber, 'sortedLog2MUT_High is not correct length')
			self.assertTrue( len(sortedLog2MUT_Low) == topNumber, 'sortedLog2MUT_Low is not correct length')

			self.assertTrue( sortedLog2WT[-1] == sortedLog2WT_High[0], 'sortedLog2WT_High has the wrong first number')
			self.assertTrue( sortedLog2WT[-topNumber] == sortedLog2WT_High[topNumber-1], 'sortedLog2WT_Low has the wrong first number')
			self.assertTrue( sortedLog2MUT[-1] == sortedLog2MUT_High[0], 'sortedLog2MUT_High has the wrong first number')
			self.assertTrue( sortedLog2MUT[-topNumber] == sortedLog2MUT_High[topNumber-1], 'sortedLog2MUT_Low has the wrong first number')

	def test_UniqueValues(self):
		for dataAnalyzer in self.DA_List:
			getUniqueHighSortedLog2MUT = dataAnalyzer.getUniqueHighSortedLog2MUT()
			getHighSortedLog2WT = dataAnalyzer.getHighSortedLog2WT()
			for uniqueData in getUniqueHighSortedLog2MUT:
				for testData in getHighSortedLog2WT:
					self.assertTrue( uniqueData != testData, 'getUniqueHighSortedLog2MUT has non unique values')

			getHighSortedLog2MUT = dataAnalyzer.getHighSortedLog2MUT()
			for uniqueData in getUniqueHighSortedLog2MUT:
				check = False
				for testData in getHighSortedLog2MUT:
					if testData == uniqueData:
						check = True
				self.assertTrue( check, 'getUniqueHighSortedLog2MUT has values not belonging to getHighSortedLog2MUT')

			getUniqueLowSortedLog2MUT = dataAnalyzer.getUniqueLowSortedLog2MUT()
			getLowSortedLog2WT = dataAnalyzer.getLowSortedLog2WT()
			for uniqueData in getUniqueLowSortedLog2MUT:
				for testData in getLowSortedLog2WT:
					self.assertTrue( uniqueData != testData, 'getUniqueLowSortedLog2MUT has non unique values')

			getLowSortedLog2MUT = dataAnalyzer.getLowSortedLog2MUT()
			for uniqueData in getUniqueLowSortedLog2MUT:
				check = False
				for testData in getLowSortedLog2MUT:
					if testData == uniqueData:
						check = True
				self.assertTrue( check, 'getUniqueLowSortedLog2MUT has values not belonging to getLowSortedLog2MUT')

if __name__ == '__main__':
	unittest.main()
