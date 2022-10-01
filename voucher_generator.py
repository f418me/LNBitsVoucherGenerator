import requests
import json
import logging


def _create_withdraw_link(voucher_config, ln_bits_config):
    payload = json.dumps({
        "title": voucher_config.title,
        "min_withdrawable": voucher_config.min_withdrawable,
        "max_withdrawable": voucher_config.max_withdrawable,
        "uses": voucher_config.uses,
        "wait_time": voucher_config.wait_time,
        "is_unique": False,
        "webhook_url": voucher_config.webhook_url
    })
    headers = {
        'Content-type': 'application/json',
        'X-Api-Key': ln_bits_config.api_key
    }

    response_id = requests.request("POST", ln_bits_config.withdraw_link, headers=headers, data=payload).json()
    voucher_id = response_id["id"]
    logging.info(f"Generated voucher with id {voucher_id}.")
    return voucher_id


def generate_vouchers(number_of_vouchers, voucher_config, ln_bits_config):
    voucher_ids = []
    for x in range(int(number_of_vouchers)):
        voucher_ids.append(_create_withdraw_link(voucher_config, ln_bits_config))
    return voucher_ids
