import json
import os
import re

from xml.etree import ElementTree as element_tree

import lxml.etree as etree

from flask import current_app as app

from query.QueryFilters import QueryFilters
from query.Query import Query
from query.QueryDefinitions import QueryDefinitions
from query.QueryDefintion import QueryDefinition
from query.QueryFilter import QueryFilter
from query.QueryLine import QueryLine
from query.Timerange import Timerange
from utilities.QueryConverter import QueryConverter

namespaces = {'dc': 'http://dublincore.org/documents/dcmi-namespace/',
              'aqd': 'http://aurora-network.global/queries/namespace/'}


def import_old_query(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = location + '/out/' + project_id + '/query.json'
    with open(path_to_file) as json_file:
        query_old = json.load(json_file)
        json_file.close()
        query = convert(query_old)
        return query


def convert(query_old):
    timerange = Timerange(start=query_old['start_year'], end=query_old['end_year'], field='PUBYEAR')
    query_filters = QueryFilters(timerange=timerange)
    if query_old['affiliation_id'] != '':
        affiliation_filter = QueryFilter(filter_field='AF-ID', filter_term=query_old['affiliation_id'],
                                         filter_type='affiliation')
        query_filters.add_filter(affiliation_filter)

    if query_old['author_name'] != '':
        person_name_filter = QueryFilter(filter_field='AUTH', filter_term=query_old['author_name'])
        query_filters.add_filter(person_name_filter)
    if query_old['subject'] != '':
        subject_filter = QueryFilter(filter_field='SUBJAREA', filter_term=query_old['subject'])
        query_filters.add_filter(subject_filter)

    query_lines = [QueryLine(field='TITLE-ABS-KEY', query_line=query_old['topic'])]
    if query_old['author_id'] != '':
        person_id_search = QueryLine(field='AU-ID', query_line=query_old['author_id'])
        query_lines.append(person_id_search)
    query_definition = QueryDefinition(query_lines=query_lines, identifier='1')
    query_definitions = QueryDefinitions(query_filters=query_filters, query_definition=[query_definition])
    query = Query(title=query_old['title'], query_definitions=query_definitions)
    return query


def save_scopus_queries(project_id, scopus_queries):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = '{}/out/{}/scopus_queries.json'.format(location, project_id)
    with open(path_to_file, 'w', encoding='utf-8') as scopus_queries_file:
        scopus_queries_file.write(json.dumps(scopus_queries, default=lambda o: o.__getstate__()))
        scopus_queries_file.close()


def create_scopus_queries(project_id, query):
    query_converter = QueryConverter(query=query)
    save_scopus_queries(project_id,  query_converter.scopus_queries)


def load_scopus_queries(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = '{}/out/{}/query.xml'.format(location, project_id)
    query = load_xml_query_from_disc(path_to_file)
    query_converter = QueryConverter(query=query)
    save_scopus_queries(project_id, query_converter.scopus_queries)
    return query_converter.scopus_queries


def load_scopus_query_from_xml(project_id):
    query = load_query_from_xml(project_id)
    query_converter = QueryConverter(query)
    query_converter.calculate_scopus_queries()
    return query_converter.calculate_scopus_queries()


def get_field_value(element, field, namespace='aqd'):
    try:
        return re.sub(' +', ' ', element.find(namespace + ':' + field, namespaces).text.strip(' \t\n\r'))
    except:
        return ''


def get_attribute_value(element, attribute):
    try:
        return element.attrib[attribute].strip(' \t\n\r')
    except:
        return ''


def get_field_attribute_value(element, field, namespace='aqd'):
    try:
        return element.find(namespace + ':' + field, namespaces).attrib['field'].strip(' \t\n\r')
    except:
        return ''


def get_filter_from_element(filter_element):
    if filter_element is None:
        return None
    try:
        filter_timerange = filter_element.find('aqd:timerange', namespaces)
        timerange_object = Timerange(get_field_value(filter_timerange, 'start'),
                                     get_field_value(filter_timerange, 'end'),
                                     get_attribute_value(filter_timerange, 'field'))
    except KeyError:
        timerange_object = None
    filters = QueryFilters(timerange=timerange_object, query_filters=None)
    if filter_element.findall('aqd:filter', namespaces) is not None:
        for filter in filter_element.findall('aqd:filter', namespaces):
            filters.add_filter(QueryFilter(filter_field=filter.attrib['field'],
                                           filter_type=filter.attrib['type'],
                                           filter_term=re.sub(' +', ' ', filter.text)))
    return filters


def load_query_from_xml(project_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = '{}/out/{}/query.xml'.format(location, project_id)
    if not os.path.exists(path_to_file):
        raise FileNotFoundError('query xml file does not exist')
    return load_xml_query_from_disc(path_to_file)


def load_query(project_id, query_id):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path_to_file = '{}/out/{}/query.xml'.format(location, project_id, query_id)
    if not os.path.exists(path_to_file):
        raise FileNotFoundError('query xml file does not exist')
    return load_xml_query_from_disc(path_to_file)


def getIdentifier(query_xml):
    try:
        list_of_identifiers = query_xml.findall('dc:identifier', namespaces)
        if len(list_of_identifiers) == 1:
            return list_of_identifiers[0].text.strip(' \t\n\r')
        for identifier in list_of_identifiers:
            if identifier.attrib['type'] == 'sdg':
                return identifier.text.strip(' \t\n\r')
    except:
        return ''


def load_xml_query_from_disc(path_to_file):
    element_tree.register_namespace('aqd', namespaces['aqd'])
    element_tree.register_namespace('dc', namespaces['dc'])
    with open(path_to_file, 'r', encoding='utf-8') as xml_file:
        query_xml = element_tree.parse(xml_file).getroot()
        identifier = getIdentifier(query_xml)
        query = Query(identifier=identifier,
                      query_definitions=None,
                      title=get_field_value(query_xml, 'title', 'dc'),
                      description=get_field_value(query_xml, 'description', 'dc'),
                      creator=get_field_value(query_xml, 'creator', 'dc'),
                      contributor=get_field_value(query_xml, 'contributor', 'dc'),
                      licence=get_field_value(query_xml, 'licence', 'dc'),
                      licence_href=get_attribute_value(query_xml.find('dc:licence'), 'href'),
                      date_modified=get_field_value(query_xml, 'date-modified', 'dc'))
        query_definitions_xml = query_xml.find('aqd:query-definitions', namespaces)
        try:
            query_definitions_filter = get_filter_from_element(query_definitions_xml.find('aqd:filters', namespaces))
        except:
            query_definitions_filter = QueryFilter(Timerange(field='', start='', end=''), None)
        syntax = get_attribute_value(query_definitions_xml, 'syntax')
        if syntax == '':
            syntax = 'SCOPUS'
        query_definitions = QueryDefinitions(query_definition=None,
                                             query_filters=query_definitions_filter,
                                             syntax=get_attribute_value(query_definitions_xml, 'syntax')
                                             )
        for query_definition_xml in query_definitions_xml.findall('aqd:query-definition', namespaces):
            try:
                query_definition_identifier = get_field_value(query_definition_xml, 'subquery-identifier')

            except AttributeError:
                query_definition_identifier = "1"
            query_definition_descriptions = []
            try:
                for query_defintion_xml in query_definition_xml.find('aqd:subquery-descriptions', namespaces):
                    query_definition_descriptions.append(query_defintion_xml.text.strip(' \t\n\r'))
            except:
                print('no subquery descriptions')
            try:
                query_filters = get_filter_from_element(query_definition_xml.find('aqd:filter', namespaces))
            except:
                query_filters = None
            query_definition = QueryDefinition(identifier=query_definition_identifier,
                                               descriptions=query_definition_descriptions,
                                               query_filters=query_filters,
                                               query_lines=None)
            for query_line_xml in query_definition_xml.find('aqd:query-lines', namespaces):
                try:
                    query_line_field = get_attribute_value(query_line_xml, 'field')

                except KeyError:
                    query_line_field = ""
                try:
                    query_definition.add_query_line(QueryLine(query_line_field,
                                                              query_line_xml.text.strip(' \t\n\r')))
                except AttributeError:
                    query_definition.add_query_line((QueryLine(query_line_field, "")))
            query_definitions.add_query_definition(query_definition)
        query.query_definitions = query_definitions
    return query


def set_element_value(parent, name, value, namespace='aqd'):
    element = element_tree.SubElement(parent, namespace + ':' + name)
    element.text = re.sub(' +', ' ', value)


def set_filter_value(parent, name, value, field):
    element = element_tree.SubElement(parent, 'aqd:' + name)
    element.text = value
    element.attrib['field'] = field


def build_filter_element(filters_element, query_filters):
    if query_filters is not None:
        for filter in query_filters.query_filters:
            filter_element = element_tree.SubElement(filters_element, 'aqd:filter')
            filter_element.attrib['field'] = filter.filter_field
            filter_element.attrib['type'] = filter.filter_type
            filter_element.text = re.sub(' +', ' ', filter.filter_term)
        if query_filters.timerange is not None:
            timerange_element = element_tree.SubElement(filters_element, 'aqd:timerange')
            timerange_element.attrib['field'] = query_filters.timerange.field
            set_element_value(timerange_element, 'start', query_filters.timerange.start)
            set_element_value(timerange_element, 'end', query_filters.timerange.end)


def save_query_to_xml(project_id, query):
    element_tree.register_namespace('aqd', namespaces['aqd'])
    element_tree.register_namespace('dc', namespaces['dc'])
    query_element = element_tree.Element('aqd:query', namespaces)
    set_element_value(query_element, 'identifier', query.identifier, 'dc')
    set_element_value(query_element, 'title', query.title, 'dc')
    set_element_value(query_element, 'creator', query.creator, 'dc')
    set_element_value(query_element, 'contributor', query.contributor, 'dc')
    set_element_value(query_element, 'description', query.description, 'dc')
    set_element_value(query_element, 'date-modified', query.date_modified, 'dc')
    licence_element = element_tree.SubElement(query_element, 'dc:licence')
    licence_element.text = query.licence
    licence_element.attrib['href'] = query.licence_href
    query_defintions_element = element_tree.SubElement(query_element, 'aqd:query-definitions')
    filter_element = element_tree.SubElement(query_defintions_element, 'aqd:filters')
    build_filter_element(filter_element, query.query_definitions.query_filters)
    query_defintions_element.attrib['syntax'] = query.query_definitions.syntax
    for query_definition in query.query_definitions.query_definition:
        query_defintion_element = element_tree.SubElement(query_defintions_element, 'aqd:query-definition')
        set_element_value(query_defintion_element, 'subquery-identifier', query_definition.identifier)
        subquery_descriptions_element = element_tree.SubElement(query_defintion_element, 'aqd:subquery-descriptions')
        for subquery_description in query_definition.descriptions:
            set_element_value(subquery_descriptions_element, 'subquery-description', subquery_description)
        query_lines_element = element_tree.SubElement(query_defintion_element, 'aqd:query-lines')
        for query_line in query_definition.query_lines:
            query_line_element = element_tree.SubElement(query_lines_element, 'aqd:query-line')
            query_line_element.text = re.sub(' +', ' ', query_line.query_line)
            query_line_element.attrib['field'] = query_line.field
        filter_element = element_tree.SubElement(query_defintion_element, 'aqd:filters')
        build_filter_element(filter_element, query.query_definitions.query_filters)
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    out_dir = '{}/out/{}'.format(location, project_id)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    with open(out_dir + '/query.xml', 'w', encoding='utf-8') as xml_file:
        xml_file.write(element_tree.tostring(query_element, encoding='unicode', method='xml').replace(" aqd=",
                                                                                                      " xmlns:aqd=").replace(
            " dc=", " xmlns:dc=").replace('\u2018', '\"').replace('\u2019', "\""))
    query_converter = QueryConverter(query)
    save_scopus_queries(project_id, query_converter.scopus_queries)


def filter_from_json(json, old_query=False):
    if (old_query):
        return convert(json)
    try:
        timerange = Timerange(field=json['timerange']['field'],
                              start=json['timerange']['start'],
                              end=json['timerange']['end'])
    except:
        timerange = None
    filters = QueryFilters(
        query_filters=None,
        timerange=timerange
    )
    if json is not None:
        try:
            for filter in json['query_filters']:
                if filter['filter_term'] is not '':
                    filters.add_filter(QueryFilter(filter_field=filter['filter_field'],
                                               filter_type=filter['filter_type'],
                                               filter_term=filter['filter_term']))
        except:
            print('no filters given')
    return filters


def from_json(json):
    query = Query(creator=json['creator'],
                  contributor=json['contributor'],
                  licence=json['licence'],
                  licence_href=json['licence'],
                  date_modified=json['date_modified'],
                  identifier=json['identifier'],
                  title=json['title'],
                  description=json['description'])
    global_filter = filter_from_json(json['query_definitions']['query_filters'])
    query_definitions = QueryDefinitions(syntax=json['query_definitions']['syntax'],
                                         query_filters=global_filter,
                                         query_definition=None)
    for query_definition in json['query_definitions']['query_definition']:
        descriptions = []
        for description in query_definition['descriptions']:
            descriptions.append(description)
        partial_filter = None
        if query_definition['query_filters'] is not None:
            if query_definition['query_filters'].__len__() is not 0:
                partial_filter = filter_from_json(query_definition['query_filters'])
        query_definition_object = QueryDefinition(identifier=query_definition['identifier'],
                                                  query_lines=None,
                                                  descriptions=descriptions,
                                                  query_filters=partial_filter)
        for query_line in query_definition['query_lines']:
            query_definition_object.add_query_line(
                QueryLine(field=query_line['field'], query_line=query_line['query_line']))
        query_definitions.add_query_definition(query_definition_object)
    query.query_definitions = query_definitions
    return query


def get_versioned_query_as_html(project, version, name):
    with app.app_context():
        location = app.config.get("LIBINTEL_DATA_DIR")
    path = location + '/out//versions/' + project + '/' + version + '/'
    with open(path + 'query_' + name + '.xml', 'r', encoding='utf-8-sig') as xml_file:
        dom = etree.parse(xml_file)
    with open('query/query.xsl', 'r', encoding='utf-8-sig') as xsl_file:
        xslt = etree.parse(xsl_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return etree.tostring(newdom, pretty_print=True)
