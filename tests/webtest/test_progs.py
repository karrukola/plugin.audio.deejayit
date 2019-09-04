import pytest
from resources.lib.deejay_it_parser import DeejayItParser
from .support.assertions import assert_valid_schema


@pytest.mark.webtest
def test_get_programs():
    deejay = DeejayItParser()
    json_data = deejay.q_programs()
    assert_valid_schema(json_data, 'programs.json')
