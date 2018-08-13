import random as rdm
from api.models import Mentor

def mentorAlgorithm(m):
	names = []
	weights = []
	for mentor in m:
		x = float(int(mentor['finalmark']) / 100) * float((1 / (1 + mentor['weeklyappointments'])))
		y = mentor['id_user42']
		weights.append(x)
		names.append(y)
	name = rdm.choices(names, weights, k=1)
	return [ret for ret in m if name[0] == ret['id_user42']][0]