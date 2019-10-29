import re

import requests
from flask import current_app as app

from model.Author import Author


class CrossRefSearch:

    @property
    def doi(self):
        return self._doi


    def __init__(self, reference):
        with app.app_context():
            email = app.config.get("LIBINTEL_USER_EMAIL")
        self._crossref_url = "https://api.crossref.org/"
        self._reference = cleanup(reference)
        r = requests.get(self._crossref_url + "works?mailto=" + email + "&rows=1&query=" + self._reference.replace(" ", "+"))
        if r.status_code == 200:
            crossref_data = r.json()
            status = crossref_data["status"]
            if status == "ok":
                self._data = crossref_data["message"]["items"][0]
                try:
                    self._title = self._data["title"][0]
                except KeyError:
                    self._title = ""
                    print("no title given")
                authors = []
                try:
                    for author in self._data["author"]:
                        author_object = Author()
                        try:
                            author_object.surname = author["family"]
                        except KeyError:
                            print("no family name")
                        try:
                            author_object.firstname = author["given"]
                        except KeyError:
                            print("no given name")
                        try:
                            author_object.affiliation = author["affiliation"]
                        except IndexError:
                            print("no affiliation given")
                        authors.append(author_object)
                except KeyError:
                    print('no authors given')
                    authors.append(Author())
                self._authors = authors
                try:
                    self._doi = self._data["DOI"]
                except KeyError:
                    self._doi = ""
                    print("no doi given")
                try:
                    self._cited_by = self._data["is-referenced-by-count"]
                except KeyError:
                    self._cited_by = 0
                    print("no cited-by given")
                try:
                    self._score = self._data["score"]
                except KeyError:
                    self._score = 0
                    print("no score given")
                self._print_issn = ""
                self._electronic_issn = ""
                try:
                    for issn in self._data["issn-type"]:
                        if issn["type"] == "print":
                            self._print_issn = issn["value"]
                        if issn["type"] == "electronic":
                            self._electronic_issn = issn["value"]
                except KeyError:
                    print("no ISSNs given")
            else:
                self._data = None

    def to_output(self, delimiter):
        string: str = "\"" + self._reference + "\""
        string += delimiter
        string += self._doi
        string += delimiter
        string += self._print_issn
        string += delimiter
        string += self._electronic_issn
        string += delimiter
        string += ("\"" + self._title.replace("\n", "") + "\"")
        string += delimiter
        string += str(self._score)
        string += delimiter
        string += str(self._cited_by)
        string += delimiter
        string += "\""
        for author in self._authors:
            string += author.to_output().replace("\n", "")
        string += "\""
        string += delimiter
        if self._reference.lower().__contains__("comment"):
            has_title = self._title.__contains__("comment")
        elif self._reference.lower().__contains__("erratum"):
            has_title = self._title.__contains__("erratum")
        else:
            has_title = self.reference_has()
        string += str(has_title)
        return string

    def reference_has(self) -> bool:
        return self._reference.lower().__contains__(re.sub("[^ a-zA-Z0-9]", "", self._title.lower()))
            

def cleanup(line):
    return re.sub("[^ a-zA-Z0-9]", "", line).replace("\n", "")
