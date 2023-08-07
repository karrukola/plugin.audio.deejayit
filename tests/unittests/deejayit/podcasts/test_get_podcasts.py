"""Test suite to verify get_podcasts() functionality."""

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


TRIO = Show(
    "Un etto di fumetto",
    6658,
    "In ogni puntata il Trio Medusa ripercorre la storia dei pi\u00f9 importanti cartoni animati giapponesi trasmessi in Italia negli anni \u201880, tra ricordi e informazioni serie e facete. Al loro fianco, Stefano Rapone e le sue curiosit\u00e0 poco probabili trovate nei meandri del deep web di cui \u00e8 esperto frequentatore.",
    "https://cdn.gelestatic.it/deejay/sites/2/2022/03/1400x1400-UnEttodiFumetto.jpg",
    "https://cdn.gelestatic.it/deejay/sites/2/2022/03/1400x1400-UnEttodiFumetto.jpg",
)


def test_get_podcasts_all_pages(deejay: DeejayIt, requests_mock):
    """Test positive case for get_podcasts() query.

    As the method makes more than 1 request, we are mocking 4 req/resp.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    :param requests_mock: mocker for requests
    :type requests_mock: _type_
    """
    for page_nr in range(1, 5):
        shows_url = f"https://www.deejay.it/api/pub/v2/all/mhub/series?brand_id=deejay&page={page_nr}&pagination_rows=15&sort=desc"
        mock_answer = Path(__file__).parent / f"podcasts_4-{page_nr}.json"
        requests_mock.get(shows_url, text=mock_answer.read_text())

    shows = deejay.get_podcasts()
    nr_shows = 45

    assert len(shows) == nr_shows

    for show_id, exp_out in zip([6658], [TRIO]):
        for show in shows:
            if show_id == show.id:
                assert show == exp_out
                break
        else:
            pytest.fail(f"Cannot find {exp_out.name}!?")
