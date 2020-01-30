class Author:

    @property
    def surname(self):
        return self._surname

    @property
    def firstname(self):
        return self._firstname

    @property
    def affiliation(self):
        return self._affiliation

    @property
    def identifier(self):
        return self._identifier

    @firstname.setter
    def firstname(self, firstname):
        self._firstname = firstname

    @affiliation.setter
    def affiliation(self, affiliation):
        self._affiliation = affiliation

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    def __init__(self, surname, firstname='', affiliation=None, identifier=None):
        self._surname = surname
        self._firstname = firstname
        if affiliation is not None:
            self._affiliation = affiliation
        else:
            self._affiliation = []
        if identifier is not None:
            self._identifier = identifier
        else:
            self._identifier = []

    def to_output(self):
        string = self._surname + "," + self._firstname + " ("
        try:
            for affil in self._affiliation:
                string += affil["name"].replace(";", " ")
                string += ", "
        except:
            print("no affiliation given")
        string += "), "
        return string
