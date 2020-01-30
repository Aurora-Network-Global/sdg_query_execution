import pytest

from app import create_app
from unpaywall.Unpaywall import Unpaywall

def test_unpaywall(test_client):
        unpaywall = Unpaywall('10.1021/ic503095t')
        assert unpaywall.title == 'A Spin-Frustrated Trinuclear Copper Complex Based on Triaminoguanidine with an Energetically Well-Separated Degenerate Ground State'
        assert unpaywall.doi == '10.1021/ic503095t'
        assert unpaywall.doi_resolver == 'crossref'
        assert unpaywall.evidence is None
        assert unpaywall.free_fulltext_url is None
        assert unpaywall.   is_boai_license is False
        assert unpaywall.is_free_to_read is False
        assert unpaywall.is_subscription_journal is True
        assert unpaywall.license is None
        assert unpaywall.oa_color == 'closed'
        assert unpaywall.reported_noncompliant_copies == []


def test_wrong_doi_for_unpaywall(test_client):
    unpaywall = Unpaywall('10.1021/ic503')
    print(unpaywall)
    assert unpaywall is None


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('flask_test.cfg')

    flask_app.config['TESTING'] = True
    flask_app.config['LIBINTEL_USER_EMAIL'] = 'eike.spielberg@uni-due.de'
    flask_app.config['WTF_CSRF_ENABLED'] = False
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()