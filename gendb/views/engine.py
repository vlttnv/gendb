"""File processing engine."""

import os

from flask import Blueprint, jsonify, request
from flask.ext.login import login_required

from gendb.tasks import add

engine_bp = Blueprint('engine_bp', __name__)


@engine_bp.route('/upload_ind', methods=['POST'])
@login_required
def upload_ind():
    files = request.files

    # assuming only one file is passed in the request
    key = list(files.keys())[0]
    value = files[key]  # this is a Werkzeug FileStorage object
    filename = value.filename

    if 'Content-Range' in request.headers:
        # extract starting byte from Content-Range header string
        range_str = request.headers['Content-Range']
        start_bytes = int(range_str.split(' ')[1].split('-')[0])

        # append chunk to the file on disk, or create new
        with open(filename, 'a') as f:
            f.seek(start_bytes)
            f.write(value.stream.read())

    else:
        # this is not a chunked request, so just save the whole file
        value.save(filename)
        add(1, 2)

    # send response with appropriate mime type header
    return jsonify({
        "name": value.filename,
        "size": os.path.getsize(filename),
        "url": 'uploads/' + value.filename,
        "thumbnail_url": None,
        "delete_url": None,
        "delete_type": None,
    })
