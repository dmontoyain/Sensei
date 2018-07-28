from models import db

class User(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    id_user42 = db.Column(db.Integer, nullable=False)
    login = db.Column(db.String(45), nullable=False)

    #   relationship with 'Mentors' table, Mentor Model Class
    mentors = db.relationship('Mentor', backref='user', lazy=True)

    #   relationship with 'Appointments' table, Appointment Model Class
    #appointments = db.relationship('Appointment', backref='user', lazy=True)

    @property
    def serialize(self):
    	return {'id': self.id,
    			'id_user42': self.id_user42,
    			'login': self.login }
    