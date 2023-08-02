"""Unit tests for the function parsing metadata of a live webradio.

Data is fed via mocked HTTP responses.
"""
from pathlib import Path

from resources.lib.deejayit import DeejayIt, WebRadioMetadata

# ruff: noqa: INP001, S101, B011, ANN201, ANN001

LINETTI_URL = "https://streamcdnb10-4c4b867c89244861ac216426883d1ad0.msvdn.net/webradio/metadata/deejaywfmlinus.json"  # noqa: E501
DEEJAY_TIME_URL = "https://streamcdnb2-4c4b867c89244861ac216426883d1ad0.msvdn.net/webradio/metadata/deejaytime.json"  # noqa: E501


def test_linetti(requests_mock):
    """Parse information for Radio Linetti.

    This is a positive case, where all information is populated by the API.

    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    mock_answer = Path(__file__).parent / "linetti.json"
    requests_mock.get(LINETTI_URL, text=mock_answer.read_text())
    out = DeejayIt.parse_webradio_metadata(LINETTI_URL)

    exp_out = WebRadioMetadata(
        "2023-07-22 11:42:56",
        "The Look Of Love",
        "ABC",
        "The Lexicon Of Love",
        "https://4c4b867c89244861ac216426883d1ad0.msvdn.net/radio/coverart/song003275_100x100.jpg",  # noqa: E501
        "2023-07-22 11:46:25",
    )

    assert out == exp_out


def test_deejaytime_no_album(requests_mock):
    """Parse information when no album is given.

    This is a case found first for Deejay Time, the album information is empty.

    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    mock_answer = Path(__file__).parent / "deejay_time.json"
    requests_mock.get(DEEJAY_TIME_URL, text=mock_answer.read_text())
    out = DeejayIt.parse_webradio_metadata(DEEJAY_TIME_URL)

    exp_out = WebRadioMetadata(
        "2023-07-22 23:01:25",
        "All I Really Want",
        "KIM LUKAS",
        None,
        "https://4c4b867c89244861ac216426883d1ad0.msvdn.net/radio/coverart/song078194_100x100.jpg",  # noqa: E501
        "2023-07-22 23:05:24",
    )

    assert out == exp_out
