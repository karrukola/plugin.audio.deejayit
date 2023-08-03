"""Test suite to verify get_show_episodes() functionality."""
from pathlib import Path

import pytest

from resources.lib.deejayit import DeejayIt, WebRadio

# ruff: noqa: INP001, S101, B011, ANN201, ANN001

GET_RADIOS_URL = "https://www.deejay.it/api/pub/v2/all/mhub/webradios/deejay"
NR_RADIOS = 10


def test_get_webradios(requests_mock):
    """Test positive case for get_radios() query.

    Asserts on Radio Linetti.

    :param requests_mock: mocker for requests
    :type requests_mock: mocked request_
    """
    mock_answer = Path(__file__).parent / "webradios.json"
    requests_mock.get(GET_RADIOS_URL, text=mock_answer.read_text())
    radios = DeejayIt().get_radios()

    exp_out = WebRadio(
        "Radio Linetti",
        "La più bella musica radiofonica scelta da Linus.",
        "https://4c4b867c89244861ac216426883d1ad0.msvdn.net/webradio/deejaywfmlinus/playlist.m3u8",  # noqa: E501
        "https://cdn.gelestatic.it/deejay/sites/2/2019/04/linetti-320x320.png",
        "https://cdn.gelestatic.it/deejay/sites/2/2019/04/webradio_linus1-1200x675.jpg",
        "https://4c4b867c89244861ac216426883d1ad0.msvdn.net/webradio/metadata/deejaywfmlinus.json",  # noqa: E501
    )

    assert len(radios) == NR_RADIOS
    for radio in radios:
        if "Radio Linetti" in radio.name:
            break
    else:
        pytest.fail("Manca Radio Linetti?!")
    # pytest.fail makes the function exit, therefore the episode is always
    # defined at this stage.
    assert radio == exp_out
