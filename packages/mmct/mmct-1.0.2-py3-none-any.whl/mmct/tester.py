import numpy as np
import random

from . import stat

# Generate a random multinomially distributed set of observations
# This function will generate a numpy-array, from a multinomial distribution
# given a set of probabilities and a set of random numbers.
# The input probability array c_prob must be cumulatively added.
# I.e if we want to simulate a dice throw, c_prob should be
# 	c_prob = np.array([1/6, 2/6, 3/6, 4/6, 5/6, 6/6])
# rs is the input randomness, and the total number of elements in rs dictates
# the number of trials in the multinomial variable. All elements in rs should be
# in [0,1). I.e. if we want to simulate throwing the dice from previously 7
# times, then we could use
# 	rs = np.array([0.20, 0.07, 0.23, 0.91, 0.14, 0.58, 0.73])
# Each element r in rs leads to an observation in the first bin
# where r<c_prob[i]
# For the example used here, this would mean the resulting array would be:
# 	[2,2,0,1,1,1]

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
# To perform a multinomial test, create an instance of this class:
# 	t = mmct.tester()
# By default the tester will perform 1000 monte carlo simulations to calculate
# a p-value. This can be changed by setting the member variable n_trials:
# 	t.n_trials = 100000
# To perform a multinomial test of an array X = [x1,x2,...,xn], where xi is the
# number of observations in bin i, under a null-hypothesis probability
# p = [p1,p2,...,pn], use the function
# 	p_value = t.do_test(X,p).
# The p-value will be returned. Remember that X and p must be numpy arrays.

class tester:

	n_obs = 1
	n_trials = 1000
	statistics = np.zeros(1)

	__old_ps = None

	def run_trials(self, probs):
		# First, generate a cumulative sum of the probabilities in ps
		cps = np.zeros(probs.size)
		cps[0] = probs[0]
		for i in range(1,probs.size):
			cps[i] = cps[i-1] + probs[i]

		# Generate n_trials samples from the underlying distribution of ps
		self.statistics = np.zeros(self.n_trials)
		for i in range(0,self.n_trials):

			# Each distribution need n_obs observations
			rs = np.zeros(self.n_obs)
			# Generate n_obs random numbers in [0,1)
			for j in range(0,self.n_obs):
				rs[j] = random.random()

			# Generate a multinomial draw from the probabilities in ps (using cps)
			m = get_multinom(cps,rs)

			# Calculate test statistic
			self.statistics[i] = stat.multinomialLLR(m,probs)

		# Set __old_ps, so we know the state of the distribution for later
		self.__old_ps = probs.copy()


	def do_test(self, x, probs):

		if x.size != probs.size:
			raise ValueError('Input arrays must have the same number of elements')

		n = np.sum(x)

		# Check if a rerun of trials is necessary
		if not np.array_equal(self.__old_ps,probs) or n!=self.n_obs or self.n_trials!=self.statistics.size:

			# Set correct number of observations
			self.n_obs = n

			# Run trials
			self.run_trials(probs)

		# Calculate statistic of x
		x_stat = stat.multinomialLLR(x, probs)

		# Count number of trials with statistic smaller than x
		n_smaller = 0
		for s in self.statistics:
			if s <= x_stat:
				n_smaller += 1
		return n_smaller/self.statistics.size
