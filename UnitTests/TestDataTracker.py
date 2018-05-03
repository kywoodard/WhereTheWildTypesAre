from SortingScript import DataAnalyzer
from SortingScript import DataTracker
import unittest

#TODO: Incorporate the data from the excel file output

class TestDataTracker(unittest.TestCase):
	def setUp(self):
		filePathList = [
		'/Users/kywoodard/Documents/MarMar_SideProject/WTvsMut_15.csv',
		'/Users/kywoodard/Documents/MarMar_SideProject/WTvsMut_2.csv',
		'/Users/kywoodard/Documents/MarMar_SideProject/WTvsMut_0.csv']
		self.numDAs = len(filePathList)
		self.DA_List = [DataAnalyzer(filePathList[i]) for i in range(self.numDAs)]
		self.DT = DataTracker(self.DA_List)

	#TODO: Figure out why the data tracker is reporting datasets of only size 1
	def test_dataSize(self):
		trackedDataHigh = self.DT.getTrackedDataHigh()
		trackedDataLow = self.DT.getTrackedDataLow()
		countThree = 0
		countTwo = 0
		countOne = 0
		for dataSet in trackedDataHigh:
			if len(dataSet)==1:
				countOne += 1
				# print 1, dataSet[0][0]
			if len(dataSet)==2:
				countTwo += 1
				# print 2, dataSet[0][0]
			if len(dataSet)==3:
				countThree += 1
				# print 3, dataSet[0][0]
			# self.assertEqual(len(dataSet),self.numDAs,'Data set is not same length as the file list provided')
			# for datapoint in dataSet:
			# 	print len(datapoint)
			# 	self.assertEqual(len(datapoint),9,'Data point is not same length as expected from template')
		print "Data Tracked High:"
		print "CountOne: ", countOne
		print "CountTwo: ", countTwo
		print "CountThree: ", countThree

		countThree = 0
		countTwo = 0
		countOne = 0
		for dataSet in trackedDataLow:
			print dataSet[0][0]
			if len(dataSet)==1:
				countOne += 1
				# print 1, dataSet[0][0]
			if len(dataSet)==2:
				countTwo += 1
				# print 2, dataSet[0][0]
			if len(dataSet)==3:
				countThree += 1
		print "Data Tracked Low:"
		print "CountOne: ", countOne
		print "CountTwo: ", countTwo
		print "CountThree: ", countThree


	def test_checkTrackedDataUniquec(self):
		trackedDataHigh = self.DT.getTrackedDataHigh()
		trackedDataLow = self.DT.getTrackedDataLow()
		for i in range(len(trackedDataHigh)):
			for j in range(i+1,len(trackedDataHigh)):
				self.assertTrue(trackedDataHigh[i]!=trackedDataHigh[j],
							'High tracked values have nonunique items')
		for i in range(len(trackedDataHigh)):
			for j in range(i+1,len(trackedDataHigh)):
				self.assertTrue(trackedDataLow[i]!=trackedDataLow[j],
							'Low tracked values have nonunique items')

	# def test_dataExistsInDAList(self):
	# 	trackedDataHigh = self.DT.getTrackedDataHigh()
	# 	trackedDataLow = self.DT.getTrackedDataLow()
	# 	for k in range(self.numDAs):
	# 		DA = self.DA_List[k]
	# 		uniqueHighSortedLog2MUT = DA.getUniqueHighSortedLog2MUT()
	# 		for i in range(len(uniqueHighSortedLog2MUT)):
	# 			foundFlag = False
	# 			print 1,uniqueHighSortedLog2MUT[i][0]
	# 			for j in range(len(trackedDataHigh)):
	# 				print j
	# 				print k
	# 				print i
	# 				print 2,len(trackedDataHigh[2])
	# 				if uniqueHighSortedLog2MUT[i]==trackedDataHigh[j][k]:
	# 					foundFlag = True
	# 					break
	# 			self.assertTrue(foundFlag,
	# 						'Could not find data in the high tracker list')
		# for k in range(self.numDAs):
		# 	DA = self.DA_List[k]
		# 	uniqueHighSortedLog2MUT = DA.getUniqueHighSortedLog2MUT()
		# 	for i in range(len(uniqueHighSortedLog2MUT)):
		# 		foundFlag = False
		# 		for j in range(len(trackedDataHigh)):
		# 			if trackedDataHigh[i]!=trackedDataHigh[j]:
		# 				foundFlag = True
		# 		self.assertTrue(foundFlag,
		# 					'Could not find data in the high tracker list')

		# 		uniqueLowSortedLog2MUT = DA.getUniqueLowSortedLog2MUT()

if __name__ == '__main__':
	unittest.main()