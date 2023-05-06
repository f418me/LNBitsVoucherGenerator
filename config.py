import configparser


class _General:
    def __init__(self, parser):
        self.output_directory = parser["OutputDirectory"]
        self.debug_level = parser["DebugLevel"]

class _LNBits:
    def __init__(self, parser):
        self.api_key = parser["ApiKey"]
        self.withdraw_link = parser["WithdrawLink"]
        self.svg_url = parser["SvgUrl"]


class _Voucher:
    def __init__(self, parser):
        self.name_of_voucher_batch = parser["NameOfVoucherBatch"]
        self.number_of_voucher = parser["NumberOfVoucher"]
        self.title = parser["Title"]
        self.min_withdrawable = parser["MinWithdrawable"]
        self.max_withdrawable = parser["MaxWithdrawable"]
        self.uses = parser["Uses"]
        self.wait_time = parser["WaitTime"]
        self.webhook_url = parser["WebhookUrl"]


class _Page:
    def __init__(self, parser):
        self.base_voucher = parser["BaseVoucher"]
        self.qr_code_size = parser["QrCodeSize"]
        self.qr_x_cord = parser["QrXCoord"]
        self.qr_y_cord = parser["QrYCoord"]


class Config:
    def __init__(self, config_url):
        parser = configparser.ConfigParser()
        parser.read(config_url)
        self.general = _General(parser["General"])
        self.ln_bits = _LNBits(parser["LNBits"])
        self.voucher = _Voucher(parser["Voucher"])
        self.page = _Page(parser["Page"])
