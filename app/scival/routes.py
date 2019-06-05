import csv
import os

from model.ScivalUpdate import ScivalUpdate
from scival.Scival import Scival
from service import project_service, elasticsearch_service
from . import scival_blueprint
from flask import current_app as app
from flask import jsonify, Response, request


# returns true if the scival_data.csv file is present for the iven project
@scival_blueprint.route("/check/<query_id>")
def check_scival(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + query_id + '/scival_data.csv'
    return jsonify(os.path.exists(path_to_file))


# uploads the scival data and saves it as scival_data.csv in the working directory
@scival_blueprint.route('/single/<query_id>', methods=['POST'])
def upload_scival_file(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    print("saving scival file for " + query_id)
    if request.method == 'POST':
        project = project_service.load_project(query_id)
        file = request.files['scival-file']
        path_to_save = location + '/out/' + query_id + '/'
        print(path_to_save)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        file.save(path_to_save + 'scival_data.csv')
        project['isScivalData'] = True
        project_service.save_project(project)
        import_scival_data(query_id)
    return Response("OK", status=204)


# reads in the scival data and uses the results to update the elasticsearch index
@scival_blueprint.route('/import/<query_id>', methods=['GET'])
def import_scival_data(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    with open(location + '/out/' + query_id + '/' + 'scival_data.csv', 'r') as csvfile:
        scivals = []
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row.__len__() < 10:
                continue
            if row[0] == 'Title':
                continue
            scival = Scival(row)
            elasticsearch_service.append_to_index(ScivalUpdate(scival), scival.eid, query_id)
            scivals.append(scival)
        csvfile.close()
    return "imported " + str(scivals.__len__()) + " Scival data"

