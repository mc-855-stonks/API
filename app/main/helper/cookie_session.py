SESSION_MAX_AGE = 86400 # 24 horas
SESSION_COOKIE_NAME = "STONKS_SESSION"

def build_auth_session_cookie(session_id):
    return '{}={}; Max-Age={}'.format(SESSION_COOKIE_NAME, session_id, SESSION_MAX_AGE)

def build_logout_session_cookie():
    return '{}={}; Max-Age=0'.format(SESSION_COOKIE_NAME, '')