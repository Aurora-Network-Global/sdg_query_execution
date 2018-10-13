

# read in the JSON-data from the request and convert them to a scopus query string
# (one could add alternative query targets here, for example transforming the individual query strings to a WoS-Search
def convert_search_to_scopus_search_string(search):
    search_string = ""
    if search["author_name"]:
        if search_string != "":
            search_string += " AND "
        search_string += "AUTH(" + search["author_name"] + ")"
    if search["topic"]:
        if search_string != "":
            search_string += " AND "
        search_string += "TITLE-ABS-KEY(" + search["topic"] + ")"
    if search["year"]:
        if search_string != "":
            search_string += " AND "
        search_string += "PUBYEAR(" + search["year"] + ")"
    if search["title"]:
        if search_string != "":
            search_string += " AND "
        search_string += "TITLE(" + search["title"] + ")"
    if search["subject"]:
        if search_string != "":
            search_string += " AND "
        search_string += "SUBJAREA(" + search["subject"] + ")"
    if search["author_id"]:
        if search_string != "":
            search_string += " AND "
        search_string += "AU-ID(" + search["author_id"] + ")"
    if search["affiliation_id"]:
        if search_string != "":
            search_string += " AND "
        search_string += 'AF-ID(' + search["affiliation_id"] + ')'
    return search_string


# TO DO: apply Altmeric search fields to procedure. Up to now only copy of Scopus procedure.
def convert_search_to_altmetric_seach_string(search):
    search_string = ""
    if search["author_name"]:
        if search_string != "":
            search_string += " AND "
        search_string += "AUTH(" + search["author_name"] + ")"
    if search["topic"]:
        if search_string != "":
            search_string += " AND "
        search_string += "TITLE-ABS-KEY(" + search["topic"] + ")"
    if search["year"]:
        if search_string != "":
            search_string += " AND "
        search_string += "PUBYEAR(" + search["year"] + ")"
    if search["title"]:
        if search_string != "":
            search_string += " AND "
        search_string += "TITLE(" + search["title"] + ")"
    if search["subject"]:
        if search_string != "":
            search_string += " AND "
        search_string += "SUBJAREA(" + search["subject"] + ")"
    if search["author_id"]:
        if search_string != "":
            search_string += " AND "
        search_string += "AU-ID(" + search["author_id"] + ")"
    if search["affiliation_id"]:
        if search_string != "":
            search_string += " AND "
        search_string += 'AF-ID(' + search["affiliation_id"] + ')'
    return search_string
