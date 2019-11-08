#################
#    imports    #
#################

from flask import Response
import jinja2
import utilities.utils as utils
from . import wheel_blueprint


################
#    routes    #
################

@wheel_blueprint.route("/doi/<doi>", methods=['GET'])
def build_wheel_for_doi(doi):
    wheel = utils.get_sdg_classification(doi)
    template_loader = jinja2.FileSystemLoader(searchpath="./app/wheel/")
    template_env = jinja2.Environment(loader=template_loader)
    template_file = 'sdg_wheel_template.svg'
    template = template_env.get_template(template_file)
    return Response(template.render(wheel=wheel), mimetype='image/svg+xml')
