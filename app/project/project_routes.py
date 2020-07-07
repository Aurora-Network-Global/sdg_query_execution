#################
#    imports    #
#################

import json
import re

from flask import Response, request

import service.project_service as project_service
from model.Project import Project
from model.QueryReference import QueryReference
from service import query_service
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


@project_blueprint.route("/<project_id>/query/<query_id>", methods=['GET'])
def get_query_for_project(project_id, query_id):
    """
    loads a project by the project ID
    :param project_id: the ID of the project to be loaded
    :return: the project associated with that ID
    """
    try:
        query = query_service.load_query(project_id, query_id)
        return json.dumps(query, default=lambda o: o.__getstate__())
    except FileNotFoundError:
        return Response("File not found", status=404)


@project_blueprint.route("/<project_id>/query", methods=['POST'])
def save_query_for_project(project_id):
    """
    loads a project by the project ID
    :param project_id: the ID of the project to be loaded
    :return: the project associated with that ID
    """
    query_json = request.get_json(silent=True)
    query = query_service.from_json(query_json)
    query_service.save_query_to_xml(project_id, query)
    return Response('query saved', status=204)


@project_blueprint.route("/<project_id>/query/<query_id>", methods=['DELETE'])
def delete_query_from_project(project_id, query_id):
    """
    loads a project by the project ID
    :param project_id: the ID of the project to be loaded
    :param query_id: the ID of the query to be deleted
    :return: the project associated with that ID
    """
    project = project_service.remove_query_from_project(project_id=project_id, query_id=query_id)
    return json.dumps(project, default=lambda o: o.__getstate__())


@project_blueprint.route("/new", methods=['POST'])
def create_new_project():
    """
    creates the project folder if it not exists
    :return: the newly created or updated project. returns 500 if errors occurs on writing the project to disc.
    """
    project_json = request.get_json(silent=True)
    project = Project(**project_json)
    if re.match('\d+', project.project_id) or re.match('[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z', project.project_id):
        print('valid ID')
        try:
            project_service.create_project(project)
            return json.dumps(project, default=lambda o: o.__getstate__())
        except IOError:
            return Response("could not create project", status=500)
    else:
        print('ID not valid')
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


@project_blueprint.route("/add_query/<project_id>", methods=['POST'])
def add_query_to_project(project_id):
    query_reference_json = request.get_json(silent=True)
    query_reference = QueryReference(**query_reference_json)
    try:
        project = project_service.add_query_reference(project_id, query_reference)
        return json.dumps(project, default=lambda o: o.__getstate__())
    except IOError:
            return Response("could not update project", status=500)


@project_blueprint.route("/<project_id>/query/<query_id>/scopusSearchString", methods=['GET'])
def get_scopus_search_string(project_id, query_id):
    """
    retrieves the Scopus search string and to display it in the browser
    :param project_id: the ID of the current project
    :return: returns the scopus query strings. if no scopus queries are found, a status of 404 is returned.
    """
    try:
        scopus_queries = query_service.load_scopus_query_string(project_id, query_id)
        return json.dumps(scopus_queries, default=lambda o: o.__getstate__())
    except FileNotFoundError:
        return Response("File not found", status=404)
