import configparser
from urllib.parse import urlparse


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
        read_files = parser.read(config_url)
        if not read_files:
            raise FileNotFoundError(f"Could not read config file: {config_url}")

        self.general = _General(parser["General"])
        self.ln_bits = _LNBits(parser["LNBits"])
        self.voucher = _Voucher(parser["Voucher"])
        self.page = _Page(parser["Page"])
        self._validate()

    def _validate(self):
        if not self.general.output_directory.strip():
            raise ValueError("General.OutputDirectory must not be empty.")

        if not self.ln_bits.api_key.strip():
            raise ValueError("LNBits.ApiKey must not be empty.")

        if not _is_http_url(self.ln_bits.withdraw_link):
            raise ValueError("LNBits.WithdrawLink must be a valid http(s) URL.")

        if not _is_http_url(self.ln_bits.svg_url):
            raise ValueError("LNBits.SvgUrl must be a valid http(s) URL.")

        number_of_vouchers = int(self.voucher.number_of_voucher)
        if number_of_vouchers <= 0:
            raise ValueError("Voucher.NumberOfVoucher must be greater than 0.")

        min_withdrawable = int(self.voucher.min_withdrawable)
        max_withdrawable = int(self.voucher.max_withdrawable)
        if min_withdrawable > max_withdrawable:
            raise ValueError("Voucher.MinWithdrawable must be <= Voucher.MaxWithdrawable.")

        qr_x_coord = _parse_coordinate_list(self.page.qr_x_cord, "Page.QrXCoord")
        qr_y_coord = _parse_coordinate_list(self.page.qr_y_cord, "Page.QrYCoord")
        if len(qr_x_coord) != len(qr_y_coord):
            raise ValueError("Page.QrXCoord and Page.QrYCoord must have the same number of values.")

        if len(qr_x_coord) == 0:
            raise ValueError("At least one QR coordinate pair must be configured.")

        qr_code_size = int(self.page.qr_code_size)
        if qr_code_size <= 0:
            raise ValueError("Page.QrCodeSize must be greater than 0.")


def _parse_coordinate_list(value, field_name):
    items = [e.strip() for e in value.split(",")]
    if any(item == "" for item in items):
        raise ValueError(f"{field_name} contains empty values.")

    try:
        return [int(item) for item in items]
    except ValueError as exc:
        raise ValueError(f"{field_name} must contain only integer values.") from exc


def _is_http_url(value):
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)
