# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['littleshelf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'little-shelf',
    'version': '0.0.1',
    'description': "Synchronized dictionaries using Greg Little's `shelf` CRDT.",
    'long_description': '# little-shelf\nSynchronized dictionaries using [Greg Little][0]\'s `shelf` CRDT.\n\nChanges/patches can be distributed to peers through any channel. See the\n[understory][1]\'s [Braid][2] implementation as an example of real world usage.\n\n# Install\n\n    pip install little-shelf\n\n# Use\n\n    >>> import littleshelf\n    >>> alice = littleshelf.LittleShelf()\n    >>> bob = littleshelf.LittleShelf()\n    >>> patch = alice.set(ham="spam")\n    >>> patch\n    [{\'ham\': [\'spam\', 0]}, 0]\n    >>> alice\n    {\'ham\': \'spam\'}\n    >>> alice == bob\n    False\n    >>> bob.merge(patch)\n    >>> alice == bob\n    True\n    >>> bob.get("ham") == bob["ham"] == "spam"\n    True\n\n[0]: //glittle.org\n[1]: //github.com/angelogladding/understory/blob/main/understory/web/braid.py\n[2]: //braid.org\n',
    'author': 'Angelo Gladding',
    'author_email': 'angelo@lahacker.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
