################
#    imports   #
################

import csv
import os

from model.ScivalUpdate import ScivalUpdate
from scival.Scival import Scival
from service import project_service, elasticsearch_service
from . import scival_blueprint
from flask import current_app as app
from flask import jsonify, Response, request


################
#    routes    #
################

# returns true if the scival_data.csv file is present for the iven project
@scival_blueprint.route("/check/<project_id>")
def check_scival(project_id):
    """
    checks whether scival data have been uploaded
    :param project_id: the ID of the current project
    :return: True, if scival data have been uploaded.
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/scival_data.csv'
    return jsonify(os.path.exists(path_to_file))


# uploads the scival data and saves it as scival_data.csv in the working directory
@scival_blueprint.route('/single/<project_id>', methods=['POST'])
def upload_scival_file(project_id):
    """
    retrieves the scival file from the request and saves it to disc
    :param project_id: the ID of the current project
    :return: returns a status of 204 when the file could be saved
    """
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    app.logger.info('project {}: saving scival file'.format(project_id))
    if request.method == 'POST':
        project = project_service.load_project(project_id)
        file = request.files['scival-file']
        path_to_save = location + '/out/' + project_id + '/'
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'scival_data.csv')
        project.isQueryDefined = True
        project_service.save_project(project)
        import_scival_data(project_id)
    return Response("OK", status=204)


# reads in the scival data and uses the results to update the elasticsearch index
@scival_blueprint.route('/import/<project_id>', methods=['GET'])
def import_scival_data(project_id):
    """
    imports the scival data into the data store
    :param project_id: the ID of the current project
    :return: a status of 200 when the data have been imported
    """
    app.logger.info('project {}: importing Scival data'.format(project_id))
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    with open(location + '/out/' + project_id + '/' + 'scival_data.csv', 'r', encoding='utf-8-sig') as csvfile:
        scivals = []
        linereader = csv.DictReader(csvfile, delimiter=',')
        rows = list(linereader)
        app.logger.info('project {}: importing {} lines of scival data'.format(project_id, str(len(rows))))
        for index, row in enumerate(rows):
            app.logger.info('project {}: processed entry {} of {} '.format(project_id, str(index), str(len(rows))))
            if len(row) < 10:
                continue
            scival = Scival(row)
            elasticsearch_service.append_to_index(ScivalUpdate(scival), scival.eid, project_id)
            scivals.append(scival)
        csvfile.close()
        app.logger.info('project {}: imported {} Scival data out of  {}'.format(project_id, str(len(scivals)), str(len(rows))))
    return Response("imported " + str(len(scivals)) + " Scival data", status=200)
