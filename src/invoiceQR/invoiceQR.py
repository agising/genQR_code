''' genQR_code'''

__author__ = 'Andreas Gising'
__copyright__ = 'Free to use, please credit'
__status__ = 'development'


import os
import json
import qrcode
import sys
import argparse
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from datetime import datetime


# parse command-line arguments
parser = argparse.ArgumentParser(description='genQRCode', allow_abbrev=False, add_help=False)
parser.add_argument('-h', '--help', action='help', help=argparse.SUPPRESS)
parser.add_argument('--invoice', action='store_true', help='Creates invoice QR', required=False)
# Set defaults
parser.set_defaults(feature=True)
# Parse
args = parser.parse_args()

# Find path to config file and logotype in different versions of python executable
config_name = 'config.json'
invoice_config_name = 'invoice.json'

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
invoice_config_path = os.path.join(application_path, invoice_config_name)

print('Running mode:', running_mode)
print('  Appliction path  :', application_path)
print('  Config full path :', config_path)

# Try to open the config
try:
  with open(config_path, 'r', encoding="utf-8") as json_file:
    config = json.load(json_file)
    url = config['url']
    logo = config['logo']
    project = config['project']
except:
  json_example = {"url": "klockren.nu", "logo": "logga.png", "project": "project_name"}
  print(f'Faulty or no config file. Create a config.json that looks like this: \n{json.dumps(json_example, ident = 2)}')
  sys.exit()

if args.invoice:
   # Replace url
  url = {}
  # Try to open the invoice
  try:
    with open(invoice_config_path, 'r', encoding="utf-8") as json_file:
      invoice = json.load(json_file)
      invoice_data = {}
      invoice_data['uqr']= invoice['uqr']
      invoice_data['tp']= invoice['tp']
      invoice_data['nme']= invoice['company_name']
      invoice_data['cc']= invoice['country_code']
      invoice_data['cid']= invoice['org_nr']
      invoice_data['iref']= invoice['invoice_ref']
      invoice_data['idt']= invoice['invoice_date']
      invoice_data['ddt']= invoice['due_date']
      invoice_data['due']= invoice['due']
      invoice_data['cur']= invoice['currency']
      invoice_data['pt']= invoice['payment_type']
      invoice_data['acc']= invoice['account']

      url = json.dumps(invoice_data)
      print('invoice data loaded')
  except:
    # TODO
    json_example = {"url": "klockren.nu", "logo": "logga.png", "project": "project_name"}
    print(f'Faulty or no config file. Create a config.json that looks like this: \n{json.dumps(json_example, ident = 2)}')
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
qr.add_data(url)

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
    outfile.write(json.dumps(config, indent=2))

# For more inspiraion on QR-code modifications, please see
# https://github.com/reegan-anne/python_qrcode/blob/main/main.ipynb
