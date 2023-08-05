import unittest
import numpy as np

import mmct

class TestGetMultinomObs(unittest.TestCase):

  def test_2d(self):
    prob = np.array([0.3,1.0])
    r = np.array([0.90,0.15,0.30,0.22,0.10])
    m = mmct.get_multinom(prob,r)
    self.assertEqual(2,m.size)
    self.assertEqual(3,m[0])
    self.assertEqual(2,m[1])

  def test_3d(self):
    prob = np.array([0.5,0.9,1.0])
    r = np.array([0.50,0.90,0.15,0.45,0.81,0.46,0.38,0.38])
    m = mmct.get_multinom(prob,r)
    self.assertEqual(3,m.size)
    self.assertEqual(5,m[0])
    self.assertEqual(2,m[1])
    self.assertEqual(1,m[2])

class TestTester(unittest.TestCase):

	def test_tester_run_trials(self):
		t = mmct.tester()
		t.n_trials = 10
		t.run_trials(np.ones(1))
		self.assertEqual(t.statistics.size,10)

	def test_tester_do_test_params(self):
		t = mmct.tester()
		t.n_trials = 200
		t.n_obs = 4
		t.statistics = np.zeros(80)

		x = np.array([3,4,5,6])
		p = t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		self.assertEqual(t.n_obs,18)
		self.assertEqual(t.statistics.size,200)

	def test_tester_do_test_no_rerun(self):
		t = mmct.tester()
		t.n_trials = 4

		x = np.array([3,4,5,6])

		t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		# Set artificial and impossible statistics. If run_trials is run, these
		# values will be overwritten, since they cannot occur mathematically
		t.statistics = np.array([10,12,14,16])

		y = np.array([6,5,4,3])

		t.do_test(y,np.array([0.2,0.25,0.3,0.25]))

		self.assertEqual(t.statistics.size,4)
		self.assertEqual(t.statistics[0],10)
		self.assertEqual(t.statistics[1],12)
		self.assertEqual(t.statistics[2],14)
		self.assertEqual(t.statistics[3],16)


	def test_tester_do_rerun_prob_changed(self):
		t = mmct.tester()
		t.n_trials = 4

		x = np.array([3,4,5,6])

		t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		# Set artificial and impossible statistics. If run_trials is run, these
		# values will be overwritten, since they cannot occur mathematically
		t.statistics = np.array([10,12,14,16])

		t.do_test(x,np.array([0.25,0.2,0.3,0.25]))

		self.assertEqual(t.statistics.size,4)
		self.assertNotEqual(t.statistics[0],10)
		self.assertNotEqual(t.statistics[1],12)
		self.assertNotEqual(t.statistics[2],14)
		self.assertNotEqual(t.statistics[3],16)

	def test_tester_do_rerun_n_obs_changed(self):
		t = mmct.tester()
		t.n_trials = 4

		x = np.array([3,4,5,6])

		t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		# Set artificial and impossible statistics. If run_trials is run, these
		# values will be overwritten, since they cannot occur mathematically
		t.statistics = np.array([10,12,14,16])
		x[0] = 4

		t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		self.assertEqual(t.statistics.size,4)
		self.assertNotEqual(t.statistics[0],10)
		self.assertNotEqual(t.statistics[1],12)
		self.assertNotEqual(t.statistics[2],14)
		self.assertNotEqual(t.statistics[3],16)

	def test_tester_do_rerun_n_trials_changed(self):
		t = mmct.tester()
		t.n_trials = 4

		x = np.array([3,4,5,6])

		t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		t.n_trials = 5

		t.do_test(x,np.array([0.2,0.25,0.3,0.25]))

		self.assertEqual(t.statistics.size,5)

	def test_tester_do_test_pvalue(self):
		t = mmct.tester()
		t.n_trials = 5
		t.n_obs = 8
		t.run_trials(np.array([0.05,0.6,0.1,0.25]))

		# null prob: [0.05,0.6,0.1,0.25]
		# Trial 0: [0,4,2,2]			LLR = -1.1032952365724916
		# Trial 1: [1,5,2,0]			LLR = -2.9529821682237408
		# Trial 2: [0,3,2,3]			LLR = -1.6389659003355966
		# Trial 3: [0,6,2,0]			LLR = -3.1714427716335686
		# Trial 4: [1,1,5,1]			LLR = -7.8174349521419151
		t.statistics = np.array([-1.1032952365724916,-2.9529821682237408,
			-1.6389659003355966,-3.1714427716335686,-7.8174349521419151])

		x = np.array([1,3,1,3])	#	LLR = -0.9458187197756513
		p = t.do_test(x,np.array([0.05,0.6,0.1,0.25]))

		self.assertEqual(p,1.0)

		x = np.array([8,0,0,0]) # LLR = -23.965858188431927
		p = t.do_test(x,np.array([0.05,0.6,0.1,0.25]))

		self.assertEqual(p,0.0)

		x = np.array([1,2,2,3])	#	LLR = -2.2143300452391584
		p = t.do_test(x,np.array([0.05,0.6,0.1,0.25]))

		self.assertEqual(p,0.6)


	def test_tester_do_test_error_x_probs_not_same_dim(self):
		t = mmct.tester()
		x = np.array([3,4,5])
		p = np.array([0.3,0.6,0.05,0.05])
		self.assertRaises(ValueError, t.do_test,x,p)
