import os
import requests
import lxml
import re
import xml.etree.ElementTree as ET
import json

from scopus.utils import get_content, get_encoded_text, ns

SCOPUS_XML_DIR = os.path.expanduser('~/.scopus/xml')
SCOPUS_ISSN_DIR = os.path.expanduser('~/.scopus/issn')

doi_regex = "10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![\"&\'])\S)+"

if not os.path.exists(SCOPUS_XML_DIR):
    os.makedirs(SCOPUS_XML_DIR)

if not os.path.exists(SCOPUS_ISSN_DIR):
    os.makedirs(SCOPUS_ISSN_DIR)


class ScopusAbstract(object):
    @property
    def abstract(self):
        """Return the abstract of an article."""
        return self._abstract

    @property
    def affiliations(self):
        """A list of scopus_api._ScopusAffiliation objects."""
        return self._affiliations

    @property
    def aggregationType(self):
        """Type of source the abstract is published in."""
        return self._aggregationType

    @property
    def article_number(self):
        """Article number."""
        return self._article_number

    @property
    def authkeywords(self):
        """Return the keywords of the abstract.
        Note: This may be empty.
        """
        return self._authkeywords

    @property
    def authors(self):
        """A list of scopus_api._ScopusAuthor objects."""
        return self._authors

    @property
    def citationLanguage(self):
        """Language of the article."""
        try:
            return self.items.find(
                'bibrecord/head/citation-info/citation-language').get("language")
        except:
            return None

    @property
    def citationType(self):
        """Type (short version) of the article."""
        try:
            return self.items.find(
                'bibrecord/head/citation-info/citation-type').get("code")
        except:
            return None

    @property
    def citedby_count(self):
        """Number of articles citing the abstract."""
        return self._citedby_count

    @property
    def citedby_url(self):
        """URL to Scopus page listing citing papers."""
        return self._citedby_url

    @property
    def coverDate(self):
        """The date of the cover the abstract is in."""
        return self._coverDate

    @property
    def description(self):
        """Return the description of a record.
        Note: If this is empty, try the abstract instead.
        """
        return self._description

    @property
    def doi(self):
        """DOI of article."""
        return self._doi

    @property
    def eid(self):
        """EID """
        return self._eid

    @property
    def endingPage(self):
        """Ending page."""
        return self._endingPage

    @property
    def issn(self):
        """ISSN of the publisher.
        Note: If E-ISSN is known to Scopus, this returns both
        ISSN and E-ISSN in random order separated by blank space.
        """
        return self._issn

    @property
    def issueIdentifier(self):
        """Issue number for abstract."""
        return self._issueIdentifier

    @property
    def nauthors(self):
        """Return number of authors listed in the abstract."""
        return len(self.authors)

    @property
    def pageRange(self):
        """Page range."""
        return self._pageRange

    @property
    def publicationName(self):
        """Name of source the abstract is published in."""
        return self._publicationName

    @property
    def publisher(self):
        """Name of the publisher of the abstract."""
        return self._publisher

    @property
    def refcount(self):
        """Number of references of an article.
        Note: Requires the FULL view of the article.
        """
        refs = self.items.find('bibrecord/tail/bibliography', ns)
        try:
            return refs.attrib['refcount']
        except AttributeError:  # refs is None
            return None

    @property
    def references(self):
        """Return EIDs of references of an article.
        Note: Requires the FULL view of the article.
        """
        return self._references

    @property
    def source_id(self):
        """Scopus source_id of the abstract."""
        return self._source_id

    @property
    def srctype(self):
        """Type (short version) of source the abstract is published in."""
        return self._srctype

    @property
    def startingPage(self):
        """Starting page."""
        return self._startingPage

    @property
    def subjectAreas(self):
        """List of subject areas of article.
        Note: Requires the FULL view of the article.
        """
        return self._subjectAreas

    @property
    def scopus_url(self):
        """URL to the abstract page on Scopus."""
        return self._scopus_url


    def title(self):
        """Abstract title."""
        return self._title

    @property
    def url(self):
        """URL to the API view of the abstract."""
        return self._url

    @property
    def volume(self):
        """Volume for the abstract."""
        return self._volume

    @property
    def website(self):
        """Website of article."""
        return self._website

    def __init__(self, ID, view='META_ABS', refresh=False):
        """Class to represent the results from a Scopus abstract.

        Parameters
        ----------
        ID : str
            The Scopus ID (EID) of an abstract or the DOI of the publication.

        view : str (optional, default=META_ABS)
            The view of the file that should be downloaded.  Will not take
            effect for already cached files. Supported values: META, META_ABS,
            FULL, where FULL includes all information of META_ABS view and
            META_ABS includes all information of the META view .  See
            https://dev.elsevier.com/guides/AbstractRetrievalViews.htm
            for details.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Notes
        -----
        The files are cached in ~/.scopus/xml/{id}.
        """
        allowed_views = ('META', 'META_ABS', 'FULL')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))

        # Get file content
        qfile = os.path.join(SCOPUS_XML_DIR, ID)
        url = "https://api.elsevier.com/content/abstract/" + "eid/{}".format(ID)

        params = {'view': view}
        self.xml = ET.fromstring(get_content(qfile, url=url, refresh=refresh,
                                             params=params))
        # Remove default namespace if present
        remove = u'{http://www.elsevier.com/xml/svapi/abstract/dtd}'
        nsl = len(remove)
        for elem in self.xml.getiterator():
            if elem.tag.startswith(remove):
                elem.tag = elem.tag[nsl:]

        if self.xml.tag == 'service-error':
            raise Exception('\n{0}\n{1}'.format(ID, self.xml))

        self.coredata = self.xml.find('coredata', ns)
        self.items = self.xml.find('item', ns)
        self._title = get_encoded_text(self.coredata, 'dc:title')
        self._abstract = get_encoded_text(self.coredata, 'dc:description/abstract/ce:para')
        self._citedby_count = int(get_encoded_text(self.coredata, 'citedby-count'))
        self._website = get_encoded_text(self.items, 'bibrecord/head/source/website/ce:e-address')
        self._volume = get_encoded_text(self.coredata, 'prism:volume')
        self._url = get_encoded_text(self.coredata, 'prism:url')
        self._startingPage = get_encoded_text(self.coredata, 'prism:startingPage')
        self._srctype = get_encoded_text(self.coredata, 'srctype')
        self._source_id = get_encoded_text(self.coredata, 'source-id')
        self._publisher = get_encoded_text(self.coredata, 'dc:publisher')
        self._publicationName = get_encoded_text(self.coredata, 'prism:publicationName')
        self._pageRange = get_encoded_text(self.coredata, 'prism:pageRange')
        self._issueIdentifier = get_encoded_text(self.coredata, 'prism:issueIdentifier')
        self._issn = get_encoded_text(self.coredata, 'prism:issn')
        self._endingPage = get_encoded_text(self.coredata, 'prism:endingPage')
        self._eid = get_encoded_text(self.coredata, 'eid')
        self._doi = get_encoded_text(self.coredata, 'prism:doi')
        self._description = get_encoded_text(self.coredata, 'dc:description')
        self._coverDate = get_encoded_text(self.coredata, 'prism:coverDate')
        self._article_number = get_encoded_text(self.coredata, 'article-number')
        self._aggregationType = get_encoded_text(self.coredata, 'prism:aggregationType')
        refs = self.items.find('bibrecord/tail/bibliography', ns)
        if refs is not None:
            eids = [r.find("ref-info/refd-itemidlist/itemid", ns).text for r
                    in refs.findall("reference", ns)]
            self._references = ["2-s2.0-" + eid for eid in eids]
        else:
            self._references = None
        scopus_url = self.coredata.find('link[@rel="scopus"]', ns)
        try:
            self._scopus_url = scopus_url.get('href')
        except AttributeError:  # scopus_url is None
            self._scopus_url = None
        subjectAreas = self.xml.find('subject-areas', ns)
        try:
            self._subjectAreas =  [a.text for a in subjectAreas]
        except:
            self._subjectAreas = None
        cite_link = self.coredata.find('link[@rel="scopus-citedby"]', ns)
        try:
            self._citedby_url = cite_link.get('href')
        except AttributeError:  # cite_link is None
            self._citedby_url = None
        authors = self.xml.find('authors', ns)
        try:
            self._authors = [_ScopusAuthor(author) for author in authors]
        except TypeError:
            self._authors = None
        try:
            self._authkeywords = [a.text for a in self.xml.find('authkeywords', ns)]
        except:
            self._authkeywords = None
        self._affiliations = [_ScopusAffiliation(aff) for aff in
            self.xml.findall('affiliation', ns)]

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['xml']
        del state['coredata']
        del state['items']
        return state


    def get_corresponding_author_info(self):
        """Try to get corresponding author information.

        Returns (scopus-id, name, email).
        """
        resp = requests.get(self.scopus_url)
        from lxml import html

        parsed_doc = html.fromstring(resp.content)
        for div in parsed_doc.body.xpath('.//div'):
            for a in div.xpath('a'):
                if '/cdn-cgi/l/email-protection' not in a.get('href', ''):
                    continue
                encoded_text = a.attrib['href'].replace('/cdn-cgi/l/email-protection#', '')
                key = int(encoded_text[0:2], 16)
                email = ''.join([chr(int('0x{}'.format(x), 16) ^ key)
                                 for x in
                                 map(''.join, zip(*[iter(encoded_text[2:])]*2))])
                for aa in div.xpath('a'):
                    if 'http://www.scopus.com/authid/detail.url' in aa.get('href', ''):
                        scopus_url = aa.attrib['href']
                        name = aa.text
                    else:
                        scopus_url, name = None, None

        return (scopus_url, name, email)

    def __str__(self):
        """Return pretty text version of the abstract.

        Assumes the abstract is a journal article and was loaded with
        view="META_ABS" or view="FULL".
        """

        if len(self.authors) > 1:
            authors = ', '.join([str(a.initials) +
                                 ' ' +
                                 str(a.surname)
                                 for a in self.authors[0:-1]])
            authors += (' and ' +
                        str(self.authors[-1].initials) +
                        ' ' + str(self.authors[-1].surname))
        else:
            a = self.authors[0]
            authors = str(a.given_name) + ' ' + str(a.surname)

        s = '[[{self.scopus_url}][{self.eid}]]  '
        s += '{authors}, {self.title}, {self.publicationName}, '
        s += '{self.volume}'
        if self.issueIdentifier:
            s += '({self.issueIdentifier}), '
        else:
            s += ', '
        if self.pageRange:
            s += 'p. {self.pageRange}, '
        elif self.startingPage:
            s += 'p. {self.startingPage}, '
        elif self.article_number:
            s += 'Art. No. {self.article_number} '
        else:
            s += '(no pages found) '

        from dateutil.parser import parse
        pubDate = parse(self.coverDate)

        s += '({}).'.format(pubDate.year)
        s += ' https://doi.org/{self.doi},'
        s += ' {self.scopus_url},'
        s += ' cited {self.citedby_count} times (Scopus).\n'
        s += '  Affiliations:\n   '
        s += '\n   '.join([str(aff) for aff in self.affiliations])

        return s.format(authors=authors,
                        self=self)

    @property
    def latex(self):
        """Return LaTeX representation of the abstract."""
        s = ('{authors}, \\textit{{{title}}}, {journal}, {volissue}, '
             '{pages}, ({date}). {doi}, {scopus_url}.')
        if len(self.authors) > 1:
            authors = ', '.join([str(a.given_name) +
                                 ' ' + str(a.surname)
                                 for a in self.authors[0:-1]])
            authors += (' and ' +
                        str(self.authors[-1].given_name) +
                        ' ' + str(self.authors[-1].surname))
        else:
            a = self.authors[0]
            authors = str(a.given_name) + ' ' + str(a.surname)
        title = self.title
        journal = self.publicationName
        volume = self.volume
        issue = self.issueIdentifier
        if volume and issue:
            volissue = '\\textbf{{{0}({1})}}'.format(volume, issue)
        elif volume:
            volissue = '\\textbf{{0}}'.format(volume)
        else:
            volissue = 'no volume'
        date = self.coverDate
        if self.pageRange:
            pages = 'p. {0}'.format(self.pageRange)
        elif self.startingPage:
            pages = 'p. {self.startingPage}'.format(self)
        elif self.article_number:
            pages = 'Art. No. {self.article_number}, '.format(self)
        else:
            pages = '(no pages found)'
        doi = '\\href{{https://doi.org/{0}}}{{doi:{0}}}'.format(self.doi)
        scopus_url = '\href{{{0}}}{{scopus:{1}}}'.format(self.scopus_url,
                                                         self.eid)

        return s.format(**locals())

    @property
    def html(self):
        """Returns an HTML citation."""
        s = (u'{authors}, {title}, {journal}, {volissue}, {pages}, '
             '({date}). {doi}.')

        au_link = ('<a href="https://www.scopus.com/authid/detail.url'
                   '?origin=AuthorProfile&authorId={0}">{1}</a>')

        if len(self.authors) > 1:
            authors = u', '.join([au_link.format(a.auid,
                                                (str(a.given_name) +
                                                 ' ' + str(a.surname)))
                                 for a in self.authors[0:-1]])
            authors += (u' and ' +
                        au_link.format(self.authors[-1].auid,
                                       (str(self.authors[-1].given_name) +
                                        ' ' +
                                        str(self.authors[-1].surname))))
        else:
            a = self.authors[0]
            authors = au_link.format(a.auid,
                                     str(a.given_name) + ' ' + str(a.surname))

        title = u'<a href="{link}">{title}</a>'.format(link=self.scopus_url,
                                                      title=self.title)

        jname = self.publicationName
        sid = self.source_id
        jlink = ('<a href="https://www.scopus.com/source/sourceInfo.url'
                 '?sourceId={sid}">{journal}</a>')
        journal = jlink.format(sid=sid, journal=jname)

        volume = self.volume
        issue = self.issueIdentifier
        if volume and issue:
            volissue = u'<b>{0}({1})</b>'.format(volume, issue)
        elif volume:
            volissue = u'<b>{0}</b>'.format(volume)
        else:
            volissue = 'no volume'
        date = self.coverDate
        if self.pageRange:
            pages = u'p. {0}'.format(self.pageRange)
        elif self.startingPage:
            pages = u'p. {self.startingPage}'.format(self=self)
        elif self.article_number:
            pages = u'Art. No. {self.article_number}, '.format(self=self)
        else:
            pages = '(no pages found)'
        doi = '<a href="https://doi.org/{0}">doi:{0}</a>'.format(self.doi)

        html = s.format(**locals())
        return html.replace('None', '')

    @property
    def bibtex(self):
        """Bibliographic entry in BibTeX format.

        Returns
        -------
        bibtex : str
            A string representing a bibtex entry for the item.

        Raises
        ------
        ValueError : If the item's aggregationType is not Journal.
        """
        if self.aggregationType != 'Journal':
            raise ValueError('Only Journal articles supported.')
        template = u'''@article{{{key},
  author = {{{author}}},
  title = {{{title}}},
  journal = {{{journal}}},
  year = {{{year}}},
  volume = {{{volume}}},
  number = {{{number}}},
  pages = {{{pages}}},
  doi = {{{doi}}}
}}

'''
        if self.pageRange:
            pages = self.pageRange
        elif self.startingPage:
            pages = self.startingPage
        elif self.article_number:
            pages = self.article_number
        else:
            pages = 'no pages found'
        year = self.coverDate[0:4]
        first = self.title.split()[0].title()
        last = self.title.split()[-1].title()
        key = ''.join([self.authors[0].surname, year, first, last])
        authors = ' and '.join(["{} {}".format(a.given_name, a.surname)
                                for a in self.authors])
        bibtex = template.format(
            key=key, author=authors, title=self.title,
            journal=self.publicationName, year=year, volume=self.volume,
            number=self.issueIdentifier, pages=pages, doi=self.doi)
        return bibtex

    @property
    def ris(self):
        """Bibliographic entry in RIS (Research Information System Format)
        format.

        Returns
        -------
        ris : str
            The RIS string representing an item.

        Raises
        ------
        ValueError : If the item's aggregationType is not Journal.
        """
        if self.aggregationType != 'Journal':
            raise ValueError('Only Journal articles supported.')
        template = u'''TY  - JOUR
TI  - {title}
JO  - {journal}
VL  - {volume}
DA  - {date}
SP  - {pages}
PY  - {year}
DO  - {doi}
UR  - https://doi.org/{doi}
'''
        ris = template.format(
            title=self.title, journal=self.publicationName,
            volume=self.volume, date=self.coverDate, pages=self.pageRange,
            year=self.coverDate[0:4], doi=self.doi)
        for au in self.authors:
            ris += 'AU  - {}\n'.format(au.indexed_name)
        if self.issueIdentifier is not None:
            ris += 'IS  - {}\n'.format(self.issueIdentifier)
        ris += 'ER  - \n\n'
        return ris


