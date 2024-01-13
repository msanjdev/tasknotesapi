from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasklists.db'
db = SQLAlchemy(app)

# Tasklist model
class Tasklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), unique=True, nullable=False)
    tasklist = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return "id " + str(self.id) + " user " + self.user + " tasklist " + self.tasklist

# Create the database tables
with app.app_context():
    db.create_all()

# Helper function to get the user ID based on IP address
def get_user_id():
    return request.remote_addr

# Endpoint to create a new tasklist
@app.route('/tasklist', methods=['POST'])
def create_tasklist():
    user_id = get_user_id()
    data = request.get_json()

    if not Tasklist.query.filter_by(user=user_id).first():
        new_tasklist = Tasklist(user=user_id, tasklist=data['tasklist'])
        db.session.add(new_tasklist)
        db.session.commit()
        return jsonify({'message': 'Tasklist created successfully'}), 201
    else:
        return jsonify({'error': 'User already has a tasklist'}), 400

# Endpoint to get a user's tasklist
@app.route('/tasklist', methods=['GET'])
def get_tasklist():
    user_id = get_user_id()
    tasklist_entry = Tasklist.query.filter_by(user=user_id).first()

    print("the tasklist for " + user_id + " is " + str(tasklist_entry))

    if tasklist_entry:
        return jsonify({'user': tasklist_entry.user, 'tasklist': tasklist_entry.tasklist})
    else:
        return jsonify({'error': 'User does not have a tasklist'}), 404

# Endpoint to update a user's tasklist
@app.route('/tasklist', methods=['PUT'])
def update_tasklist():
    user_id = get_user_id()
    data = request.get_json()
    tasklist_entry = Tasklist.query.filter_by(user=user_id).first()

    if tasklist_entry:
        tasklist_entry.tasklist = data['tasklist']
        db.session.commit()
        return jsonify({'message': 'Tasklist updated successfully'})
    else:
        return jsonify({'error': 'User does not have a tasklist'}), 404

# Endpoint to delete a user's tasklist
@app.route('/tasklist', methods=['DELETE'])
def delete_tasklist():
    user_id = get_user_id()
    tasklist_entry = Tasklist.query.filter_by(user=user_id).first()

    if tasklist_entry:
        db.session.delete(tasklist_entry)
        db.session.commit()
        return jsonify({'message': 'Tasklist deleted successfully'})
    else:
        return jsonify({'error': 'User does not have a tasklist'}), 404

if __name__ == '__main__':
    app.run(debug=True)
