# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thumbor_expire']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2" and python_version < "3"': ['libthumbor>=1.3.2,<2.0.0'],
 ':python_version >= "3.6"': ['libthumbor>=2.0.1,<3.0.0']}

setup_kwargs = {
    'name': 'thumbor-expire',
    'version': '0.1.1',
    'description': 'Add timeout verification for thumbor',
    'long_description': '# thumbor-expire\nAdd timeout verification for thumbor\n\n## Use \n\n* Server side\n\nthumbor config file set `URL_SIGNER = thumbor_expire.base64_hmac_sha1_expire`\n\n\n* Client side\n\nuse `from thumbor_expire.crypto import CryptoURL` class and pass expire argument, accept type `:obj:`int` | :obj:`float` | :obj:`datetime.timedelta` | \\\n        :obj:`datetime.datetime` | :obj:`datetime.time`, optional`\n',
    'author': 'HonQii',
    'author_email': 'honqi3014@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HonQii/thumbor-expire.git',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