class _ScopusAuthor(object):
    """An internal class for a author in a ScopusAbstract."""
    def __init__(self, author):
        """author should be an xml element.
        The following attributes are supported:

        author
        indexed_name
        given_name
        surname
        initials
        author_url - the scopus api url to get more information
        auid - the scopus id for the author
        scopusid - the scopus id for the author
        seq - the index of the author in the author list.
        affiliations - a list of ScopusAuthorAffiliation objects

        This class is not the same as the one in scopus.scopus_author, which
        uses the scopus author api.

        """
        self.author = author
        self.indexed_name = get_encoded_text(author, 'ce:indexed-name')
        self.given_name = get_encoded_text(author, 'ce:given-name')
        self.surname = get_encoded_text(author, 'ce:surname')
        self.initials = get_encoded_text(author, 'ce:initials')
        self.author_url = get_encoded_text(author, 'author-url')
        self.auid = author.attrib.get('auid')
        self.scopusid = self.auid
        self.seq = author.attrib.get('seq')
        self.affiliations = [_ScopusAuthorAffiliation(aff)
                             for aff in author.findall('affiliation', ns)]

    def __str__(self):
        s = """{0.seq}. {0.given_name} {0.surname} scopusid:{0.auid} """
        s += ' '.join([str(aff) for aff in self.affiliations])
        return s.format(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['author']
        return state


class _ScopusAffiliation(object):
    """Internal class to represent the affiliations in an Abstract."""
    def __init__(self, affiliation):
        """affiliation should be an xml element from the main abstract"""
        self.affiliation = affiliation
        self.affilname = get_encoded_text(affiliation, 'affilname')
        self.city = get_encoded_text(affiliation, 'affiliation-city')
        self.country = get_encoded_text(affiliation, 'affiliation-country')
        self.href = affiliation.attrib.get('href', None)
        self.id = affiliation.attrib.get('id', None)

    def __str__(self):
        return 'id:{0.id} {0.affilname}'.format(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['affiliation']
        return state


class _ScopusAuthorAffiliation(object):
    """Internal class to represent the affiliation in an Author element"""
    def __init__(self, affiliation):
        """affiliation should be an xml element from an Author element."""
        self.affiliation = affiliation
        self.id = affiliation.get('id', None)
        self.href = affiliation.get('href', None)

    def __str__(self):
        return 'affiliation_id:{0.id}'.format(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['affiliation']
        return state


class ScopusJournal(object):
    """Class to represent a journal from the Scopus API."""

    def __init__(self, ISSN, refresh=False):
        ISSN = str(ISSN)
        self.issn = ISSN

        qfile = os.path.join(SCOPUS_ISSN_DIR, ISSN)
        url = ("https://api.elsevier.com/content/serial/title/issn:" + ISSN)
        self.xml = ET.fromstring(get_content(qfile, refresh, url))

        self.publisher = get_encoded_text(self.xml, 'entry/dc:publisher')
        self.title = get_encoded_text(self.xml, 'entry/dc:title')
        self.aggregationType = get_encoded_text(self.xml,
                                                'entry/prism:aggregationType')
        self.prism_url = get_encoded_text(self.xml, 'entry/prism:url')

        # Impact factors
        SNIP = get_encoded_text(self.xml, 'entry/SNIPList/SNIP')
        SNIP_year = self.xml.find('entry/SNIPList/SNIP', ns)
        if SNIP_year is not None:
            SNIP_year = SNIP_year.get('year')
        else:
            SNIP_year = -1

        IPP = get_encoded_text(self.xml, 'entry/IPPList/IPP')
        IPP_year = self.xml.find('entry/IPPList/IPP', ns)
        if IPP_year is not None:
            IPP_year = IPP_year.get('year')
        else:
            IPP_year = -1

        SJR = get_encoded_text(self.xml, 'entry/SJRList/SJR')
        SJR_year = self.xml.find('entry/SJRList/SJR', ns)
        if SJR_year is not None:
            SJR_year = SJR_year.get('year')
        else:
            SJR_year = -1
        if SNIP:
            self.SNIP = float(SNIP)
            self.SNIP_year = int(SNIP_year)
        else:
            self.SNIP = None
            self.SNIP_year = None

        if IPP:
            self.IPP = float(IPP)
            self.IPP_year = int(IPP_year)
        else:
            self.IPP = None
            self.IPP_year = None

        if SJR:
            self.SJR = float(SJR)
            self.SJR_year = int(SJR_year)
        else:
            self.SJR = None
            self.SJR_year = None

        scopus_url = self.xml.find('entry/link[@ref="scopus-source"]')
        if scopus_url is not None:
            self.scopus_url = scopus_url.attrib['href']
        else:
            self.scopus_url = None

        homepage = self.xml.find('entry/link[@ref="homepage"]')
        if homepage is not None:
            self.homepage = homepage.attrib['href']
        else:
            self.homepage = None

    def __str__(self):
        s = """{self.title} {self.scopus_url}
    Homepage: {self.homepage}
    SJR:  {self.SJR} ({self.SJR_year})
    SNIP: {self.SNIP} ({self.SNIP_year})
    IPP:  {self.IPP} ({self.IPP_year})
""".format(self=self)
        return s

    @property
    def org(self):
        """Return an org-formatted string for a Journal."""
        s = """[[{self.scopus_url}][{self.title}]] [[{self.homepage}][homepage]]
| SJR | SNIP | IPP |
| {self.SJR} | {self.SNIP} | {self.IPP} |""".format(self=self)
        return s

    def __getstate__(self):
        state = self.__dict__.copy()
        return state



