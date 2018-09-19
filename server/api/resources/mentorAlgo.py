import random as rdm
import datetime
from api.models import Mentor

def mentorAlgorithm(m):
	names = []
	weights = []
	n = datetime.datetime.now()
	for mentor in m:
		stat = getattr(mentor, 'mentorstat')
		last = mentor.last_appointment if type(mentor.last_appointment) != None else 0
		x = float(int(mentor.finalmark) / 100) * float((n - last) / n) * float(stat.rating / 5)
		weights.append(x)
		names.append(mentor)
	return rdm.choices(names, weights, k=1)
