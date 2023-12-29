"""Integration tests for deejay.it Python client.

Their main purpose is to parse the information out of the API endpoint, to
ensure nothing had changed (thus that the mocks are still valid).
"""
import pytest

from resources.lib.deejayit import DeejayIt

# ruff: noqa: INP001, S101, B011, ANN201


@pytest.fixture(scope="module", name="deejay")
def deejay_setup() -> DeejayIt:
    """Prepare a client.

    :return: client to deejay.it APIs
    :rtype: DeejayIt
    """
    return DeejayIt()


def test_webradios(deejay: DeejayIt):
    """Get list of webradios.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    """
    radios = deejay.get_radios()
    assert len(radios) != 0

    cerca = "Radio Linetti"
    for radio in radios:
        print(radio.name)
        if radio.name == cerca:
            break
    else:
        pytest.fail(f"Manca {cerca}?")


def test_shows(deejay: DeejayIt):
    """Get full list of shows.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    """
    shows = deejay.get_shows()
    assert len(shows) != 0

    cerca = "Cordialmente"
    for show in shows:
        print(show.name)
        if show.name.startswith(cerca):
            break
    else:
        pytest.fail(f"Manca {cerca}")


def test_get_episodes(deejay: DeejayIt):
    """Get all episodes for a given show.

    Show is Cordialmente.
    Only page 1 is queried.

    :param deejay: client to deejay.it
    :type deejay: DeejayIt
    """
    eps = deejay.get_show_episodes(15, 1)
    assert len(eps) != 0


def test_parse_webradio_metadata_linetti():
    """Parse metadata for Radio Linetti."""
    info_url = "https://streamcdnb10-4c4b867c89244861ac216426883d1ad0.msvdn.net/webradio/metadata/deejaywfmlinus.json"
    info = DeejayIt.parse_webradio_metadata(info_url)
    assert info.last_update != ""
    assert info.next_date != ""
    assert info.artist != ""
    assert info.title != ""
    assert info.cover_url != ""
