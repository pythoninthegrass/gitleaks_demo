#!/usr/bin/env python3

import pyqrcode
from pathlib import Path
from pyqrcode import QRCode

home = str(Path.home())

qr = pyqrcode.create(
    '''
    https://www.tailwindapp.com
    https://www.meetup.com/okccoffeeandcode
    https://www.meetup.com/pythonistas
    ''',
    encoding='binary',
)
qr.png(Path(f"{home}/Downloads/thanks.png"), scale=8)
