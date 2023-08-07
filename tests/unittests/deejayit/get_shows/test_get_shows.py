"""Test suite to verify get_radios() functionality."""

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


DJCI = Show(
    "Deejay Chiama Italia",
    20,
    "Linus e Nicola Savino in diretta con Matteo Curti e la regia di Alex Farolfi nel morning show che ha fatto la storia di Radio DEEJAY. Da lunedì a venerdì dalle 10 alle 12, in radio, web e TV (canale 69 del Digitale Terrestre)\r\n\r\nPer contattarci su WhatsApp scrivi a 342/5221012",
    "https://cdn.gelestatic.it/deejay/sites/2/2022/11/DeejayChiamaItalia_Cover-1200x627-alta-320x320.png",
    "https://cdn.gelestatic.it/deejay/sites/2/2022/11/DeejayChiamaItalia_Cover-1200x627-alta-1200x627.png",
)
CORDIALMENTE = Show(
    "Cordialmente 4 Stagioni",
    15,
    'Cordialmente con Linus e gli Elio e le Storie Tese torna per quattro puntate all\'anno: una per stagione\r\n\r\n2022\r\n\r\nInverno 28 febbraio\r\n\r\nPrimavera 23 maggio\r\n\r\nEstate 19 settembre\r\n\r\nAutunno 21 novembre\r\n\r\n&nbsp;\r\n\r\n2023\r\n\r\n&nbsp;\r\n\r\nInverno 6 marzo <a href="https://www.deejay.it/programmi/cordialmente/puntate/cordialmente-4-stagioni-del-06-03-2023/">ascolta qui</a>\r\n\r\nPrimavera  22 maggio <a href="https://www.deejay.it/programmi/cordialmente/puntate/cordialmente-4-stagioni-del-22-05-2023/">ascolta qui </a>\r\n\r\nEstate 24 luglio',
    "https://cdn.gelestatic.it/deejay/sites/2/2021/12/cordialmente-4-stagioni-1200x627-320x320.jpg",
    "https://cdn.gelestatic.it/deejay/sites/2/2021/12/cordialmente-4-stagioni-1200x627-1200x627.jpg",
)


def test_get_radios_one_page(deejay: DeejayIt, requests_mock):
    """Test the case where the client has to make only 1 request.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    shows_url = "https://www.deejay.it/api/pub/v2/all/mhub/programs?brand_id=deejay&page=1&pagination_rows=15&sort=desc"
    mock_answer = Path(__file__).parent / "shows_1-1.json"
    requests_mock.get(shows_url, text=mock_answer.read_text())

    shows = deejay.get_shows()

    # 14 is the size of the mocked response
    assert len(shows) == 14  # noqa: PLR2004
    for show in shows:
        if show.id == DJCI.id:
            assert show == DJCI
            break
    else:
        pytest.fail(f"Cannot find {DJCI.name}!?")


def test_get_radios_two_pages(deejay: DeejayIt, requests_mock):
    """Test the case where the client has to make 2 requests.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    for page_nr in [1, 2]:
        shows_url = f"https://www.deejay.it/api/pub/v2/all/mhub/programs?brand_id=deejay&page={page_nr}&pagination_rows=15&sort=desc"
        mock_answer = Path(__file__).parent / f"shows_2-{page_nr}.json"
        requests_mock.get(shows_url, text=mock_answer.read_text())

    shows = deejay.get_shows()
    nr_shows = 30

    assert len(shows) == nr_shows  # show from page 1

    for show_id, exp_out in zip([15, 20], [CORDIALMENTE, DJCI]):
        for show in shows:
            if show_id == show.id:
                assert show == exp_out
                break
        else:
            pytest.fail(f"Cannot find {exp_out.name}!?")
