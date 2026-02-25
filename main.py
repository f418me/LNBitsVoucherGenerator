import os
import glob
import logging
from config import Config
from pdf_generator import generate_images, generate_pdf
from voucher_generator import generate_vouchers


def clear_output_directory(output_directory):
    os.makedirs(output_directory, exist_ok=True)
    files = glob.glob(output_directory + '/*')
    for file_path in files:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            try:
                os.remove(file_path)
            except OSError as exc:
                logging.warning(f"Could not remove file \"{file_path}\": {exc}")
        else:
            logging.debug(f"Skipping non-file path in output directory: \"{file_path}\".")
    logging.info(f"Cleared output directory \"{output_directory}\".")


def _resolve_logging_level(level_name):
    normalized_name = str(level_name).upper()
    level = getattr(logging, normalized_name, None)
    return level if isinstance(level, int) else logging.INFO


def main():
    config = Config("config.ini")
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=_resolve_logging_level(config.general.debug_level)
    )

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
