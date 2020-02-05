from nltk.corpus import stopwords


def replace_index_by_clear_name(list_of_indices, clear_names):
    for index, value in enumerate(list_of_indices):
        list_of_indices[index] = clear_names[index]


def get_survey_results_from_row(row):
    unselected_journals = []
    selected_journals = []
    judgements = []
    unselected_keywords = []
    selected_keywords = []
    session = ''
    suggested_keywords = []
    suggested_journals = []
    glossaries_suggested = []
    if row is not None:
        session = row[9]
        for i in range(29, 128):
            judgements.append({'eid': row[100 + i], 'judgement': ('Yes' in row[i])})
        for i in range(227, 326):
            if row[i] is '':
                unselected_keywords.append(i - 226)
            else:
                selected_keywords.append(i - 226)
        suggested_keywords = row[328].split('\n')
        clean_tokens = suggested_keywords[:]
        for token in suggested_keywords:
            if token in stopwords.words('english'):
                clean_tokens.remove(token)
        suggested_journals = row[435].split('\n')
        for i in range(334, 433):
            if row[i] is '':
                unselected_journals.append(i - 333)
            else:
                selected_journals.append(i - 333)
