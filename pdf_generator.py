import cairosvg
import requests
from PIL import Image
from fpdf import FPDF
import logging

HTTP_TIMEOUT_SECONDS = 15


def _parse_coordinates(page_config):
    qr_x_coord = [int(e.strip()) for e in page_config.qr_x_cord.split(',')]
    qr_y_coord = [int(e.strip()) for e in page_config.qr_y_cord.split(',')]
    return qr_x_coord, qr_y_coord


def create_page(page_counter, id_list, page_config, output_directory, svg_url, session):
    for i, voucher_id in enumerate(id_list):
        svg_url_id = f"{svg_url}{voucher_id}"

        try:
            response = session.get(svg_url_id, timeout=HTTP_TIMEOUT_SECONDS)
            response.raise_for_status()
            svg_data = response.content
        except requests.RequestException as exc:
            raise RuntimeError(f"Failed to download SVG for voucher id {voucher_id}: {exc}") from exc

        png_file = f"{output_directory}/qr_Page_{str(page_counter)}_{str(i)}.png"
        cairosvg.svg2png(bytestring=svg_data, write_to=png_file)

    background = Image.open(page_config.base_voucher)
    background = background.convert("RGBA")

    qr_x_coord, qr_y_coord = _parse_coordinates(page_config)

    current_qr_on_page = 0
    for x_coord, y_coord in zip(qr_x_coord, qr_y_coord):
        if current_qr_on_page >= len(id_list):
            break

        front_image = Image.open(f"{output_directory}/qr_Page_{str(page_counter)}_{str(current_qr_on_page)}.png")
        front_image = front_image.resize((int(page_config.qr_code_size), int(page_config.qr_code_size)))
        front_image = front_image.convert("RGBA")
        background.paste(front_image, (x_coord, y_coord), front_image)
        current_qr_on_page = current_qr_on_page + 1

    page_file_name = f"{output_directory}/page_{str(page_counter)}.png"

    background.save(page_file_name, format="png")

    logging.info(f"Created page Nr. {page_counter} and saved it to \"{page_file_name}\".")

    return page_file_name


def generate_images(voucher_ids, page_config, output_directory, svg_url):
    qr_x_coord, qr_y_coord = _parse_coordinates(page_config)
    vouchers_per_page = min(len(qr_x_coord), len(qr_y_coord))

    id_list = []
    page_counter = 0
    file_name_pages = []

    with requests.Session() as session:
        for voucher_id in voucher_ids:
            id_list.append(voucher_id)
            if len(id_list) == vouchers_per_page:
                page_counter += 1
                file_name_pages.append(create_page(page_counter, id_list, page_config, output_directory, svg_url, session))
                id_list = []

        if len(id_list) > 0:
            page_counter += 1
            file_name_pages.append(create_page(page_counter, id_list, page_config, output_directory, svg_url, session))

    return file_name_pages


def generate_pdf(file_name_pages, name_of_voucher_batch):
    pdf = FPDF()
    for image in file_name_pages:
        pdf.add_page()
        pdf.set_title(name_of_voucher_batch)
        pdf.image(image, 1, 1, 210)
    logging.info(f"Generated PDF \"{name_of_voucher_batch}\" with {len(file_name_pages)} page(s).")
    return pdf
