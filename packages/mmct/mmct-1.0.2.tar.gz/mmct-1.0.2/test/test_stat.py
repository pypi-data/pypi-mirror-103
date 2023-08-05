
import unittest
import numpy as np

import mmct.stat as stat

class TestMultinomialLLR(unittest.TestCase):

  def test_2_elems_as_expected(self):
    x = np.array([10,10])
    ref = np.array([1,1])
    self.assertEqual(0.0,stat.multinomialLLR(x,ref))

  def test_2_elems(self):
    x = np.array([5,5])
    ref = np.array([1,3])
    self.assertAlmostEqual(-1.4384103622589046,stat.multinomialLLR(x,ref))

  def test_2_elems_2(self):
    x = np.array([1,9])
    ref = np.array([1,3])
    self.assertAlmostEqual(-0.7246032792714366,stat.multinomialLLR(x,ref))

  def test_5_elems(self):
    x = np.array([14,26,29,59,38])
    ref = np.array([10,6,4,1,2])
    self.assertAlmostEqual(-124.6498750742718601,stat.multinomialLLR(x,ref))

  def test_fails_different_number_of_elems(self):
    x = np.array([5,5])
    ref = np.array([1,2,3])
    self.assertRaises(ValueError, stat.multinomialLLR, x, ref)
