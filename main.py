import os
import glob
import logging
from config import Config
from pdf_generator import generate_images, generate_pdf
from voucher_generator import generate_vouchers


def clear_output_directory(output_directory):
    files = glob.glob(output_directory + '/*')
    for f in files:
        os.remove(f)
    logging.info(f"Cleared output directory \"{output_directory}\".")


def main():
    config = Config("config.ini")
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=str(config.general.debug_level))

    clear_output_directory(config.general.output_directory)

    voucher_ids = generate_vouchers(config.voucher.number_of_voucher, config.voucher, config.ln_bits)
    images = generate_images(voucher_ids, config.page, config.general.output_directory, config.ln_bits.svg_url)
    pdf = generate_pdf(images, config.voucher.name_of_voucher_batch)

    filename = f"{config.general.output_directory}/{config.voucher.name_of_voucher_batch}_Vouchers.pdf"
    pdf.output(filename)
    pdf.close()

    logging.info(f"Wrote generated PDF file to \"{filename}\".")


if __name__ == "__main__":
    main()
