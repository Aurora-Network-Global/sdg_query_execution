

# read in the JSON-data from the request and convert them to a scopus query string
# (one could add alternative query targets here, for example transforming the individual query strings to a WoS-Search
from model.KeywordFrequency import KeywordFrequency


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
    if search["start_year"]:
        if search_string != "":
            search_string += " AND "
        search_string += "PUBYEAR AFT " + search["start_year"] + ""
    if search["end_year"]:
        if search_string != "":
            search_string += " AND "
        search_string += "PUBYEAR BEF " + search["end_year"] + ""

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


# Given a list of words, return a dictionary of
# word-frequency pairs.
# THANKS TO William J. Turkel and Adam Crymble (https://programminghistorian.org/en/lessons/counting-frequencies)
def wordlist_to_freq_dict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist, wordfreq))


# Sort a dictionary of word-frequency pairs in
# order of descending frequency.
# THANKS TO William J. Turkel and Adam Crymble (https://programminghistorian.org/en/lessons/counting-frequencies)
def sort_freq_dict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    list_of_frequencies = []
    for keyword_freq in aux:
        list_of_frequencies.append(KeywordFrequency(keyword_freq[1], keyword_freq[0]))
    return list_of_frequencies


