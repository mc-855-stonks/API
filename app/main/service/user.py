from app.main.model.user import User
from app.main import db

def save_new_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(username):
    return User.query.filter_by(username=username).first()


