#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys
import argparse

from pixel2number.application import application
#
#
# flask_options = dict(
#     host='0.0.0.0',
#     debug=True,
#     port=args.port,
#     threaded=True,
# )

if __name__ == '__main__':
    application.debug = True
    # application.run(**flask_options)
    application.run()

