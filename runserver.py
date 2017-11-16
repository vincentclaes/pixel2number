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
    help="pixel2number",
    default=80,
)
args = parser.parse_args()

if __name__ == '__main__':
    flask_options = dict(
        host='0.0.0.0',
        debug=True,
        threaded=True,
    )

    app.run(**flask_options)

