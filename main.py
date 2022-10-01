import cairosvg
from PIL import Image
import requests
import json
from fpdf import FPDF
import os
import glob
from config import Config


def create_withdraw_link(voucher_config, ln_bits_config):
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

    response = requests.request("POST", ln_bits_config.withdraw_link, headers=headers, data=payload).json()

    return response["id"]


def create_page(page_counter, id_list, page_config, output_directory):
    for i in range(len(id_list)):
        print(id_list[i])
        svg_url = f"https://legend.lnbits.com/withdraw/img/{id_list[i]}"

        # Get svg data
        svg_data = requests.get(svg_url).content
        png_file = f"{output_directory}/qr_Page_{str(page_counter)}_{str(i)}.png"
        cairosvg.svg2png(bytestring=svg_data, write_to=png_file)

    background = Image.open(page_config.base_voucher)
    background = background.convert("RGBA")

    qr_x_coord = [e.strip() for e in page_config.qr_x_cord.split(',')]
    qr_y_coord = [e.strip() for e in page_config.qr_y_cord.split(',')]

    current_qr_on_page = 0
    for xCord in qr_x_coord:
        front_image = Image.open(f"{output_directory}/qr_Page_{str(page_counter)}_{str(current_qr_on_page)}.png")
        front_image = front_image.resize((int(page_config.qr_code_size), int(page_config.qr_code_size)))
        front_image = front_image.convert("RGBA")
        background.paste(front_image, (int(xCord), int(qr_y_coord[current_qr_on_page])), front_image)
        current_qr_on_page = current_qr_on_page + 1
    page_file_name = f"{output_directory}/page_{str(page_counter)}.png"

    background.save(page_file_name, format="png")

    return page_file_name


def generate_pdf(file_name_pages):
    pdf = FPDF()
    for image in file_name_pages:
        pdf.add_page()
        pdf.set_title('Ekasi Voucher')
        pdf.image(image, 1, 1, 210)
    return pdf


def generate_images(voucher_ids, page_config, output_directory):
    id_list = []
    page_counter = 0
    file_name_pages = []
    for index, id in enumerate(voucher_ids):
        id_list.append(id)
        # Länge aus Array Koord ermitteln
        if len(id_list) == 4:
            page_counter += 1
            file_name_pages.append(create_page(page_counter, id_list, page_config, output_directory))
            id_list = []
    if len(id_list) > 0:
        page_counter += 1
        file_name_pages.append(create_page(page_counter, id_list, page_config, output_directory))

    return file_name_pages


def generate_vouchers(number_of_vouchers, voucher_config, ln_bits_config):
    voucher_ids = []
    for x in range(int(number_of_vouchers)):
        voucher_ids.append(create_withdraw_link(voucher_config, ln_bits_config))
    return voucher_ids


def clear_output_directory(output_directory):
    files = glob.glob(output_directory + '/*')
    for f in files:
        os.remove(f)


def main():
    config = Config("config.ini")
    clear_output_directory(config.general.output_directory)
    voucher_ids = generate_vouchers(config.voucher.number_of_voucher, config.voucher, config.ln_bits)
    file_name_pages = generate_images(voucher_ids, config.page, config.general.output_directory)
    pdf = generate_pdf(file_name_pages)

    filename = f"{config.general.output_directory}/{config.voucher.name_of_voucher_batch}_Vouchers.pdf"
    pdf.output(filename, "F")
    pdf.close()


if __name__ == "__main__":
    main()
