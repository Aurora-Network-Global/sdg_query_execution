import csv

from flask import current_app as app


def load_facettes_list(project_id, facettes_type='keyword'):
    """loads the list of facettes from file"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = location + '/out/' + project_id + '/' + facettes_type + '_facettes.txt'
    with open(path_to_file, 'r', encoding='utf-8-sig') as f:
        strings = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in strings]


def save_facettes_list(project_id, facettes, facettes_type='keyword'):
    """takes a list of keywords, journals or somehting similar and writes it as 'XXX_facettes.txt'. the value of
    XXX can be provided as paramter 'facettes_type' and is keyword by default."""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = location + '/out/' + project_id + '/'
    with open(out_dir + facettes_type + '_facettes.txt', 'w', encoding='utf-8') as list_file:
        for facette in facettes:
            list_file.write(facette + '\n')
        list_file.close()


def generate_lists(project_id):
    """takes a scopus facettes export and extracts the two columns for the most common journals and the moste common
    keywords. writes the list to the two files 'keywords_facettes.txt and journal_facettes.txt"""
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    journal_facettes = []
    keyword_facettes = []
    with open(location + '/out/' + project_id + '/' + 'facettes.csv', 'r',  encoding='utf-8-sig') as csvfile:
        linereader = csv.reader(csvfile, delimiter=',')
        for row in linereader:
            if row.__len__() < 16:
                continue
            # skip header line
            if row[12] == 'SOURCE TITLE':
                continue
            # skip empty data
            if row[12] is not '':
                journal_facettes.append(row[12])
            if row[14] is not '':
                keyword_facettes.append(row[14])
        csvfile.close()
    save_facettes_list(project_id, keyword_facettes)
    save_facettes_list(project_id, journal_facettes, 'journal')
