
import unittest
import numpy as np

import mmct.stat as stat

class TestMultinomialLLR(unittest.TestCase):

  def test_2_elems_as_expected(self):
    x = np.array([10,10])
    ref = np.array([0.5,0.5])
    self.assertEqual(0.0,stat.multinomialLLR(x,ref))

  def test_2_elems(self):
    x = np.array([5,5])
    ref = np.array([0.25,0.75])
    self.assertAlmostEqual(-1.4384103622589046,stat.multinomialLLR(x,ref))

  def test_2_elems_2(self):
    x = np.array([1,9])
    ref = np.array([0.25,0.75])
    self.assertAlmostEqual(-0.7246032792714366,stat.multinomialLLR(x,ref))

  def test_5_elems(self):
    x = np.array([14,26,29,59,38])
    ref = np.array([10/23,6/23,4/23,1/23,2/23])
    self.assertAlmostEqual(-124.6498750742718601,stat.multinomialLLR(x,ref))

  def test_fails_different_number_of_elems(self):
    x = np.array([5,5])
    ref = np.array([1/6,2/6,3/6])
    self.assertRaises(ValueError, stat.multinomialLLR, x, ref)



class TestMultinomialProb(unittest.TestCase):

  def test_2_elems(self):
    x = np.array([5,5])
    ref = np.array([0.25,0.75])
    self.assertAlmostEqual(0.058399200439453125,stat.multinomialProb(x,ref))

  def test_2_elems_2(self):
    x = np.array([1,9])
    ref = np.array([0.25,0.75])
    self.assertAlmostEqual(0.1877117156982421875,stat.multinomialProb(x,ref))

  def test_5_elems(self):
    x = np.array([10,4,4,2,3])
    ref = np.array([10/23,6/23,4/23,1/23,2/23])
    self.assertAlmostEqual(0.0013101541339934,stat.multinomialProb(x,ref))

  def test_fails_different_number_of_elems(self):
    x = np.array([5,5])
    ref = np.array([1/6,2/6,3/6])
    self.assertRaises(ValueError, stat.multinomialProb, x, ref)
