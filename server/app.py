from flask import Flask, jsonify
from marshmallow import pprint
import database

app = Flask(__name__)

db = database.init_db(app)

@app.route('/users')
#users.getOnlineUsers();
def index():
    from models.user import User
    userQuery = User.query.all()
    print([{'login': user.login} for user in userQuery])
    return str([{'login': user.login } for user in userQuery])

@
if __name__ == '__main__':
    app.run(debug=True)
