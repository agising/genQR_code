This repo creates a QR-code based on input from a config.json.

Install requirements
  pip install -r requirements.txt

Configure the config.json, set up your own url

Excute the script

  cd src
  python3 genQR_code.py

To compile a stand alone binary
  cd src
  pyinstaller --onefile --distpath ../executable --workpath ../tmp genQR_code.py
  cp config.json ../executable
  cp logo.png ../executable
