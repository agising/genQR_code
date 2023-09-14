# genQR_code
This repo holds simple python code to create a QR-code based on input from a config.json. It can put a logo in the center of the QR-code

## Install
Install requirements
>  pip install -r requirements.txt

## Configure
Configure the config.json, set up your own url

## Execute
Excute the script
>  cd src
>  python3 genQR_code.py

## Compile stand alone
To compile a stand alone binary
>  cd src
>  pyinstaller --onefile --distpath ../executable --workpath ../tmp genQR_code.py
>  cp config.json ../executable
>  cp logo.png ../executable
