

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/f418me/LNBitsVoucherGenerator">
    <img src="https://f418.me/wp-content/uploads/2022/08/bild_qr.jpg" alt="Logo" width="500" height="300">
  </a>

  <h3 align="center">LNBits Bitcoin Lightning Vouchers</h3>

  <p align="center">
    Python Script to generate as much Bitcoin Lightning Vouchers you want.
    <br />
    <br />
    <a href="https://github.com/f418me/LNBitsVoucherGenerator/issues">Report Bug</a>
    ·
    <a href="https://github.com/f418me/LNBitsVoucherGenerator/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- 
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->

LNbits a free and open-source lightning wallet that offers a lot of extension. 
LNbits can run on any lightning-network funding source, currently supporting LND, c-lightning, OpenNode, lntxbot, LNPay and even LNbits itself!

You can run LNbits for yourself, or easily take the service from LNBits.

Each wallet has its own API keys and there is no limit to the number of wallets you can make.

Extensions add extra functionality to LNbits so it is possible to experiment with a range of cutting-edge technologies on the lightning network. One of the extension ist LNURL-withdraw.

You can generate LNURL-withdraw links wich are also available in form of QR-Codes. With this QR-Codes every wallet that supports LNURL-withdraw can remain the amount which is defined.

Generating vouchers in large quantities by the GUI is painful. Therefore you can use this script.



<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- GETTING STARTED -->
## Getting Started


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/f418me/LNbitsVoucherGenerator.git
   ```
2. Install Pyhton Packages:
   ```sh
   pip install cairosvg
   pip install requests
   pip install pandas
   pip install PIL
   pip install fpdf
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
### Usage
Setup an LNBits Wallet and activate the LNURL-withdraw extension.
Do the configuration in the config.ini file. Maybe you also like to change the desing of the voucher. Just define an other background image.

 ```sh
   python main.py
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add Changelog
- [ ] Add Logging
- [ ] Add Docker Compose
- [ ] Add possibility to use CSV-Files as Input to generate the vouchers


See the [open issues](https://github.com/f418me/LNBitsVoucherGenerator/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

LNBitsVoucherGenerator is released under the terms of the MIT license. See [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) for further information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

f418.me - [f418_me](https://twitter.com/f418_me) - info@f418.me

Project Link: [https://github.com/f418me/LNBitsVoucherGenerator](https://github.com/f418me/LNBitsVoucherGenerator)

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/f418me/LNBitsVoucherGenerator?style=for-the-badge
[contributors-url]: https://github.com/f418me/LNBitsVoucherGenerator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/f418me/LNBitsVoucherGenerator.svg?style=for-the-badge
[forks-url]: https://github.com/f418me/LNBitsVoucherGenerator/network/members
[issues-shield]: https://img.shields.io/github/issues/f418me/LNBitsVoucherGenerator.svg?style=for-the-badge
[issues-url]: https://github.com/f418me/LNBitsVoucherGenerator/issues
[license-shield]: https://img.shields.io/github/license/f418me/LNBitsVoucherGenerator.svg?style=for-the-badge
[license-url]: https://github.com/f418me/LNBitsVoucherGenerator/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/f418-me/
[product-screenshot]: images/screenshot.png
