import os

from flask import current_app as app

from utilities import utils


def load_id_list(project_id, query_id, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = utils.get_path(location=location, project_id=project_id, query_id=query_id,
                                  filename='identifier_list.txt', prefix=prefix)
    with open(path_to_file) as f:
        eids = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in eids]


def save_id_list(project_id, query_id, identifiers, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = utils.get_path(location=location, project_id=project_id, query_id=query_id, filename='', prefix='')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    path = utils.get_path(location=location, project_id=project_id, query_id=query_id, filename='identifier_list.txt', prefix=prefix)
    with open(path, 'w') as list_file:
        for identifier in identifiers:
            list_file.write(identifier + '\n')
        list_file.close()


def get_last_change(project_id, query_id, prefix=''):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = utils.get_path(location=location, project_id=project_id, query_id=query_id,
                                  filename='identifier_list.txt', prefix=prefix)
    last_change = os.path.getmtime(path_to_file)
    return last_change
