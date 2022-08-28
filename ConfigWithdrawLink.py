import configparser
from WithdrawLink import WithdrawLink


class ConfigWithdrawLink(WithdrawLink):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        super().__init__(config.get('LNBits', 'WithdrawLink'), config.get('Voucher', 'Title'),
                       config.get('Voucher', 'MinWithdrawable'), config.get('Voucher', 'MaxWithdrawable'),
                       config.get('Voucher', 'Uses'), config.get('Voucher', 'WaitTime'),
                       config.get('Voucher', 'WebhookUrl'))


