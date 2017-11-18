#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import argparse

from pixel2number.application import app

parser = argparse.ArgumentParser(description="Uploadr")
parser.add_argument(
    "--port", "-p",
    type=int,
    help="pixel2number"
)
args = parser.parse_args()
flask_options = dict(
    host='0.0.0.0',
    debug=True,
    port=args.port,
    threaded=True,
)

if __name__ == '__main__':
    app.debug = True
    app.run(**flask_options)

