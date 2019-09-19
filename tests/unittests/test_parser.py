#!/usr/bin/python2
from os.path import join, dirname
from simplejson import loads
from resources.lib.deejay_it_parser import DeejayItParser


class TestDeejayItParser:
    def test_speakers_dci(self):
        deejay = DeejayItParser()
        prog = self._load_json_file('speakers_dci.json')
        assert deejay.get_speakers(prog) == 'Linus, Nicola Savino'

    def test_speakers_empty_array(self):
        deejay = DeejayItParser()
        prog = self._load_json_file('speakers_empty_array.json')
        assert deejay.get_speakers(prog) == 'Radio Deejay'

    def test_speakers_missing(self):
        deejay = DeejayItParser()
        prog = self._load_json_file('speakers_missing.json')
        assert deejay.get_speakers(prog) == 'Radio Deejay'

    def _load_json_file(self, filename):
        abs_path = join(dirname(__file__), filename)
        with open(abs_path) as schema_file:
            return loads(schema_file.read())
