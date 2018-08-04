#The function for choosing a randomized mentor.
#Ooh, python3.6+'s Random module has something called choices
#If a list is passed in as the first parameter, e.g. the list of eligible
#mentors, the second parameter is a list of weights per each parameter.
#If the json object or whatever has the entirety of the proper mentors for
#a project, I can grab properties from that to create an in-order list of
#weights perhaps?

import json
import random as rdm

def     c(score, appt):
    return (score / 100) * (1 / (1 + appt))

def     names(m):
    return [d['name'] for d in m['mentors']]

def     wei(m):
    w = []
    for d in m['mentors']:
        x = c(float(d['grade']), float(d['appts']))
        #The line after this is just for testing purposes to see if
        #weights were properly calculated
        print (str(x) + "-" + d['name'])
        w.append(x)
    return w

#This list is made under the assumption that we know which project the student
#needs a mentor for.  In this case, ls.  Appointment numbers are random.
json_input = '{"mentors": [{"name": "jmeier", "grade": "113", "appts" : 1},\
{"name": "dmontoya", "grade": "104", "appts" : 1},\
{"name": "bpierce", "grade": "102", "appts" : 0},\
{"name": "lkaba", "grade": "111", "appts" : 1},\
{"name": "nwang", "grade": "115", "appts" : 2},\
{"name": "ihodge", "grade": "103", "appts" : 0}]}'

m = json.loads(json_input)

n = names(m)
w = wei(m)

i = 0

#Choices chooses from a list with assigned weights for each item
#Running the choice ten times after the list has been created
print(rdm.choices(n, w, k=100))

