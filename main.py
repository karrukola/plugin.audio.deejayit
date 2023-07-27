from __future__ import annotations

import sys
from datetime import datetime
from urllib.parse import parse_qs, urlencode

import xbmc
import xbmcgui
import xbmcplugin

from resources.lib.deejayit import DeejayIt


def _build_url(query: dict[str, str | int]) -> str:
    base_url = sys.argv[0]
    return base_url + "?" + urlencode(query)


def _build_webradios_page() -> None:
    li_list = []
    radios = DeejayIt().get_radios()
    for radio in radios:
        item = xbmcgui.ListItem(label=radio.name, label2=radio.desc)
        item.setArt(
            {
                "icon": radio.logo_url,
                "fanart": radio.fanart_url,
                # TODO: @karrukola consider icon
            },
        )
        item.setProperty("IsPlayable", "true")
        url = _build_url(
            {
                "mode": "livestream",
                "url": radio.content_url,
                "webradio": radio.name,
                "fanart_url": radio.fanart_url,
                "logo_url": radio.logo_url,
                "metadata_url": radio.metadata_url,
            },
        )
        li_list.append((url, item, False))

    xbmcplugin.addDirectoryItems(ADDON_HANDLE, li_list, len(li_list))
    # set the content of the directory
    xbmcplugin.setContent(ADDON_HANDLE, "songs")
    xbmcplugin.endOfDirectory(ADDON_HANDLE)
    xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_LABEL)


def _build_shows_page() -> None:
    li_list = []
    for show in DeejayIt().get_shows():
        item = xbmcgui.ListItem(label=show.name, label2=show.desc)
        item.setProperty("IsPlayable", "false")
        item.setArt({"icon": show.logo_url, "fanart": show.fanart_url})
        url = _build_url(
            {
                "mode": "reloaded",
                "show_id": show.id,
                "page": 1,
                "fanart_url": show.fanart_url,
            },
        )
        li_list.append((url, item, True))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE, li_list, len(li_list))
    # set the content of the directory
    xbmcplugin.setContent(ADDON_HANDLE, "songs")
    xbmcplugin.endOfDirectory(ADDON_HANDLE)
    xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_LABEL)


def _adjust_show_date(ddmmyyyy: str) -> str:
    """Transform date from dd/mm/yyyy to yyyy-mm-dd format.

    :param ddmmyyyy: dd/mm/yyyy date in string format
    :type ddmmyyyy: str
    :return: yyyy-mm-dd date in string format
    :rtype: str
    """
    (day, month, year) = ddmmyyyy.split("/")
    return f"{year}-{month}-{day}"


def _build_reloaded_page(show_id: str, page_nr: int, show_fanart_url: str) -> None:
    li_list = []
    for epsd in DeejayIt().get_show_episodes(show_id, page_nr):
        # not all episodes have pics associated to them, in such case we fall
        # back to the show one
        fanart_url = epsd.fanart_url if epsd.fanart_url is not None else show_fanart_url
        item = xbmcgui.ListItem(epsd.title, epsd.desc, offscreen=True)
        item.setArt({"icon": epsd.logo_url, "fanart": fanart_url})
        item.setDateTime(_adjust_show_date(epsd.date))

        item.setInfo("music", {"comment": epsd.desc})

        item.setProperty("IsPlayable", "true")
        url = _build_url(
            {
                "mode": "stream",
                "url": epsd.content_url,
                "speakers": epsd.speakers,
                "album": epsd.program,
                "fanart_url": fanart_url,
            },
        )
        li_list.append((url, item, False))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE, li_list, len(li_list))

    # next page
    next_page_item = xbmcgui.ListItem(">>> Di più")
    next_page_item.setDateTime("1982-02-01")  # cannot be earlier than then!
    xbmcplugin.addDirectoryItem(
        ADDON_HANDLE,
        _build_url(
            {
                "mode": "reloaded",
                "show_id": show_id,
                "page": int(page_nr) + 1,
                "fanart_url": fanart_url,
            },
        ),
        next_page_item,
        isFolder=True,
    )
    xbmcplugin.setContent(ADDON_HANDLE, "songs")
    xbmcplugin.endOfDirectory(ADDON_HANDLE)

    xbmcplugin.addSortMethod(ADDON_HANDLE, xbmcplugin.SORT_METHOD_DATE)


