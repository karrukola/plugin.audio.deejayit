from json import loads
from os.path import join, dirname
from jsonschema import validate


def assert_valid_schema(data, schema_file):
    schema = _load_json_schema(schema_file)
    return validate(data, schema)


def assert_expected_answer(data, exp_answ):
    return data == _load_json_file(exp_answ)


def _load_json_schema(filename):
    rel_path = join('schemas', filename)
    return _load_json_file(rel_path)


def _load_json_file(filename):
    abs_path = join(dirname(__file__), filename)
    with open(abs_path) as schema_file:
        return loads(schema_file.read())
