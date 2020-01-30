################
#    imports   #
################

from service import query_service
from . import query_viewer_blueprint


################
#    routes    #
################

@query_viewer_blueprint.route("/view/<project>/<version>/<name>", methods=['GET'])
def display_query(project, version, name):
    """
    loads an xml query from disc and uses the stored stylesheet 'queries.xsl' to transform it into an html file.
    :param project: the overall project, which can contain multiple queries
    (not identifical to the projects responsible for managing a single query)
    :param version: the version of the query.
    :param name: the name of the query
    :return: an html page depicting the selected query.
    """
    return query_service.get_versioned_query_as_html(project, version, name)
