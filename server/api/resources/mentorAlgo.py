import random as rdm
import datetime
from api.models import Mentor

def mentorAlgorithm(m):
	names = []
	weights = []
	n = datetime.datetime.now()
	for mentor in m:
		stat = getattr(mentor, 'mentorstat')
		type(mentor.last_appointment)
		print(mentor.last_appointment)
		x = float(int(mentor.finalmark) / 100) * float((n - mentor.last_appointment) / n) * float(stat.rating / 5)
		weights.append(x)
		names.append(mentor)
	return rdm.choices(names, weights, k=1)
