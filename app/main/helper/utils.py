import datetime

def get_side(_id):
    """
        This method returns the side associated to the given id.

        :param id: the side id. (0 = buy; 1 = sell)
        :return: (str) investor profile
    """
    side_map = {0: 'buy',
                     1: 'sell'}

    if _id not in side_map.keys():
        raise AssertionError('The side id does not exist.')
    else:
        return side_map[_id]


def get_side_id(side):
    """
    This method returns the id associated to the given side.

    :param side: the side. (buy = 0; sell = 1)
    :return: (int) side id
    """
    side_map = {'buy': 0,
                'sell': 1}

    if side.lower() not in side_map.keys():
        raise AssertionError('The side does not exist.')
    else:
        return side_map[side]


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
        raise AssertionError('The operation id does not exist.')
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


def get_date(string):
    """

    :param string: string with date in format Y-m-d
    :return: datetime
    :raise ValueError in case of invalid date format
    """

    return datetime.datetime.strptime(string, '%Y-%m-%d')

def create_response(status, msg, code):
    response_object = {
        'status': status,
        'message': msg,
    }
    return response_object, code


def compute_mean_price_amount(prices):
    """
    Given a list of prices and amount, compute the mid price and final amount.

    :param prices: array of tuples (price_i, amount_i)
    :return: mid price, final amount
    """
    amount = 0
    mean_price = 0
    for p, q in prices:
        if q > 0:
            mean_price = (mean_price*amount + p*q)/(amount + q)
        amount += q

    return mean_price, amount