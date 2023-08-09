"""Test suite to verify get_radios() functionality."""

from html import unescape
from json import loads
from pathlib import Path

import pytest

from resources.lib.deejayit import DeejayIt, Show

# ruff: noqa: INP001, S101, B011, ANN201, ANN001, E501


@pytest.fixture(scope="module", name="deejay")
def deejay_setup() -> DeejayIt:
    """Prepare a client.

    :return: client to deejay.it APIs
    :rtype: DeejayIt
    """
    return DeejayIt()


def _giveme_a_show(filepath: Path, idx: int) -> Show:
    shows = loads(filepath.read_text())
    show = shows["results"][idx]
    return Show(
        unescape(show["name"]),
        show["id"],
        unescape(show["description"]),
        show["images"]["size_320x320"],
        show["images"]["size_1200x675"],
    )


def test_get_radios_one_page(deejay: DeejayIt, requests_mock):
    """Test the case where the client has to make only 1 request.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    exp_show = _giveme_a_show(Path(__file__).parent / "shows_2-1.json", 0)
    shows_url = "https://www.deejay.it/api/pub/v2/all/mhub/programs?brand_id=deejay&page=1&pagination_rows=15&sort=desc"
    mock_answer = Path(__file__).parent / "shows_1-1.json"
    requests_mock.get(shows_url, text=mock_answer.read_text())

    shows = deejay.get_shows()

    # 14 is the size of the mocked response
    assert len(shows) == 14  # noqa: PLR2004
    for show in shows:
        if show.id == exp_show.id:
            assert show == exp_show
            break
    else:
        pytest.fail(f"Cannot find {exp_show.name}!?")


@pytest.mark.parametrize(
    ("filename", "idx"),
    [
        ("shows_2-2", 8),  # Cordialmente
        ("shows_2-1", 0),  # Deejay Chiama Italia
    ],
)
def test_get_radios_two_pages(deejay: DeejayIt, requests_mock, filename: str, idx: int):
    """Test the case where the client has to make 2 requests.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    exp_show = _giveme_a_show(Path(__file__).parent / f"{filename}.json", idx)

    for page_nr in range(1, 3):
        shows_url = f"https://www.deejay.it/api/pub/v2/all/mhub/programs?brand_id=deejay&page={page_nr}&pagination_rows=15&sort=desc"
        mock_answer = Path(__file__).parent / f"shows_2-{page_nr}.json"
        requests_mock.get(shows_url, text=mock_answer.read_text())

    shows = deejay.get_shows()
    nr_shows = 30

    assert len(shows) == nr_shows  # show from page 1
    for show in shows:
        if show.id == exp_show.id:
            assert show == exp_show
            break
    else:
        pytest.fail(f"Cannot find {exp_show.name}!?")
