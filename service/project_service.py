import json
import os
import shutil

from flask import current_app as app

from model.Project import Project
from model.ProjectList import ProjectList


def delete_project(project_id):
    """deletes a project by the provided ID"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '.json'
    try:
        os.remove(path_to_file)
        shutil.rmtree(location + '/out/' + project_id)
        return True
    except IOError:
        return False


def load_project(project_id):
    """loads a project by the provided ID"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '.json'
    with open(path_to_file) as json_file:
        project = json.load(json_file)
        json_file.close()
        return Project(**project)


def load_all_projects():
    """loads all available projects"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    projects = ProjectList(None)
    list_filenames = os.listdir(location + '/out/')
    for filename in list_filenames:
        if filename.endswith('.json'):
            path_to_file = location + '/out/' + filename
            try:
                with open(path_to_file) as json_file:
                    project = json.load(json_file)
                    json_file.close()
                    projects.add_project(Project(**project))
            except FileNotFoundError:
                continue
    return projects


def save_project(project):
    """save the project on disc"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    json_string = json.dumps(project, default=lambda o: o.__getstate__())
    out_dir = location + '/out/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + project.project_id + '.json', 'w') as json_file:
        json_file.write(json_string)


def create_project(project):
    """creates a new project and creates the corresponding folder"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    save_project(project)
    path = location + '/out/' + project.project_id
    if not os.path.exists(path):
        os.makedirs(path)
    return project
