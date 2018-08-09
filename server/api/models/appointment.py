from api.app import db, ma
from datetime import datetime, timedelta

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    id_mentor = db.Column(db.Integer, db.ForeignKey('mentors.id'), nullable=False) 
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime)
    feedback = db.Column(db.Text)

    def __init__(self, id_mentor, id_user, feedback=""):
        self.id_mentor = id_mentor
        self.id_user = id_user
        self.feedback = feedback
    
    @classmethod
    def createAppointment(cls, mentorId, userId):
        data = {"id_mentor": mentorId, "id_user": userId}
        newappointment, error = appointment_schema.load(data)
        if error:
            return None, error
        #creates an appointment 15 minutes ahead from creation
        newappointment.start_time = datetime.now() + timedelta(minutes=15)
        db.session.add(newappointment)
        db.session.commit()
        return appointment_schema.dump(newappointment).data, None

    @classmethod
    def querybyId(cls, appointmentId):
        query = cls.query.filter_by(id=appointmentId).first()
        if query is None:
            return None, "No appointment with id {} was found".format(appointmentId)
        return appointment_schema.dump(query).data, None
    
    @classmethod
    def queryManyAsUser(cls, userId):
        query = cls.query.filter(cls.id_user==userId).all()
        if query is None:
            return None, "No appointments requested by user {}".format(userId)
        return appointments_schema.dump(query).data, None

    @classmethod
    def queryManyAsMentor(cls, userId):
        from api.models import Mentor
        query = cls.query.join(Mentor, cls.id_mentor==Mentor.id).filter(Mentor.id_user42 == userId).all()
        print(query)
        if query is None:
            return None, "No appointments to mentor for user {}".format(userId)
        return appointments_schema.dump(query).data, None

    @classmethod
    def queryManyPendingAsUser(cls, userId):
        query = cls.query.filter(cls.id_user==userId, cls.feedback is None).all()
        if query is None:
            return None, "No pending appointments requested by user {}".format(userId)
        return appointments_schema.dump(query).data, None
    
    @classmethod
    def queryManyPendingAsMentor(cls, userId):
        from api.models import Mentor
        query = cls.query.join(Mentor, cls.id_mentor==Mentor.id).filter(cls.feedback is None).filter(Mentor.id_user42 == userId).all()
        print(query)
        if query is None:
            return None, "No pending appointments to mentor for user {}".format(userId)
        return appointments_schema.dump(query).data, None

class AppointmentSchema(ma.ModelSchema):
    class Meta:
        model = Appointment
        include_fk = True

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)