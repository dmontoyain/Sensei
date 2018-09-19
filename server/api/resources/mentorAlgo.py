import random as rdm
import datetime
from api.models import Mentor

def mentorAlgorithm(m):
	names = []
	weights = []
	n = datetime.datetime.now().timestamp()
	for mentor in m:
		stat = getattr(mentor, 'mentorstat')
		rate = 5 if not stat else stat.rating
		last = mentor.last_appointment.timestamp() if mentor.last_appointment is not None else 0
		x = float(int(mentor.finalmark) / 100) * float((n - last) / n)
		x *= float(rate / 5) if rate else 1
		weights.append(x)
		names.append(mentor)
	name = rdm.choices(names, weights, k=1)
	return name[0]
