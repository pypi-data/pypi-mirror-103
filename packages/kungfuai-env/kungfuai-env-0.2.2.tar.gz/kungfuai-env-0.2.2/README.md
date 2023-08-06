<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://www.linkedin.com/company/kungfuai/">
    <img src="https://www.kungfu.ai/wp-content/uploads/2020/06/kungfu-lockup-variant-1.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">KUNGFU.AI Env</h3>

  <p align="center">
    Environment handling to simplify development environments
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Dependencies](#dependencies)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

### Built With
* [Python-Dotenv](https://flask.palletsprojects.com/en/1.1.x/)
* [Python 3.8](https://www.python.org/)



<!-- GETTING STARTED -->
## Getting Started

This repo aims to be a cloud and local compatible approach to modern application environment handling.

Environment files committed with the repo bring us some clear advantages that we should consider
when building software.

At KUNGFU.AI, many of our usecases are single container microservice deployment into a cloud. By committing secrets to
cloud Secret Manager, and keeping Secret IDs + other environment data within our env files, we're able to:

1. Keep our deployed assets secure
2. Developers don't have to pass keys, know about keys, or share env files (YUCK)
3. Developers can pull and run their repos immediately.

The kungfuai/env repo aims to simplify the above usecases.

### Dependencies
Python 3.8

### Installation

`pip install kungfuai-env`

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/kungfuai/env/issues) for a list of proposed features (and known issues).

1. Add semantic versioning
2. Deploy to PyPi


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Endurance Idehen - endurance.idehen@kungfu.ai




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/kungfuai/env/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/kungfuai/
[product-screenshot]: images/screenshot.png