def _play_live_content(
    url: str,
    webradio: str,
    fanart_url: str,
    logo_url: str,
    metadata_url: str,
) -> None:
    """Play a live webradio.

    As this is a live stream, the currently playing song must be regularly
    fetched via a metadata service in order to provide up-to-date information
    on UI.

    Note that metadata would get out of sync if user paused the stream, as
    the updates are driven via the clock and not handled relatively to the
    playbakc start

    :param url: URL of the content to be played, i.e. the m3u file.
    :type url: str
    :param fanart_url: URL of the picture to be used as fanart
    :type fanart_url: str
    :param logo_url: URL of the picture to be used as logo
    :type logo_url: str
    :param metadata_url: URL of the JSON information feed to fetch what is live
    :type metadata_url: str
    :return: nothing
    :rtype: None
    """
    item = xbmcgui.ListItem(path=url)
    item.setArt(
        {
            "fanart": fanart_url,
            "landscape": fanart_url,
            "clearlogo": logo_url,
            "icon": logo_url,
        },
    )
    item.setInfo("music", {"comment": webradio})
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=item)

    player = xbmc.Player()  # assumption: this does not change over execution time
    monitor = xbmc.Monitor()  # from forum: use monitor.waitForAbort() iso sleep()

    # A small delay is needed for getPlayingItem() to return.
    # This is now set to 3 seconds to be conservative, the only thing it delays
    # is the update of the metadata for the currently playing webradio stream.
    # TODO: @karrukola consider looping continuously through exception
    if monitor.waitForAbort(3):
        return

    last_update = ""
    while True:
        try:
            item = player.getPlayingItem()
        except RuntimeError:
            # If the player is not active anymore, the exception is raised.
            # If a metadata update is due and the player had been stopped,
            # this situation would occur. In this condition there is no point
            # to download and parse the metadata as well.
            return  # exit directly, no point in breaking out of the loop

        tag = item.getMusicInfoTag()
        print(f">>>> {tag.getComment()=}")
        print(f">>>> {webradio=}")
        if tag.getComment() != webradio:
            # this means we changed the stream while waiting for the next moment
            # to update the metadata
            print(f">>>> we are not playing the {webradio} anymore, exiting...")
            return
        metadata = DeejayIt.parse_webradio_metadata(metadata_url)
        if metadata.last_update == last_update:
            # metadata was not yet updated, just wait
            aborted = monitor.waitForAbort(5)
        else:
            # let's update the metadata
            tag.setTitle(metadata.title)
            tag.setArtist(metadata.artist)
            tag.setAlbum(metadata.album)
            player.updateInfoTag(item)
            print(f">>>> metadata updated: {metadata.title} - {metadata.artist}")

            last_update = metadata.last_update
            now = datetime.now()
            then = datetime.fromisoformat(metadata.next_date)
            # FIXME: sometimes we still have a negative delta, not clear why
            # this logic reacts to that situation
            if then > now:
                time_delta = then - now
                print(f">>>> next update: {metadata.next_date} <<<<<")
                print(f">>>> about to sleep for {time_delta.seconds} seconds <<<<<")
                aborted = monitor.waitForAbort(time_delta.seconds + 3)
            else:
                aborted = monitor.waitForAbort(5)

        if aborted:
            return  # exit directly, no point in breaking out of the loop


def _play_content(url: str, artist: str, album: str, fanart_url: str) -> None:
    item = xbmcgui.ListItem(path=url)
    item.setInfo(
        "music",
        {
            "artist": artist,
            "album": album,
        },
    )
    item.setArt(
        {
            "fanart": fanart_url,
            "landscape": fanart_url,
        },
    )
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=item)


def _build_main_page() -> None:
    targets = {
        "programmi": "Tutti i programmi",
        "webradio": "Webradio",
    }
    for target, name in targets.items():
        xbmcplugin.addDirectoryItem(
            ADDON_HANDLE,
            _build_url({"mode": target}),
            xbmcgui.ListItem(name),
            isFolder=True,
        )
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def _main() -> None:
    args = parse_qs(sys.argv[2][1:])
    mode = args.get("mode", None)

    # initial launch of add-on
    if mode is None:
        _build_main_page()
    elif mode[0] == "webradio":
        _build_webradios_page()
    elif mode[0] == "programmi":
        _build_shows_page()
    elif mode[0] == "reloaded":
        _build_reloaded_page(
            args["show_id"][0],
            args["page"][0],
            args["fanart_url"][0],
        )
    elif mode[0] == "livestream":
        _play_live_content(
            args["url"][0],
            args["webradio"][0],
            args["fanart_url"][0],
            args["logo_url"][0],
            args["metadata_url"][0],
        )
    elif mode[0] == "stream":
        _play_content(
            url=args["url"][0],
            artist=args["speakers"][0],
            album=args["album"][0],
            fanart_url=args["fanart_url"][0],
        )
    else:
        raise ValueError("Unhandled mode %s" % (mode))


if __name__ == "__main__":
    ADDON_HANDLE = int(sys.argv[1])
    _main()
