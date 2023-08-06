import math
import numpy as np
from scipy.stats import multinomial

# Computes the log-likelihood ratio for a set of multinomially distributed
# observations x, compared to a reference (expectation under
# the null-hypothesis). The total number of observations in the two arrays
# does not need to be the same, although the order of the elements in the
# arrays matter.
# Both arrays must be numpy arrays.

def multinomialLLR(x, ref):
  if x.size != ref.size:
    raise ValueError('Input arrays must have the same number of elements')

  n = x.sum()

  llr = 0.0
  for i in range(0,x.size):
    if (x[i] != 0):
      llr += x[i] * math.log(n*ref[i]/x[i])

  return llr


def multinomialProb(x, ref):
	n_obs = np.sum(x)
	return multinomial.pmf(x, n=n_obs, p=ref)
