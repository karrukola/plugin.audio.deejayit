"""Test suite to verify get_show_episodes() functionality."""
from pathlib import Path

import pytest

from resources.lib.deejayit import DeejayIt, Episode

# ruff: noqa: INP001, S101, B011, ANN201, ANN001

EPS_URL = "https://www.deejay.it/api/pub/v2/all/mhub/search?program_id=15&audio_type=episode&page=1&pagination_rows=15&sort=desc"  # noqa: E501


def test_get_episodes(requests_mock):
    """Test the positive case, i.e. for Cordialmente.

    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    pagination_size = 15

    mock_answer = Path(__file__).parent / "cordialmente.json"
    requests_mock.get(EPS_URL, text=mock_answer.read_text())
    eps = DeejayIt().get_show_episodes(pagination_size, 1)

    exp_out = Episode(
        "Il ritorno del Concertozzo (Live in Carpi)",
        "La registrazione integrale del concerto di Elio e le Storie Tese "
        "andato in scena domenica 2 luglio 2023 in Piazza dei Martiri a Carpi",
        "https://media.deejay.it/2023/07/02/episodes/cordialmente/hls-cordialmente-20230702/hls-cordialmente-20230702.m3u8",  # noqa: E501
        "https://cdn.gelestatic.it/deejay/sites/2/2023/07/Elio-carpi-puntata-320x320.jpg",  # noqa: E501
        "https://cdn.gelestatic.it/deejay/sites/2/2023/07/Elio-carpi-puntata-1200x627.jpg",  # noqa: E501
        "02/07/2023",
        "Linus e Elio e le Storie Tese",
        "Cordialmente 4 stagioni",
    )

    assert len(eps) == pagination_size
    for ep in eps:
        if "Concertozzo" in ep.title:
            break
    else:
        pytest.fail("Manca il Concertozzo?!")
    # pytest.fail makes the function exit, therefore the episode is always
    # defined at this stage.
    assert ep == exp_out
