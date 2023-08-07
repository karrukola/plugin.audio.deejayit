"""Test suite to verify get_podcast_season_episodes() functionality."""
from pathlib import Path

from resources.lib.deejayit import DeejayIt, Episode

# ruff: noqa: INP001, S101, B011, ANN201, ANN001, E501

SEASON_ID = 6658
PAGE = 1
GET_URL = f"https://www.deejay.it/api/pub/v2/all/mhub/audios?season_id={SEASON_ID}&page={PAGE}&sort=desc"


def test_get_podcast_season_episodes(requests_mock):
    """Test positive case for get_podcast_season_episodes() query.

    Asserts on Un etto di fumeeto, episodio 8.

    :param requests_mock: mocker for requests
    :type requests_mock: mocked request
    """
    mock_answer = Path(__file__).parent / "trio.json"
    requests_mock.get(GET_URL, text=mock_answer.read_text())
    deejay = DeejayIt()
    p_eps = deejay.get_podcast_season_episodes(SEASON_ID, page_nr=PAGE)
    exp_out = Episode(
        "Episodio 8: Young Adult Parte 2",
        'Nell\u2019ultima puntata di "Un etto di fumetto" il Trio Medusa racconta della prima protagonista LGBTQ+ nella storia dei cartoni animati e non solo: Lady Oscar, Occhi di Gatto, Lam\u00f9. Immancabile il contributo altamente inattendibile di Stefano Rapone.',
        "https://media.deejay.it/2022/05/05/series/etto_fumetto/hls-etto_fumetto-s1_e8_un_etto_di_fumetto/hls-etto_fumetto-s1_e8_un_etto_di_fumetto.m3u8",
        "https://cdn.gelestatic.it/deejay/sites/2/2022/03/1400x1400-UnEttodiFumetto-320x320.jpg",
        "https://cdn.gelestatic.it/deejay/sites/2/2022/03/1400x1400-UnEttodiFumetto-1200x675.jpg",
        "09/05/2022",
        "Trio Medusa",
        "Un etto di fumetto",
    )
    for p_ep in p_eps:
        if p_ep.title == "Episodio 8: Young Adult Parte 2":
            break
    # pytest.fail makes the function exit, therefore the episode is always
    # defined at this stage.
    assert p_ep == exp_out
