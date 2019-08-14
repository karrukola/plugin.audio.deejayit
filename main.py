# -*- coding: utf-8 -*-

from resources.lib import kodilogging
import logging
import sys
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from resources.lib.deejay_it_parser import DeejayItParser

# Keep this file to a minimum, as Kodi
# doesn't keep a compiled copy of this
ADDON = xbmcaddon.Addon()
ADDON_HANDLE = int(sys.argv[1])
ARGS = urlparse.parse_qs(sys.argv[2][1:])
kodilogging.config()
DEEJAY = DeejayItParser()


def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)


def build_programs_list():
    progs = DEEJAY.get_programs()
    progs_list = []
    for prog in progs:
        show = prog['title']
        icon = prog['images']['size_320x320']
        fanart = prog['images']['size_full']
        spkrs = DEEJAY.get_speakers(prog)
        li = xbmcgui.ListItem(label=show,
                              iconImage=icon)
        li.setProperty('fanart_image', fanart)
        url = build_url({'mode': 'eplist',
                         'id': prog['id'],
                         'fanart': fanart,
                         'icon': icon,
                         'show': show,
                         'spkrs': spkrs})
        # this is still a folder, so isFolder must be True
        progs_list.append((url, li, True))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE,
                                 progs_list,
                                 len(progs_list))
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def build_ep_list():
    # mostly passing through
    show_id = ARGS.get('id', None)[0]
    fanart = ARGS.get('fanart', None)[0]
    icon = ARGS.get('icon', None)[0]
    show = ARGS.get('show', None)[0]
    spkrs = ARGS.get('spkrs', None)[0]
    eps = DEEJAY.get_show_episodes(show_id)
    eps_list = []
    for ep in eps:
        data = ep.keys()[0]
        for tipo in ['reloaded']:
            # you get an array of podcast or a single reloaded
            if tipo == 'podcast':
                print ep[data][tipo]
                #         for pod in ep[data][tipo]:
                #             print pod
                #             print pod['title']
                #             print pod['file']
            else:
                # i.e. reloaded
                title = ep[data][tipo]['title']
                file_url = ep[data][tipo]['file']
                li = xbmcgui.ListItem(label=title)
                li.setProperty('IsPlayable', 'true')
                li.setArt({'fanart': fanart})
                # li.setInfo('music', {'date': ep[1], 'count': idx})
                url = build_url({'mode': 'stream',
                                 'url': file_url,
                                 'title': title,
                                 'icon': icon,
                                 'show': show,
                                 'spkrs': spkrs})
                eps_list.append((url, li, False))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE,
                                 eps_list,
                                 len(eps_list))
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def play_item():
    play_item = xbmcgui.ListItem(path=ARGS['url'][0])
    icon = ARGS.get('icon', None)[0]
    play_item.setThumbnailImage(icon)
    show_name = ARGS.get('show', None)[0]
    spkrs = ARGS.get('spkrs', None)[0]
    play_item.setInfo('music', {'album': show_name,
                                'artist': spkrs})
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=play_item)


def main():
    mode = ARGS.get('mode', None)
    print mode
    if mode is None:
        build_programs_list()
    elif mode[0] == 'eplist':
        build_ep_list()
    elif mode[0] == 'stream':
        play_item()


if __name__ == '__main__':
    logger = kodilogging.KodiLogHandler()
    logger.emit(str(ARGS))
    main()
