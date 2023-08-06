import logging

import zapf.io
import zapf.scan

logging.basicConfig(level=logging.DEBUG)

# URL = 'modbus://127.0.0.1:5002/0'
# URL = 'ads://ccr12.ictrl.frm2/5.53.35.202:800'
URL = 'tango://ccr12.ictrl.frm2:10000/box/plc/modbus'

scan = zapf.scan.Scanner(URL, logging.root)
for dev in scan.scan_devices():
    print('got a device:', dev)
