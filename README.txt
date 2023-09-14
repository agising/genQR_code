Några rader python-kod genererar en QR-kod baserat på information i en config-fil och en bild i jpg- eller png-format.
För att på enklaste sätt köra python-koden har jag kompilerat ihop en 'executable'. Det ska bara vara att ställa in config-filen och lägga en logga i samma katalog som skriptet och sedan dubbelklicka skriptet.

 
Skriptet läser alltså in inställningar från en json-fil som måste ligga i samma katalog som skriptet genQR_code.

Filen ska heta config.json
Json-filen ska innehålla nycklarna "url" och "logo".
Json är lite petigt med mellanslag, citationstecken och dylikt.
Om det krånglar, öppna config.json i en textredigerare (notepad), ta bort allt innehåll och kopiera in exemplet nedan.

{
  "url": "www.klockren.nu",
  "logo": "logga.jpg",
  "project": "my_project"
}

"Project" kan vara en tom sträng, så här: "project": ""

Under nyckeln "logo" anges filnamnet på den logga som ska hamna mitt i QR-koden. Skriptet kommer att generara en QR-kod med och en utan logga. En QR-kod utan logga är lättare att läsa, mindre risk för att läsningen kommer att misslyckas.


Om det av någon anledning slutar att fungera i framtiden kan ni antingen använda en gratistjänst på nätet eller ge er på python-koden själva eller med hjälp av IT-firma eller en driftig ungdom kanske. Med informationen nedan löser ni det!
För att komma till en exekverbar fil har jag använt pyinstaller
$> pyinstaller --onefile --distpath ../executable --workpath ../tmp genQR_code.py 


####################################################################
# https://github.com/reegan-anne/python_qrcode/tree/main
# https://github.com/reegan-anne/python_qrcode/blob/main/main.ipynb
####################################################################

import sys,os
import json
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer

# Find path to config file and logotype in different versions of python executable
config_name = 'config.json'
logo_jpg_name = 'logga.jpg'
logo_png_name = 'logga.png'

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'

config_path = os.path.join(application_path, config_name)
logo_jpg_path = os.path.join(application_path, logo_jpg_name)
logo_png_path = os.path.join(application_path, logo_png_name)

print('Running mode:', running_mode)
print('  Appliction path  :', application_path)
print('  Config full path :', config_path)
print('  Logo.jpg full path :', logo_jpg_path)
print('  Logo.png full path :', logo_png_path)

try:
  with open(config_path, 'r', encoding="utf-8") as json_file:
    config = json.load(json_file)
    url = config['url']
    logo = config['logo']
    project = config['project']
except:
  print('Faulty or no config file. Read the README.txt')
  sys.exit()

# Build path for out files
out_no_logo_path = os.path.join(application_path, project + '_no_logo.png')
out_logo_path = os.path.join(application_path, project + '_logo.png')

# Create the QR object
qr = qrcode.QRCode(version=4,
                   error_correction=qrcode.constants.ERROR_CORRECT_H)

# Add the link to the qr object
qr.add_data(url)

# Generate the QR withou logo
qr_img = qr.make_image(image_factory=StyledPilImage,
                          module_drawer=CircleModuleDrawer(),
                          eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                          )
qr_img.save(out_no_logo_path)

# Try to generate QR with logo, test what logo file ending is used, jpg or png
# Look for jpg
if os.path.isfile(logo_jpg_path):
  qr_img = qr.make_image(image_factory=StyledPilImage,
                          module_drawer=CircleModuleDrawer(),
                          eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                          embeded_image_path=logo_jpg_path
                          )
  qr_img.save(out_logo_path)
# Else look for png
elif os.path.isfile(logo_png_path):
  qr_img = qr.make_image(image_factory=StyledPilImage,
                            module_drawer=CircleModuleDrawer(),
                            eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                            embeded_image_path=logo_jpg_path
                            )
  qr_img.save(out_logo_path)
else:
  print(f'Could not find logotype {logo}')
