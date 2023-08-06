# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rundeckpy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'paramiko>=2.7.2,<3.0.0']

entry_points = \
{'console_scripts': ['rdpy = rundeckpy.rundeckpy:cli',
                     'rundeckpy = rundeckpy.rundeckpy:cli']}

setup_kwargs = {
    'name': 'rundeckpy',
    'version': '0.2.7',
    'description': 'Rundeck python plugins, helper functions and cli tool',
    'long_description': '=========\nrundeckpy\n=========\nPython based Rundeck plugins.\n\nThe package contains:\n\n* a command line tool\n* a series of helper functions\n* a series of plugins\n* squeleton for new plugins\n\ncommand line tool\n#################\n\n\nplugins\n#######\n\n\nsqueleton\n#########\n\n\nbase class\n##########\n\n\nDevelopment\n###########\n\nInstall\n*******\nClone\n=====\nCreate venv \n===========\nActivate\n========\nInstall poetry \n==============\nInstall package\n===============\n.. code-block:: bash\n\n    poetry install\n\nTests\n*****\n\nCode Quality\n============\n\n.. code-block:: bash\n\n    black src/rundeckpy  \n    poetry run pylint src/rundeckpy/  \n\nTests and coverage\n==================\n\n.. code-block:: bash\n\n    poetry run pytest tests \n    poetry run coverage run -m pytest -v && poetry run coverage report -m  \n    poetry run pytest --cov=src/rundeckpy/ tests  \n  \npoetry build\n\npoetry publish\n\npoetry publish -r gitlab',
    'author': 'Thiago Takayama',
    'author_email': 'thiago@takayama.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/labitup/rundeck/rundeckpy/-/wikis/home',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
