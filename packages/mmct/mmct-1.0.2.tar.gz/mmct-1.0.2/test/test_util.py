
import unittest
import numpy as np

import mmct.util as util

class TestNormL1(unittest.TestCase):

	def test_1d_nonzero(self):
		arr = np.array([2])
		narr = util.normL1(arr)
		self.assertEqual(1,narr.size)
		self.assertEqual(1.0,narr[0])

	def test_2d_nonzero(self):
		arr = np.array([0.5,1.5])
		narr = util.normL1(arr)
		self.assertEqual(2,narr.size)
		self.assertEqual(0.25,narr[0])
		self.assertEqual(0.75,narr[1])

	def test_1d_zero(self):
		arr = np.array([0])
		narr = util.normL1(arr)
		self.assertEqual(1,narr.size)
		self.assertEqual(0.0,narr[0])

	def test_2d_zero(self):
		arr = np.array([0.0,0.0])
		narr = util.normL1(arr)
		self.assertEqual(2,narr.size)
		self.assertEqual(0.0,narr[0])
		self.assertEqual(0.0,narr[1])
