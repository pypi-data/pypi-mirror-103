import requests  # noqa
import pytz      # noqa

from yokr import libs_in_use

packages_info = libs_in_use()

names = set([lib_info.Entity for lib_info in packages_info])

assert 'sys' not in names
assert 'pprint' not in names
assert 'yokr' not in names

assert 'requests' in names
assert 'pytz' in names
