import configparser
import cairosvg
from PIL import Image
import requests
import json
import pandas as pd
from fpdf import FPDF
import os
import glob
from config_withdraw_link import ConfigWithdrawLink

config = configparser.ConfigParser()
config.read('config.ini')


def create_withdraw_link(withdraw_link):
    payload = json.dumps({
        "title": withdraw_link.get_title(),
        "min_withdrawable": withdraw_link.get_min_withdrawable(),
        "max_withdrawable": withdraw_link.get_min_withdrawable(),
        "uses": withdraw_link.get_uses(),
        "wait_time": withdraw_link.get_wait_time(),
        "is_unique": False,
        "webhook_url": withdraw_link.get_webhook_url()
    })
    headers = {
        'Content-type': 'application/json',
        'X-Api-Key': config.get('LNBits', 'ApiKey')
    }

    response = requests.request("POST", withdraw_link.get_url(), headers=headers, data=payload)

    return pd.json_normalize(response.json())


def create_page(page_counter, id_list):
    for i in range(len(id_list)):
        print(id_list[i])
        svg_url = 'https://legend.lnbits.com/withdraw/img/' + id_list[i]

        # Get svg data
        svg_data = requests.get(svg_url).content
        png_file = config.get('General', 'OutputDirectory') + '/' + 'qr_Page_' + str(page_counter) + '_' + str(i) + '.png'
        cairosvg.svg2png(bytestring=svg_data, write_to=png_file)

    background = Image.open(config.get('Page', 'BaseVoucher'))
    background = background.convert("RGBA")

    qr_x_coord = [e.strip() for e in config.get('Page', 'QrXCoord').split(',')]
    qr_y_coord = [e.strip() for e in config.get('Page', 'QrYCoord').split(',')]

    current_qr_on_page = 0
    for xCord in qr_x_coord:
        front_image = Image.open(
            config.get('General', 'OutputDirectory') + '/' + 'qr_Page_' + str(page_counter) + '_' + str(
                current_qr_on_page) + '.png')
        front_image = front_image.resize((int(config.get('Page', 'QrCodeSize')), int(config.get('Page', 'QrCodeSize'))))
        front_image = front_image.convert("RGBA")
        background.paste(front_image, (int(xCord), int(qr_y_coord[current_qr_on_page])), front_image)
        current_qr_on_page = current_qr_on_page + 1
    page_file_name = config.get('General', 'OutputDirectory') + '/' + 'page_' + str(page_counter) + '.png'

    background.save(page_file_name, format="png")

    return page_file_name


def main():
    files = glob.glob(config.get('General', 'OutputDirectory') + '/*')
    for f in files:
        os.remove(f)

    withdraw_link = ConfigWithdrawLink()
    data_frame = pd.DataFrame()
    for x in range(int(config.get('Voucher', 'NumberOfVoucher'))):
        data_frame = pd.concat([data_frame, create_withdraw_link(withdraw_link)])

    data_frame.reset_index()
    id_list = []
    page_counter = 0
    file_name_pages = []
    for index, row in data_frame.iterrows():
        id_list.append(row['id'])
        print(id_list)
        # Länge aus Array Koord ermitteln
        if len(id_list) == 4:
            page_counter = page_counter + 1
            file_name_pages.append(create_page(page_counter, id_list))
            id_list = []

    if len(id_list) > 0:
        page_counter = page_counter + 1
        file_name_pages.append(create_page(page_counter, id_list))
        id_list = []

    print(file_name_pages)

    pdf = FPDF()
    for image in file_name_pages:
        pdf.add_page()
        pdf.set_title('Ekasi Voucher')
        pdf.image(image, 1, 1, 210)

    filename = config.get('General', 'OutputDirectory') + "/" + config.get('Voucher',
                                                                           'NameOfVoucherBatch') + "_Vouchers.pdf"
    pdf.output(filename, "F")
    pdf.close()


if __name__ == "__main__":
    main()
