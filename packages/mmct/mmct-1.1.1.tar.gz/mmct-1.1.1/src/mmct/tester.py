import numpy as np
import random
from multiprocessing import Pool

from . import stat

# Generate a multinomially distributed set of observations

def get_multinom(c_prob,rs):

  res = np.zeros(c_prob.size)

  for r in rs:
    # TODO: binary search since c_prob should be increasing
    i = 0
    while r >= c_prob[i]:
      i += 1
    res[i] += 1

  return res




# Main class used for performing multinomial tests

class tester:

	n_samples = 1000 # The number of Monte Carlo samples to generate
	statistics = np.zeros(1) # Test statistics of random samples

	test_statistic = 'LLR' # The test statistic to use (LLR or Prob)

	# The test statistics can be fixed by setting fix to True. This prevents
	# rerunning the Monte Carlo sampling when running a new test. This can
	# be useful when testing or to save time (bias danger!)
	fix = False


	# Internal state objects
	__prob = np.ones(1)
	__c_prob = np.ones(1)
	__n_obs = 0


	def generate_sample_stat(self, index):

		# The index argument is irrelevant but necessary to make Pool.map work

		# Each distribution need n observations
		rs = np.zeros(self.__n_obs)
		# Generate n random numbers in [0,1)
		for j in range(0,self.__n_obs):
			rs[j] = random.random() # Thread safe

		# Generate a multinomial draw from the probabilities in ps (using cps)
		m = get_multinom(self.__c_prob,rs)

		# Calculate test statistic
		if self.test_statistic == 'Prob':
			return stat.multinomialProb(m,self.__prob)
		else:
			return stat.multinomialLLR(m,self.__prob)


	def mc_runs(self):
		# Reset statistics array
		self.statistics = np.zeros(self.n_samples)

		# Run Monte Carlo simulation:
		for i in range(0,self.n_samples):
			self.statistics[i] = self.generate_sample_stat(i)


	def do_test(self, x, probs):

		if x.size != probs.size:
			raise ValueError('Input arrays must have the same number of elements')

		# Run samples if not fixed
		if not self.fix:

			self.__n_obs = np.sum(x) # Total number of observations in x
			self.__prob = probs.copy()

			# First, generate a cumulative sum of the probabilities in ps
			self.__c_prob = np.zeros(probs.size)
			self.__c_prob[0] = probs[0]
			for i in range(1,probs.size):
				self.__c_prob[i] = self.__c_prob[i-1] + probs[i]

			self.mc_runs()



		# Calculate statistic of x
		if self.test_statistic == 'Prob':
			x_stat = stat.multinomialProb(x, probs)
		else:
			x_stat = stat.multinomialLLR(x, probs)

		# Count number of trials with statistic smaller than x
		n_smaller = 0
		for s in self.statistics:
			if s <= x_stat:
				n_smaller += 1
		return n_smaller/self.statistics.size



# Derived class from tester that uses multithreading to speed up the monte carlo
# sampling

class mt_tester(tester):

	# Number of threads to use. If None, the system default is used
	# (typically the number of logical processors)
	threads = None

	def mc_runs(self):

		with Pool(processes=self.threads) as pool:
			res = pool.map(self.generate_sample_stat, range(0,self.n_samples))
		self.statistics = np.array(res)
