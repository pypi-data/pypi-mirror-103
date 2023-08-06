# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_embeddings',
 'text_embeddings.base',
 'text_embeddings.hash',
 'text_embeddings.visual']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.2.0,<9.0.0',
 'coverage-badge>=1.0.1,<2.0.0',
 'coverage>=5.5,<6.0',
 'icecream>=2.1.0,<3.0.0',
 'interrogate>=1.3.2,<2.0.0',
 'mmh3>=3.0.0,<4.0.0',
 'numpy>=1.20.2,<2.0.0',
 'pdoc3>=0.9.2,<0.10.0',
 'pytest>=6.2.3,<7.0.0',
 'torch>=1.8.1,<2.0.0',
 'transformers>=4.5.1,<5.0.0']

setup_kwargs = {
    'name': 'text-embeddings',
    'version': '0.0.3',
    'description': 'Non-traditional/no-vocabulary text embeddings in one place.',
    'long_description': None,
    'author': 'Chenghao Mou',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
