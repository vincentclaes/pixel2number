#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# import sys
# import argparse
#
# from pixel2number.application import application
#
#
# flask_options = dict(
#     host='0.0.0.0',
#     debug=True,
#     port=args.port,
#     threaded=True,
# )

import glob
import json
import os
import zipfile
from uuid import uuid4
import shutil
from flask import Flask, request, redirect, url_for, render_template, send_file

from pixel2number import image_converter

dir_path = os.path.dirname(os.path.realpath(__file__))

application = Flask(__name__)


@application.route("/")
@application.route("/index")
def index():
    return render_template("index.html")


@application.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "pixel2number/static/uploads/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))


@application.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "pixel2number/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        image_converter.convert(file)
        files.append(fname)

    return render_template("files.html",
                           uuid=uuid,
                           files=files,
                           )


def cleanup(func):
    def wrapped(uuid):
        response = func(uuid)
        for root, dirs, files in os.walk('pixel2number/static/uploads'):
            for dir_ in dirs:
                if dir_ != uuid:
                    shutil.rmtree(os.path.join(root, dir_))
        return response

    return wrapped


@application.route('/return-files/<uuid>')
@cleanup
def return_files(uuid):
    root = "pixel2number/static/uploads/{}".format(uuid)
    # create zip file from all files in uuid folder
    local_zipfile = os.path.join(root, uuid + '.zip')
    zip = zipfile.ZipFile(local_zipfile, "w", zipfile.ZIP_DEFLATED)
    for individualFile in os.listdir(root):
        if '.zip' not in individualFile:
            zip.write(os.path.join(root, individualFile))
    zip.close()
    return send_file('static/uploads/{}/{}.zip'.format(uuid, uuid), attachment_filename='pixel2number.zip',
                     as_attachment=True)


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))


if __name__ == '__main__':
    application.debug = True
    # application.run(**flask_options)
    application.run()

