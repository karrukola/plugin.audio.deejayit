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
        li = xbmcgui.ListItem(label=prog['title'],
                              iconImage=prog['images']['size_320x320'])
        li.setProperty('fanart_image',
                       prog['images']['size_full'])
        url = build_url({'mode': 'eplist',
                         'id': prog['id']})
        # this is still a folder, so isFolder must be True
        progs_list.append((url, li, True))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE,
                                 progs_list,
                                 len(progs_list))
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def build_ep_list():
    eps_list = []
    show_id = ARGS.get('id', None)[0]
    eps = DEEJAY.get_show_episodes(show_id)
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
                url = build_url({'mode': 'stream',
                                 'url': file_url,
                                 'title': title})
                eps_list.append((url, li, False))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE,
                                 eps_list,
                                 len(eps_list))
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def play_song(url):
    play_item = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=play_item)


def main():
    mode = ARGS.get('mode', None)
    print mode
    if mode is None:
        build_programs_list()
    elif mode[0] == 'eplist':
        build_ep_list()
    elif mode[0] == 'stream':
        play_song(ARGS['url'][0])


if __name__ == '__main__':
    logger = kodilogging.KodiLogHandler()
    logger.emit(str(ARGS))
    main()
