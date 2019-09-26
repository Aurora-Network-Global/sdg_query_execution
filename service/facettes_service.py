import csv
import os

from flask import current_app as app

def load_facettes_list(query_id, facettes_type='keyword'):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    # path to the file
    path_to_file = location + '/out/' + query_id + '/' + facettes_type + '_facettes.txt'
    with open(path_to_file, 'r', encoding='utf-8-sig') as f:
        strings = f.readlines()
        f.close()
        # remove whitespace characters like `\n` at the end of each line
    return [x.strip() for x in strings]


def save_facettes_list(query_id, facettes, facettes_type='keyword'):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = location + '/out/' + query_id + '/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + facettes_type + '_facettes.txt', 'w', encoding='utf-8') as list_file:
        for facette in facettes:
            list_file.write(facette + '\n')
        list_file.close()

def generate_lists(query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    journal_facettes = []
    keyword_facettes = []
    with open(location + '/out/' + query_id + '/' + 'facettes.csv', 'r', encoding='utf-8-sig') as csvfile:
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
    save_facettes_list(query_id, keyword_facettes)
    save_facettes_list(query_id, journal_facettes, 'journal')

