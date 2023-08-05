import numpy as np

# Normalises a numpy array to L1 norm 1 (sum of absolute value of elements equal
# to 1).
# In case of a norm of zero of the input vector is found, a zero-vector of the
# same dimension is returned

def normL1(arr):
  norm = np.linalg.norm(arr,ord=1)
  if norm == 0.0:
    return np.zeros(arr.shape)

  return arr/norm
