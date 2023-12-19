# OperaGX Discord Promocode Generator

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Disclaimer](#disclaimer)

## About <a name = "about"></a>

OperaGX Discord Promocode Generator is a tool that generates Discord promotion codes through Opera GX. It utilizes the `operagxdriver` to launch Opera GX and save the generated promotion links to a file.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

- Python 3+
- Opera GX
- Opera Chromium Driver
    > You can get it from [here](https://github.com/operasoftware/operachromiumdriver/releases). Download the driver that matches your browser version.

### Installing

First, open your terminal and clone the repo then navigate to it.
```
git clone https://github.com/NoobToolzz/OperaGX-Discord-Promocode-Generator.git
cd OperaGX-Discord-Promocode-Generator
```

Next, install the requirements
```
pip install -r requirements.txt
```

Finally, edit `config.json` as follows

- If you have Opera GX browser installed on the default path, the script will automatically detect it. Otherwise, navigate to your Opera GX folder and find `opera.exe`. Replace the value of `opera_browser_exe` in `config.json` with the path to `opera.exe`.

- Replace the value of `opera_driver_exe` in `config.json` with the path to the downloaded Opera GX driver.


## Usage <a name = "usage"></a>

Launch `main.py` or navigate to your terminal and and type `python main.py`

## Disclaimer <a name = "disclaimer"></a>
> This tool was created for educational purposes only. I do not endorse any illegal or unethical activities. Please ensure that you comply with Discord and Opera's Terms of Service. I am not responsible for any misuse of this tool.
