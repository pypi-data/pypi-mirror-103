from __future__ import absolute_import

import importlib

from thglib.version import __version__

version = __version__

__all__ = [
    'teste'

]

for module in __all__:
    importlib.import_module('.%s' % module, 'thglib')
