import random as rdm
import datetime
from api.models import Mentor

def mentorAlgorithm(m):
	names = []
	weights = []
	n = datetime.datetime.now().timestamp()
	for mentor in m:
		stat = getattr(mentor, 'mentorstat')
		print(stat.rating)
		if mentor.last_appointment is not None:
			last = mentor.last_appointment.timestamp()
		else:
			last = 0
		x = float(int(mentor.finalmark) / 100) * float((n - last) / n) * float(stat.rating / 5)
		weights.append(x)
		names.append(mentor)
	return rdm.choices(names, weights, k=1)
