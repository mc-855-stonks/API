

def get_investor_profile(_id):
    """
    This method returns the  investor profile associated to the given id.

    :param id: the investor profile id. (1 = Conservador; 2 = Moderado; 3 = Arrojado)
    :return: (str) investor profile
    """
    investor_profile_map = {1: 'Conservador',
                            2: 'Moderado',
                            3: 'Arrojado'}
    if _id not in investor_profile_map.keys():
        raise AssertionError('The investor profile id does not exist.')
    else:
        return investor_profile_map[_id]


def get_investor_profile_id(investor_profile):
    """
    This method returns the id associated to the given investor profile.

    :param investor_profile: the investor profile. (Conservador = 1; Moderado = 2; Arrojado = 3)
    :return: (int) investor profile id
    """
    investor_profile_map = {'conservador': 1,
                            'moderado': 2,
                            'arrojado': 3}

    if investor_profile.lower() not in investor_profile_map.keys():
        raise AssertionError('The investor profile does not exist.')
    else:
        return investor_profile_map[investor_profile]


def create_response(status, msg, code):
    response_object = {
        'status': status,
        'message': msg,
    }
    return response_object, code, {'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept'}