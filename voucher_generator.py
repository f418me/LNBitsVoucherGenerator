import requests
import json
import logging

HTTP_TIMEOUT_SECONDS = 15


def _create_withdraw_link(voucher_config, ln_bits_config, session):
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

    try:
        response = session.post(
            ln_bits_config.withdraw_link,
            headers=headers,
            data=payload,
            timeout=HTTP_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        response_id = response.json()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed to create LNBits withdraw link: {exc}") from exc
    except ValueError as exc:
        raise RuntimeError("LNBits API returned invalid JSON while creating withdraw link.") from exc

    voucher_id = response_id.get("id")
    if voucher_id is None:
        raise ValueError("LNBits response did not include voucher id.")

    logging.info(f"Generated voucher with id {voucher_id}.")
    return voucher_id


def generate_vouchers(number_of_vouchers, voucher_config, ln_bits_config):
    voucher_ids = []
    with requests.Session() as session:
        for _ in range(int(number_of_vouchers)):
            voucher_ids.append(_create_withdraw_link(voucher_config, ln_bits_config, session))
    return voucher_ids
