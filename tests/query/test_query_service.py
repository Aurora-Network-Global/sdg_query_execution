from unittest import TestCase

from service import query_service


class TestQueryService(TestCase):
    def test_import_old_query(self):
        old_query = {"affiliation_id": "123456",
                     "author_id": "9837-3493-034i-2344",
                     "author_name": "Max Mustermann",
                     "end_year": "2018",
                     "start_year": "2015",
                     "subject": "PHYS",
                     "title": "This is test old query",
                     "topic": "test OR testing OR (test AND case)"
                     }
        new_query = query_service.convert(old_query)
        assert new_query.title == old_query['title']
        assert old_query['end_year'] == new_query.query_definitions.query_filters.timerange.end
        assert old_query['start_year'] == new_query.query_definitions.query_filters.timerange.start
        assert 'AU-ID' == new_query.query_definitions.query_filters.query_filters[0].filter_field
        assert old_query['author_id'] == new_query.query_definitions.query_filters.query_filters[0].filter_term
        assert 'AUTH' == new_query.query_definitions.query_filters.query_filters[1].filter_field
        assert old_query['author_name'] == new_query.query_definitions.query_filters.query_filters[1].filter_term
        assert 'AF-ID' == new_query.query_definitions.query_filters.query_filters[2].filter_field
        assert old_query['affiliation_id'] == new_query.query_definitions.query_filters.query_filters[2].filter_term
        assert 'SUBJAREA' == new_query.query_definitions.query_filters.query_filters[3].filter_field
        assert old_query['subject'] == new_query.query_definitions.query_filters.query_filters[3].filter_term
        assert 'TITLE-ABS-KEY' == new_query.query_definitions.query_definition[0].query_lines[0].field
        assert old_query['topic'] == new_query.query_definitions.query_definition[0].query_lines[0].query_line





