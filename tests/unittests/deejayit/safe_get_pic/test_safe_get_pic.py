from json import loads
from pathlib import Path

import pytest

from resources.lib.deejayit import DeejayIt


@pytest.fixture(scope="session")
def session_setup_teardown() -> DeejayIt:
    deejayit = DeejayIt()
    return deejayit


@pytest.mark.parametrize(
    "input_data,exp_out",
    [
        (
            "test_safe_get_pic_w_art.json",
            "https://cdn.gelestatic.it/deejay/sites/2/2023/07/Elio-carpi-puntata-1200x627.jpg",
        ),
        (
            "test_safe_get_pic_wo_art.json",
            None,
        ),
    ],
)
def test_safe_get_pic(session_setup_teardown: DeejayIt, input_data, exp_out):
    deejay = session_setup_teardown
    test_data = input_data
    file_path = Path(__file__).parent / test_data
    print(file_path.absolute())
    url = deejay._safe_get_pic(loads(file_path.read_text()), "size_1200x675")
    assert url == exp_out
