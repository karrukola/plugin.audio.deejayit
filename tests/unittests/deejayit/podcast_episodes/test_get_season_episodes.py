"""Test suite to verify get_podcast_season_episodes() functionality."""
from html import unescape
from json import loads
from pathlib import Path

import pytest

from resources.lib.deejayit import DeejayIt, Episode

# ruff: noqa: INP001, S101, B011, ANN201, ANN001, E501

SEASON_ID = 6658
PAGE = 1
GET_URL = f"https://www.deejay.it/api/pub/v2/all/mhub/audios?season_id={SEASON_ID}&page={PAGE}&sort=desc"


def _giveme_an_ep(filepath: Path, idx: int) -> Episode:
    eps = loads(filepath.read_text())["results"]
    ep = eps[idx]
    return Episode(
        unescape(ep["name"]),
        unescape(ep["description"]),
        ep["hls_url"],
        ep["images"]["size_320x320"],
        ep["images"]["size_1200x675"],
        ep["datePublished"],
        unescape(" e ".join(spk["name"] for spk in ep["speakers"])),
        unescape(ep["serie"]["name"]),
    )


@pytest.mark.parametrize(
    ("filename", "idx"),
    [
        ("trio", 0),
        ("dnd", 0),
    ],
)
def test_get_podcast_season_episodes(requests_mock, filename: str, idx: int):
    """Verify you can retrieve season episodes.

    :param requests_mock: mocker for requests
    :type requests_mock: requests_mock
    :param filename: name of the JSON file from where to read the exp result
    :type filename: str
    :param idx: index to select the epiode being the expected result
    :type idx: int
    """
    answer_path = Path(__file__).parent / f"{filename}.json"
    exp_out = _giveme_an_ep(answer_path, idx)
    requests_mock.get(GET_URL, text=answer_path.read_text())
    deejay = DeejayIt()
    p_eps = deejay.get_podcast_season_episodes(SEASON_ID, page_nr=PAGE)
    for p_ep in p_eps:
        if p_ep.title == exp_out.title:
            assert p_ep == exp_out
            break
    else:
        pytest.fail(f"Cannot find {exp_out.title}!?")
