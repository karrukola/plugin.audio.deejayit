#!/usr/bin/python
import urllib
import simplejson as json
from xbmcgui import ListItem


class DeejayItParser():
    def __init__(self):
        self.base_url = 'http://www.deejay.it/api/pub/v1/'

    def _q_and_r(self, sp_qry):
        query_url = self.base_url + sp_qry
        hres = urllib.urlopen(query_url).read().decode("utf-8")
        if hres == '':
            data_to_ret = None
        else:
            data_to_ret = json.loads(hres)
        return data_to_ret

    def _q_programs(self):
        return self._q_and_r('programs_ondemand?section=radio')

    def _q_show_episodes(self, id):
        qry = 'archive_ondemand?pid=%s&rid=%s' % (id, id)
        print qry
        return self._q_and_r(qry)

    def _get_speakers(self, prog):
        spkrs = []
        for spkr in prog['speakers']:
            spkrs.append(spkr['title'])
        return ', '.join(spkrs)

    def build_url(self, base_url, query):
        base_url = base_url
        return base_url + '?' + urllib.urlencode(query)

    def get_programs(self, base_url):
        progs = self._q_programs()
        progs_list = []
        for prog in progs:
            show = prog['title']
            icon = prog['images']['size_320x320']
            fanart = prog['images']['size_full']
            spkrs = self._get_speakers(prog)
            li = ListItem(label=show,
                          iconImage=icon)
            li.setProperty('fanart_image', fanart)
            url = self.build_url(base_url,
                                 {'mode': 'eplist',
                                  'id': prog['id'],
                                  'fanart': fanart,
                                  'icon': icon,
                                  'show': show,
                                  'spkrs': spkrs})
            # this is still a folder, so isFolder must be True
            progs_list.append((url, li, True))
        return progs_list
