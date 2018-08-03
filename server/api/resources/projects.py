from flask_restful import Resource
from api.models import Project, ProjectSchema
from rq42 import Api42
import json
from api.app import db

#   api/projects
class apiProjects(Resource):
    def get(self):
        projects = Project.query.all()
        return [project for project in projects], 200

    def post(self):
        # add filter to find if project already exists
        data = Api42.allProjects()
        if data is None:
            return {"message": "all projects was empty"}, 400

        for d in data:
            newProject = Project(d['project_id42'], d['name'], d['slug'], d['tier'])
            db.session.add(newProject)
        db.session.commit()
        # data = json.loads(json.dumps(data))
        # project_schema = ProjectSchema()
        # print(data)
        # output, err = project_schema.dump(data)
        # if err:
        #     return err, 422
#        for proj in allProjects:

#        Project.commit()
        return {"status": "success"}, 201