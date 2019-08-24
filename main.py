# -*- coding: utf-8 -*-

from resources.lib import kodilogging
import logging
import sys
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


def build_programs_list():
    progs_list = DEEJAY.get_programs(sys.argv[0])
    xbmcplugin.addDirectoryItems(ADDON_HANDLE,
                                 progs_list,
                                 len(progs_list))
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def build_ep_list():
    eps_list = DEEJAY.get_show_episodes(ARGS,
                                        sys.argv[0])
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
