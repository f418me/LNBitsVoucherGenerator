import cairosvg
from PIL import Image
import requests
import json
from fpdf import FPDF
import os
import glob
from config import Config

config = Config('config.ini')


def create_withdraw_link():
    payload = json.dumps({
        "title": config.voucher.title,
        "min_withdrawable": config.voucher.min_withdrawable,
        "max_withdrawable": config.voucher.max_withdrawable,
        "uses": config.voucher.uses,
        "wait_time": config.voucher.wait_time,
        "is_unique": False,
        "webhook_url": config.voucher.webhook_url
    })
    headers = {
        'Content-type': 'application/json',
        'X-Api-Key': config.ln_bits.api_key
    }

    response = requests.request("POST", config.ln_bits.withdraw_link, headers=headers, data=payload).json()

    return response["id"]


def create_page(page_counter, id_list):
    for i in range(len(id_list)):
        print(id_list[i])
        svg_url = 'https://legend.lnbits.com/withdraw/img/' + id_list[i]

        # Get svg data
        svg_data = requests.get(svg_url).content
        png_file = config.general.output_directory + '/' + 'qr_Page_' + str(page_counter) + '_' + str(
            i) + '.png'
        cairosvg.svg2png(bytestring=svg_data, write_to=png_file)

    background = Image.open(config.page.base_voucher)
    background = background.convert("RGBA")

    qr_x_coord = [e.strip() for e in config.page.qr_x_cord.split(',')]
    qr_y_coord = [e.strip() for e in config.page.qr_y_cord.split(',')]

    current_qr_on_page = 0
    for xCord in qr_x_coord:
        front_image = Image.open(
            config.general.output_directory + '/' + 'qr_Page_' + str(page_counter) + '_' + str(
                current_qr_on_page) + '.png')
        front_image = front_image.resize((int(config.page.qr_code_size), int(config.page.qr_code_size)))
        front_image = front_image.convert("RGBA")
        background.paste(front_image, (int(xCord), int(qr_y_coord[current_qr_on_page])), front_image)
        current_qr_on_page = current_qr_on_page + 1
    page_file_name = config.general.output_directory + '/' + 'page_' + str(page_counter) + '.png'

    background.save(page_file_name, format="png")

    return page_file_name


def main():
    files = glob.glob(config.general.output_directory + '/*')
    for f in files:
        os.remove(f)

    voucher_ids = []
    for x in range(int(config.voucher.number_of_voucher)):
        voucher_ids.append(create_withdraw_link())

    id_list = []
    page_counter = 0
    file_name_pages = []
    for index, id in enumerate(voucher_ids):
        id_list.append(id)
        # Länge aus Array Koord ermitteln
        if len(id_list) == 4:
            page_counter += 1
            file_name_pages.append(create_page(page_counter, id_list))
            id_list = []

    if len(id_list) > 0:
        page_counter += 1
        file_name_pages.append(create_page(page_counter, id_list))

    pdf = FPDF()
    for image in file_name_pages:
        pdf.add_page()
        pdf.set_title('Ekasi Voucher')
        pdf.image(image, 1, 1, 210)

    filename = config.general.output_directory + "/" + config.voucher.name_of_voucher_batch + "_Vouchers.pdf"
    pdf.output(filename, "F")
    pdf.close()


if __name__ == "__main__":
    main()
