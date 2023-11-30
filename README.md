# genQR_code
This repo holds python code to create a QR-code based on input from a config.json. It can also put a logo in the center of the QR-code.

Two QR-code versions are available. One that encodes an url and an other that encodes payment information that can be put on an invoice, at least for Swedish banks. ALWAYS double check that the econded information is correct, use your bank app and scan the invoiceQR-code before sending it to a customer. It shows that there is some error handling, if the company name and account number does not match, the bank app throws an error.

YOU HAVE THE FULL RESPONSIBILITY FOR ANY EFFECTS USING QR-CODES GEREATED BY THIS SOFTWARE.

## Using binary
If you choose a precompiled binary, put it next to config.json and logo.png, then double click the executable. You can download example config file and logo.png from here or create your own.
### Config.json content for url
```yaml
{
  "url": "www.klockren.nu",
  "logo": "logo.png",
  "project": "lampa"
}
```

### Config.json content for invoice
```yaml
{
    "invoice_ref": "Donation-0001",
    "invoice_date": "20231025",
    "due_date": "20231112",
    "amount_due": 150.0,
    "uqr": 1,
    "tp": 1,
    "company_name": "UASolutions AB",
    "org_nr": "212000-1363",
    "country_code": "SE",
    "currency": "SEK",
    "payment_type": "BG",
    "account": "265-5389",
    "logo": "black_icon_white_background_square.png"
}
```


## Install
Install requirements
>  pip install -r requirements.txt

## Configure
Configure the config.json

## Execute
To excute the script
>  cd src/urlQR
>  python3 urlQR.py

## Compile urlQR stand alone
To compile a stand alone binary
>  cd src/urlQR

>  pyinstaller --onefile --distpath ../executable --workpath ../tmp urlQR.py

>  cp config.json ../executable

>  cp logo.png ../executable

## Compile invoiceQR stand alone
To compile a stand alone binary
>  cd src/invoiceQR

>  pyinstaller --onefile --distpath ../executable --workpath ../tmp invoiceQR.py

>  cp config.json ../executable

>  cp logo.png ../executable

##
Invoice example
![Donation-0001_logo](https://github.com/agising/genQR_code/assets/49570216/8376956a-ac7e-41ba-b7c8-a35e3be7ec79)

url example

![Example_logo](https://github.com/agising/genQR_code/assets/49570216/71ebe745-78a3-4338-8c4a-3929900ea7b6)

