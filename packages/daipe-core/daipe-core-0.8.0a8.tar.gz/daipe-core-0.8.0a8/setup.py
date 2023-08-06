# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['daipecore',
 'daipecore.bootstrap',
 'daipecore.decorator',
 'daipecore.decorator.tests',
 'daipecore.function',
 'daipecore.lineage',
 'daipecore.lineage.argument',
 'daipecore.logger',
 'daipecore.test']

package_data = \
{'': ['*'], 'daipecore': ['_config/*']}

install_requires = \
['injecta>=0.10.0,<0.11.0',
 'logger-bundle>=0.7.0,<0.8.0',
 'pyfony-bundles>=0.4.0,<0.5.0']

entry_points = \
{'daipe': ['input_decorators_mapping = daipecore.lineage.mapping:get_mapping'],
 'pyfony.bundle': ['create = daipecore.DaipeCore:DaipeCore']}

setup_kwargs = {
    'name': 'daipe-core',
    'version': '0.8.0a8',
    'description': 'Daipe framework core',
    'long_description': '# Daipe Core\n\nCore component of the [Daipe Framework](https://www.daipe.ai).  \n\n## Resources\n\n* [Documentation](https://docs.daipe.ai/)\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/daipe-ai/daipe-core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
