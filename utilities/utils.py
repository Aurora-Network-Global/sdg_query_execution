

# read in the JSON-data from the request and convert them to a scopus query string
# (one could add alternative query targets here, for example transforming the individual query strings to a WoS-Search
import numpy as np

from model.KeywordFrequency import KeywordFrequency
from service import eids_service


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
        affil_search = '(AF-ID(' + search["affiliation_id"] + '))'
        affil_search = affil_search.replace(" OR ", ") OR AF-ID(")
        affil_search = affil_search.replace(" AND ", ") AND AF-ID(")
        search_string += affil_search
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
        affil_search = 'AF-ID(' + search["affiliation_id"] + ')'
        affil_search = affil_search.replace(" OR ", ") OR AF-ID(")
        affil_search = affil_search.replace(" AND ", ") AND AF-ID(")
        search_string += affil_search
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


def calculate_symmetric_overlap(primary):
    primary_length = len(primary)
    overlap_map = np.empty((primary_length, primary_length), dtype=object)
    data = {}
    for key in primary:
        data[key] = eids_service.load_eid_list(key, '')
    for i in range(0, primary_length):
        for entry in data[primary[i]]:
            found = False
            for j in range(i + 1, primary_length):
                if entry in data[primary[j]]:
                    if overlap_map[i, j] is None:
                        overlap_map[i, j] = [entry]
                        overlap_map[j, i] = [entry]
                    else:
                        overlap_map[i, j].append(entry)
                        overlap_map[j, i].append(entry)
                    found = True
            if not found:
                if overlap_map[i, i] is None:
                    overlap_map[i, i] = [entry]
                else:
                    overlap_map[i, i].append(entry)
    return overlap_map


def calculate_asymmetric_overlap(primary, secondary):
    primary_length = primary.__len__()
    secondary_length = secondary.__len__()
    overlap_map = np.empty((primary_length, secondary_length), dtype=object)
    data = {}
    for key in primary:
        data[key] = eids_service.load_eid_list(key, '')
    for key in secondary:
        data[key] = eids_service.load_eid_list(key, '')
    for i in range(0, primary_length):
        for entry in data[primary[i]]:
            found = False
            for j in range(0, secondary):
                if j == i:
                    continue
                if entry in data[secondary[j]]:
                    if overlap_map[i, j] is None:
                        overlap_map[i, j] = [entry]
                    else:
                        overlap_map[i, j].append(entry)
                    found = True
            if not found:
                if overlap_map[i, i] is None:
                    overlap_map[i, i] = [entry]
                else:
                    overlap_map[i, i].append(entry)
    return overlap_map
