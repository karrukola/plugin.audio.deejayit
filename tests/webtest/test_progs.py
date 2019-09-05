import pytest
from resources.lib.deejay_it_parser import DeejayItParser
from .support.assertions import assert_valid_schema, assert_expected_answer

DEEJAY = DeejayItParser()


@pytest.mark.webtest
def test_get_programs():
    json_data = DEEJAY.q_programs()
    assert_valid_schema(json_data, 'programs.json')


@pytest.mark.webtest
def test_cordialmente_exists():
    json_data = DEEJAY.q_cordialmente()
    assert_expected_answer(json_data, 'cordialmente.json')
