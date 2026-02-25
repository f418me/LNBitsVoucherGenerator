# LNBits Voucher Generator

Generate printable LNURL-withdraw voucher sheets (QR codes) from an LNbits wallet using a small Python script.

## Project Status

This repository is **archived / maintenance-frozen**.

- No active feature development is planned.
- Existing behavior is kept for historical/reference use.
- Pull requests may not be reviewed.

## What It Does

- Creates LNURL-withdraw links through the LNbits API.
- Renders voucher QR codes onto a background image template.
- Exports all generated pages as a single PDF in `output/`.

## Requirements

- Python 3.9+
- Access to an LNbits instance with the withdraw endpoint enabled

Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

1. Open `config.ini`.
2. Configure your LNbits API values in `[LNBits]`.
3. Set voucher parameters in `[Voucher]`.
4. Set template/position parameters in `[Page]`.

Notes:

- `General.OutputDirectory` is cleared on every run.
- Replace the default API key in `config.ini` before production use.

## Run

```bash
python main.py
```

Result:

- QR/page images and final PDF are written to `output/`.
- Output file pattern: `<NameOfVoucherBatch>_Vouchers.pdf`

## Repository Structure

- `main.py`: entry point, orchestration, output cleanup
- `config.py`: INI config loading
- `voucher_generator.py`: LNbits withdraw-link creation
- `pdf_generator.py`: QR rendering, page composition, PDF creation
- `config.ini`: runtime configuration
- `voucher_vorlage_2100.jpg`: default voucher background template
- `output/.gitkeep`: keeps output directory in git

## License

MIT. See `LICENSE`.
