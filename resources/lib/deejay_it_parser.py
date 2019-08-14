#!/usr/bin/python
import urllib
import simplejson as json


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

    def get_programs(self):
        return self._q_and_r('programs_ondemand?section=radio')

    def get_show_episodes(self, id):
        qry = 'archive_ondemand?pid=%s&rid=%s' % (id, id)
        print qry
        return self._q_and_r(qry)

    def get_speakers(self, prog):
        spkrs = []
        for spkr in prog['speakers']:
            spkrs.append(spkr['title'])
        return ', '.join(spkrs)
