from resources.lib.deejayit import DeejayIt


def test_legacy_shows():
    """Verify that legacy shows are listed properly."""
    deejay = DeejayIt()

    legacy_shows = deejay.get_legacy_shows()
    # FIXME: get_shows() should be based on Mocked HTTP response
    online_shows = deejay.get_shows()
    o_shows_ids = {show.id for show in online_shows}
    for legacy_show in legacy_shows:
        assert legacy_show.id not in (o_shows_ids)
