import numpy

class matrix():
	def white_noise(m_sizes:tuple, g_type:str):
		if g_type=="float":
			result=numpy.random.sample(m_sizes)
		elif g_type=="int":
			result=numpy.random.randint(0, 2, m_sizes)
		else:
			return None, "wrong_type"
		return result, "success"
