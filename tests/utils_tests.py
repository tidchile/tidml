import nose.tools as nt
from tidml.utils import prepare_path


def test_prepare_path():
    import os
    import shutil
    base_path = '~/.tidml/prepared_path/'
    file_name = 'the_file'
    shutil.rmtree(os.path.expanduser(base_path), ignore_errors=True)
    pp = prepare_path(base_path + file_name)
    nt.assert_regexp_matches(pp, '/Users/(.)+/\.tidml/prepared_path/the_file')
