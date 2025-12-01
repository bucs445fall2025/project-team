import time
from functools import wraps

def timer(func):
	"""
	Decorator that measures the execution time of a function and prints it
	Parameters:
		func (callable): The function to be timed
	Returns:
		callable: The decorated wrapper function
	"""
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		elapsed_time = end_time - start_time
		print(f"[{func.__name__}] Time Elapsed: **{elapsed_time:.2f} seconds**")
		return result
	return wrapper