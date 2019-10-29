from flask import request

from app.crossref import crossref_blueprint
from flask import current_app as app

from pybliometrics import scopus

from crossref.CrossRefSearch import CrossRefSearch


@crossref_blueprint.route('/titles2dois/<query_id>', methods=['POST'])
def titles_to_dois(query_id):
    n_crossref = 0
    n_scopus = 0
    delimiter = ";"

    filename = request.form['filename']
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    file_folder = location + '/out/' + query_id + '/'
    file = open(file_folder + filename, "r", encoding="utf-8")
    file_output = open(file_folder + filename.replace(".txt", ".out"), 'w', encoding="utf-8")
    file_data = open(file_folder + filename.replace(".txt", ".data"), 'w', encoding="utf-8")
    file_output.write(
        "reference; DOI; Print ISSN; Online ISSN; title; score; cited-by (CrossRef); authors; title in reference?; "
        "PubMed ID; Scopus ID; EID; Link; cited-by (Scopus)\n")
    file_data.write("references; CrossRef Response; MyCoRe Response; Scopus Response")
    lines = file.readlines()
    for line in lines:
        data = CrossRefSearch(line)
        if data is not None:
            n_crossref += 1
            try:
                scopus_abstract = scopus.AbstractRetrieval(identifier=data.doi, id_type='doi', view="FULL", refresh=True)
                n_scopus += 1
                output_line = data.to_output(delimiter) + delimiter + scopus_abstract.eid
            except:
                output_line = data.to_output(delimiter) + delimiter + ""
            file_output.write("%s\n" % output_line)
            data_line = "\"" + line + "\"" + delimiter + 'true'
        else:
            file_output.write(("\"" + line + "\"" + ";;;;;;;;;;;;;\n"))
            data_line = "\"" + line + "\"" + delimiter + 'false'
        file_data.write("%s\n" % data_line)
    file_data.close()
    file_output.close()
    return "finished"
