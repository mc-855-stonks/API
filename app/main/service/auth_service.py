from app.main import db

from app.main.model.blocked_tokens import BlockedToken
from app.main.helper.utils import create_response
from app.main.helper.cookie_session import build_auth_session_cookie, build_logout_session_cookie
from app.main.model.user import User

def save_token(token: str):
    blocked_token = BlockedToken(token=token)
    try:
        # insert the token
        db.session.add(blocked_token)
        db.session.commit()
        return create_response('success', 'Successfully logged out.', 200)

    except Exception as e:
        return create_response('fail', e, 500)

class Auth:
    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'Authorization': auth_token.decode()
                    }
                    return response_object, 200, {'Set-Cookie': build_auth_session_cookie(auth_token.decode())}
            else:
                return create_response('fail', 'email or password does not match.', 401)

        except Exception as e:
            print(e)
            return create_response('fail', 'Unexpected Error. Try again.', 500)

    @staticmethod
    def logout_user(auth_token):
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blocked
                return save_token(token=auth_token)[0], {'Set-Cookie': build_logout_session_cookie()}
            else:
                return create_response('fail', resp, 401)
        else:
            return create_response('fail', 'Provide a valid auth token.', 401)

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                    }
                }
                return response_object, 200
            return create_response('fail', resp, 401)
        else:
            return create_response('fail', 'Provide a valid auth token.', 401)
