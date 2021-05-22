from flask_restx import Namespace, fields


class WalletDto:
    api = Namespace('wallet', description='Wallet related operations')
