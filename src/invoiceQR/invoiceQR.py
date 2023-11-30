''' genQR_code'''

__author__ = 'Andreas Gising'
__copyright__ = 'Free to use, please credit'
__status__ = 'development'


import os
import json
import qrcode
import sys
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from datetime import datetime

# Find path to config file and logotype in different versions of python executable
config_name = 'config.json'

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

print('Running mode:', running_mode)
print('  Appliction path  :', application_path)
print('  Config full path :', config_path)

# Try to open the config
try:
  with open(config_path, 'r', encoding="utf-8") as json_file:
    invoice = json.load(json_file)
    logo = invoice['logo']
    # Use inoice reference number as project number
    project = invoice['invoice_ref']
  
    invoice_data = {}
    # Chaning parameters
    invoice_data['iref']= invoice['invoice_ref']
    invoice_data['idt']= invoice['invoice_date']
    invoice_data['ddt']= invoice['due_date']
    invoice_data['due']= invoice['amount_due']
    #Likely static paramters
    invoice_data['uqr']= invoice['uqr']
    invoice_data['tp']= invoice['tp']
    invoice_data['nme']= invoice['company_name']
    invoice_data['cid']= invoice['org_nr']
    invoice_data['cc']= invoice['country_code']
    invoice_data['cur']= invoice['currency']
    invoice_data['pt']= invoice['payment_type']
    invoice_data['acc']= invoice['account']

    # Create a string to encode in the QR
    coded_string = json.dumps(invoice_data)

except:
  # Error in config.json. Show how a correct config.json looks like.
  json_example = {"iref": "Donation-0001", "idt": "20231025", "ddt": "20231112", "due": 150.0, "uqr": 1, "tp": 1, "nme": "UASolutions AB", "cid": "212000-1363", "cc": "SE", "cur": "SEK", "pt": "BG", "acc": "265-5389"}
  print(f'Faulty or no config file. Create a config.json that looks like this: {json.dumps(json_example, indent = 2)}')
  sys.exit()

# Full path to logo
logo_path = os.path.join(application_path, logo)

# Build path for out files
project_dir_path = os.path.join(application_path, project)
if not os.path.exists(project_dir_path):
   # Create directory
   os.makedirs(project_dir_path)
else:
   print('If you are re-generating a QR-code, windows might have difficulties overwriting the existing QR-code. If so, first delete the existing QR-codes.')
out_no_logo_path = os.path.join(project_dir_path, project + '_no_logo.png')
out_logo_path = os.path.join(project_dir_path, project + '_logo.png')

# Create the QR object
qr = qrcode.QRCode(version=4,
                   error_correction=qrcode.constants.ERROR_CORRECT_H)

# Add the link to the qr object
qr.add_data(coded_string)

# Generate the QR withou logo
qr_img = qr.make_image(image_factory=StyledPilImage,
                          module_drawer=CircleModuleDrawer(),
                          eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                          )
qr_img.save(out_no_logo_path)

# Try to generate QR with logo
if os.path.isfile(logo_path):
  qr_img = qr.make_image(image_factory=StyledPilImage,
                          module_drawer=CircleModuleDrawer(),
                          eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                          embeded_image_path=logo_path
                          )
  qr_img.save(out_logo_path)
else:
  print(f'Could not find logotype {logo}')

# Back up the config file, build up file name
time_str = datetime.now().strftime('%Y%m%d-%H%M%S')

config_backup_path = project_dir_path + '/' + time_str + '.json'
# Save the config settings for the generated code(s)
with open(config_backup_path,'w', encoding="utf-8") as outfile:
    outfile.write(json.dumps(invoice, indent=2))

# For more inspiraion on QR-code modifications, please see
# https://github.com/reegan-anne/python_qrcode/blob/main/main.ipynb
