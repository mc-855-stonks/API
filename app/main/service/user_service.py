from app.main import db
from app.main.model.user import User

from app.main.helper import utils
from app.main.helper.utils import create_response
from app.main.helper.validation_helper import valid_email

def valid_user(data):
    if not valid_email(data['email']):
        return False
    try:
        return bool(utils.get_investor_profile_id(data['investor_profile']))
    except AssertionError:
        return False

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        if not valid_user(data):
            return create_response('fail', 'Invalid data.', 400)

        new_user = User(
            email=data['email'],
            name=data['name'],
            # convert investor profile label into id
            investor_profile=utils.get_investor_profile_id(data['investor_profile']),
            password=data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return generate_token(new_user)
    else:
        return create_response('fail', 'User already exists. Please Log in.', 409)

def update_user(data):
    user = User.query.get(data['id'])
    if user:
        if data.get('investor_profile', None):
            try:
                user.investor_profile = utils.get_investor_profile_id(data['investor_profile'])
            except AssertionError:
                return create_response('fail', 'Invalid investor profile.', 400)

        if data.get('name', None):
            user.name = data['name']

        db.session.commit()

        return create_response('success', 'User successfully updated.', 200)
    else:
        return create_response('fail', 'User not found.', 404)


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return create_response('fail', 'User not found.', 404)

    # convert investor profile id into the correct label
    user.investor_profile = utils.get_investor_profile(user.investor_profile)
    return user


def generate_token(user: User):
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        print(e)
        return create_response('fail', 'Some error occurred. Please try again.', 401)

