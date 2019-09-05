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

    def q_cordialmente(self):
        return self._q_and_r('archive_ondemand?pid=15&rid=15&date_start=2018-05-01')

    def q_programs(self):
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
        progs = self.q_programs()
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

    def get_show_episodes(self, args, base_url):
        # mostly passing through
        show_id = args.get('id', None)[0]
        fanart = args.get('fanart', None)[0]
        icon = args.get('icon', None)[0]
        show = args.get('show', None)[0]
        spkrs = args.get('spkrs', None)[0]
        eps = self._q_show_episodes(show_id)
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
                    li = ListItem(label=title)
                    li.setProperty('IsPlayable', 'true')
                    li.setArt({'fanart': fanart})
                    # li.setInfo('music', {'date': ep[1], 'count': idx})
                    url = self.build_url(base_url,
                                         {'mode': 'stream',
                                          'url': file_url,
                                          'title': title,
                                          'icon': icon,
                                          'show': show,
                                          'spkrs': spkrs})
                    eps_list.append((url, li, False))
        return eps_list
