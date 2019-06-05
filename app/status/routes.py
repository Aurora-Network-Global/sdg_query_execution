from json import JSONDecodeError

from flask import Response, request, jsonify

from model.Status import Status
from service import status_service
from . import status_blueprint


# reads the status file (status.json) and returns it.
@status_blueprint.route("/single/<query_id>")
def get_status(query_id):
    try:
        status = status_service.load_status(query_id)
        return jsonify(status)
    except FileNotFoundError:
        return jsonify('status not found', status=404)
    except JSONDecodeError:
        status = Status("STARTING")
        return jsonify(status.__dict__)


