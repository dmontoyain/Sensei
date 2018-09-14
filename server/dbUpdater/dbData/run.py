import os
import requests
import datetime
from sqlalchemy.orm import sessionmaker
from dbUpdater.EnvSettings import configure
from rq42 import Api42

api42_url = os.environ.get("API42_URL", default=None)
projectMinScore = os.environ.get("MIN_PROJECT_SCORE")
automaticDeactivationTime = datetime.timedelta(days=900)

if not api42_url:
    raise ValueError('42 api url configuration not found in environment')

if not projectMinScore:
    raise ValueError('Missing minimum project score configuration')

def updateUsers(env):
    db = configure(env)

    from models import base
    from models import User, Mentor, Appointment, Project

    Session = sessionmaker(db)
    session = Session()

    #   Updating data relevant for Sensei application proper functionality like:
    #   1.  User projects completed / resubmmitted
    #   2.  User inactivity
    try:
        users = session.query(User)
        print("starting...")
        for user in users:
            #if (datetime.datetime.utcnow() - user.last_seen) > automaticDeactivationTime:
            #    user.active = False
            #if user.active == True:
            id42user = getattr(user, 'id_user42')
            userProjects = Api42.userProjects(id42user)
            if not userProjects:
                continue
            for p in userProjects:
                project = session.query(Project).filter(Project.id_project42==p['id_project42']).first()
                if project:
                    mentor = session.query(Mentor).filter(Mentor.id_user42==id42user, Mentor.id_project42==p['id_project42']).first()
                    if not mentor:
                        mentor = Mentor(id_project42=p['id_project42'], id_user42=id42user, finalmark=p['finalmark'])
                        session.add(mentor)
                    print(type(projectMinScore))
                    if mentor.finalmark >= int(projectMinScore):
                        mentor.abletomentor = True
        session.commit()
    except Exception as inst:
        print(inst.args)
        session.rollback()
    finally:
        session.close()
  