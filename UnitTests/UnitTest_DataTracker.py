import unittest
import sys
sys.path.insert(0, '/Users/kywoodard/Documents/WhereTheWildTypesAre/')
from SortingScript import DataAnalyzer
from SortingScript import DataTracker


class TestDataTracker(unittest.TestCase):
	def setUp(self):
		filePathList = [
		'/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_0.csv',
		'/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_15.csv',
		'/Users/kywoodard/Documents/WhereTheWildTypesAre/Data/WTvsMut_2.csv',
		]
		self.timeList = [0.0, 15.0, 120.0]
		self.numDAs = len(filePathList)
		self.DA_List = [DataAnalyzer(filePathList[i],self.timeList[i]) for i in range(len(filePathList))]
		self.DT = DataTracker(self.DA_List)

	def test_NoEmptyDatasets(self):
		#Get data and check that it is not empty
		self.assertTrue(self.DT.getTrackedDataHigh(),
						'trackedDataHigh is empty')
		self.assertTrue(self.DT.getTrackedDataLow(),
						'trackedDataLow is empty')
		self.assertTrue(self.DT.getPersistentTrackedDataHigh(),
						'persistentTrackedDataHigh is empty')
		self.assertTrue(self.DT.getPersistentTrackedDataLow(),
						'persistentTrackedDataLow is empty')

	def test_TrackedDataUnique(self):
		trackedDataHigh = self.DT.getTrackedDataHigh()
		for i in range(len(trackedDataHigh)):
			#Check for empty datasets
			self.assertTrue(trackedDataHigh[i],'One of the trackedDataHigh datasets is empty')

			#Check for too many datapoints in one set
			self.assertTrue(len(trackedDataHigh[i])<=self.numDAs,'One of the datasets in trackedDataHigh is longer than the number of analyzers')

			#Verify that the time value exists in the list
			dataSetName = trackedDataHigh[i][0][0]
			for data in trackedDataHigh[i]:
				timeCheck = False
				for timeVal in self.timeList:
					if data[9] == timeVal:
						timeCheck = True
						break
				self.assertTrue(timeCheck,'Appended time value does not exist in the default timeList for trackedDataHigh')

				#Check that the data name is consistent across the dataset
				self.assertEqual(dataSetName,data[0],'Data names did not match within one data set')

			#Check for nonunique data names
			for j in range(i+1,len(trackedDataHigh)):
				self.assertTrue(trackedDataHigh[i][0][0]!=
								trackedDataHigh[j][0][0],
								'High tracked values have nonunique items')

		trackedDataLow = self.DT.getTrackedDataLow()
		for i in range(len(trackedDataLow)):
			#Check for empty datasets
			self.assertTrue(trackedDataLow[i],'One of the trackedDataLow datasets is empty')

			#Check for too many datapoints in one set
			self.assertTrue(len(trackedDataLow[i])<=self.numDAs,'One of the datasets in trackedDataLow is longer than the number of analyzers')

			#Verify that the time value exists in the list
			dataSetName = trackedDataLow[i][0][0]
			for data in trackedDataLow[i]:
				timeCheck = False
				for timeVal in self.timeList:
					if data[9] == timeVal:
						timeCheck = True
						break
				self.assertTrue(timeCheck,'Appended time value does not exist in the default timeList for trackedDataLow')

				#Check that the data name is consistent across the dataset
				self.assertEqual(dataSetName,data[0],'Data names did not match within one data set')

			#Check for nonunique data names
			for j in range(i+1,len(trackedDataLow)):
				self.assertTrue(trackedDataLow[i][0][0]!=
								trackedDataLow[j][0][0],
								'Low tracked values have nonunique items')

	def test_PersistentData(self):
		#Check that the high persistent data has the same size as the number input datsets
		for dataSet in self.DT.getPersistentTrackedDataHigh():
			self.assertEqual(len(dataSet),self.numDAs,'Data in  persistentTrackedData_High set is not same length as the file list provided')
			DA_index = 0
			for data in dataSet:
				#TODO: Evaluate if this needs to not be hardcoded
				self.assertEqual(data[9],self.timeList[DA_index],'Data in  persistentTrackedData_High set is not same length as the file list provided')
				DA_index+=1

		#Check that the low persistent data has the same size as the number input datsets
		for dataSet in self.DT.getPersistentTrackedDataLow():
			self.assertEqual(len(dataSet),self.numDAs,'Data in persistentTrackedData_Low is not same length as the file list provided')
			DA_index = 0
			for data in dataSet:
				#TODO: Evaluate if this needs to not be hardcoded
				self.assertEqual(data[9],self.timeList[DA_index],'Data in  persistentTrackedData_Low set is not same length as the file list provided')
				DA_index+=1

if __name__ == '__main__':
	print "DataTracker Unit Test:"
	unittest.main()