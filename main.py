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


def createWithdrawLink(withdrawLink):
    payload = json.dumps({
        "title": withdrawLink.get_title(),
        "min_withdrawable": withdrawLink.get_minWithdrawable(),
        "max_withdrawable": withdrawLink.get_minWithdrawable(),
        "uses": withdrawLink.get_uses(),
        "wait_time": withdrawLink.get_waitTime(),
        "is_unique": False,
        "webhook_url": withdrawLink.get_webhookUrl()
    })
    headers = {
        'Content-type': 'application/json',
        'X-Api-Key': config.get('LNBits', 'ApiKey')
    }

    response = requests.request("POST", withdrawLink.get_url(), headers=headers, data=payload)

    return pd.json_normalize(response.json())


def createPage(pageCounter, idList):
    for i in range(len(idList)):
        print(idList[i])
        svg_url = 'https://legend.lnbits.com/withdraw/img/' + idList[i]

        # Get svg data
        svg_data = requests.get(svg_url).content
        pngfile = config.get('General', 'OutputDirectory') + '/' + 'qr_Page_' + str(pageCounter) + '_' + str(i) + '.png'
        cairosvg.svg2png(bytestring=svg_data, write_to=pngfile)

    background = Image.open(config.get('Page', 'BaseVoucher'))
    background = background.convert("RGBA")

    qrXCoord = [e.strip() for e in config.get('Page', 'QrXCoord').split(',')]
    qrYCoord = [e.strip() for e in config.get('Page', 'QrYCoord').split(',')]

    currentQROnPage = 0
    for xCord in qrXCoord:
        frontImage = Image.open(
            config.get('General', 'OutputDirectory') + '/' + 'qr_Page_' + str(pageCounter) + '_' + str(
                currentQROnPage) + '.png')
        frontImage = frontImage.resize((int(config.get('Page', 'QrCodeSize')), int(config.get('Page', 'QrCodeSize'))))
        frontImage = frontImage.convert("RGBA")
        background.paste(frontImage, (int(xCord), int(qrYCoord[currentQROnPage])), frontImage)
        currentQROnPage = currentQROnPage + 1
    pageFileName = config.get('General', 'OutputDirectory') + '/' + 'page_' + str(pageCounter) + '.png'

    background.save(pageFileName, format="png")

    return pageFileName


def main():
    files = glob.glob(config.get('General', 'OutputDirectory') + '/*')
    for f in files:
        os.remove(f)

    withdrawLink = ConfigWithdrawLink()
    dataFrame = pd.DataFrame()
    for x in range(int(config.get('Voucher', 'NumberOfVoucher'))):
        dataFrame = pd.concat([dataFrame, createWithdrawLink(withdrawLink)])

    dataFrame.reset_index()
    idList = []
    pageCounter = 0
    fileNamePages = []
    for index, row in dataFrame.iterrows():
        idList.append(row['id'])
        print(idList)
        # Länge aus Array Koord ermitteln
        if len(idList) == 4:
            pageCounter = pageCounter + 1
            fileNamePages.append(createPage(pageCounter, idList))
            idList = []

    if len(idList) > 0:
        pageCounter = pageCounter + 1
        fileNamePages.append(createPage(pageCounter, idList))
        idList = []

    print(fileNamePages)

    pdf = FPDF()
    for image in fileNamePages:
        pdf.add_page()
        pdf.set_title('Ekasi Voucher')
        pdf.image(image, 1, 1, 210)

    filename = config.get('General', 'OutputDirectory') + "/" + config.get('Voucher',
                                                                           'NameOfVoucherBatch') + "_Vouchers.pdf"
    pdf.output(filename, "F")
    pdf.close()


if __name__ == "__main__":
    main()
