#################
#    imports    #
#################

import json

from flask import Response, request

import service.project_service as project_service
from model.Project import Project
from . import project_blueprint


################
#    routes    #
################

@project_blueprint.route("/all", methods=['GET'])
def list_projects():
    """
    shows a list of all available projects
    :return: a JSOn formatted list of all available projects
    """
    projects = project_service.load_all_projects()
    return json.dumps(projects, default=lambda o: o.__getstate__())


@project_blueprint.route("/single/<project_id>", methods=['GET'])
def get_project(project_id):
    """
    loads a project by the project ID
    :param project_id: the ID of the project to be loaded
    :return: the project associated with that ID
    """
    try:
        project = project_service.load_project(project_id)
        return json.dumps(project, default=lambda o: o.__getstate__())
    except FileNotFoundError:
        return Response("File not found", status=404)


@project_blueprint.route("/new", methods=['POST'])
def create_new_project():
    """
    creates the project folder if it not exists
    :return: the newly created or updated project. returns 500 if errors occurs on writing the project to disc.
    """
    project_json = request.get_json(silent=True)
    project = Project(**project_json)
    try:
        project_service.create_project(project)
        return json.dumps(project, default=lambda o: o.__getstate__())
    except IOError:
        return Response("could not create project", status=500)

# loads a project by the project ID
@project_blueprint.route("/single/<project_id>", methods=['DELETE'])
def delete_project(project_id):
    """
    deletes a project by the project ID
    :param project_id: the ID of the project to be deleted
    :return: status of 204 if the project has been deleted, status 500 if the deletion was unseccessful, 404 if the
    project could not be found.
    """
    try:
        if project_service.delete_project(project_id):
            return Response("project deleted", status=204)
        else:
            return Response("an error occured", status=500)
    except FileNotFoundError:
        return Response("File not found", status=404)

