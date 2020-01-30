#################
#    imports    #
#################

import json

from service import status_service, elasticsearch_service
from . import status_blueprint


#################
#    routes     #
#################

@status_blueprint.route("/collection_progress/<project_id>")
def get_collection_progress(project_id):
    """
    reads the number of collected entries from elasticsearch
    :param project_id: the ID of the current project
    :return: a JSON formatted status object depicting the number of collected entries
    """
    status = status_service.load_status(project_id)
    status.progress = elasticsearch_service.get_number_of_records(project_id=project_id)
    return json.dumps(status, default=lambda o: o.__getstate__())
