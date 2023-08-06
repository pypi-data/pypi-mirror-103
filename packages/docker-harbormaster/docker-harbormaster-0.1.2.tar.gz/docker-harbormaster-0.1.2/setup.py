# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_harbormaster']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'docker-compose>=1.29.1,<2.0.0']

entry_points = \
{'console_scripts': ['harbormaster = docker_harbormaster.cli:cli']}

setup_kwargs = {
    'name': 'docker-harbormaster',
    'version': '0.1.2',
    'description': 'A supervisor for docker-compose apps.',
    'long_description': "Harbormaster\n============\n\nHarbormaster is a small utility that lets you easily deploy multiple\nDocker-Compose applications.\n\n\nInstallation\n------------\n\nInstalling Harbormaster is simple. You can use `pipx` (recommended):\n\n```\n$ pipx install docker-harbormaster\n```\n\nOr `pip` (less recommended):\n\n```\n$ pip install docker-harbormaster\n```\n\nYou need to also make sure you have `git` installed on your system.\n\n\nUsage\n-----\n\nHarbormaster uses a single YAML configuration file that's basically a list of\nrepositories to deploy:\n\n```\nrepositories:\n  myapp:\n    url: https://github.com/someuser/somerepo.git\n  otherapp:\n    url: https://gitlab.com/otheruser/otherrepo.git\n```\n\nThen, just run Harbormaster in the same directory as that configuration file.\nHarbormaster will parse the file, automatically download the repositories\nmentioned in it (and keep them up to date).\n\nHarbormaster only ever writes to the working directory you specify, and nowhere\nelse. All the data for each Compose app is under `<workdir>/data/<appname>`, so\nyou can easily back up the entire data directory in one go.\n\n\nHandling data directories\n-------------------------\n\nDue to the way Compose files work, you need to do some extra work to properly\ntell Harbormaster about your volumes.\n\nHarbormaster provides two kinds of directories: Data and cache.\n\nData is anything that you want to keep. Data directories will never be deleted,\nif you remove an app later on, its corresponding data directory will be moved\nunder the `archives/` directory and renamed to `<appname>-<deletion date>`.\n\nCache is anything you don't care about. When you remove an app from the config,\nthe cache dir is deleted.\n\nHarbormaster will look for a file called `docker-compose.yml` at the root of the\nrepo, and look for the specific strings `{{ HM_DATA_DIR }}` and\n`{{ HM_CACHE_DIR }}` in it. It will replace those strings with the proper\ndirectories (without trailing slashes), so the `volumes` section of your\nCompose file in your repository needs to look something like this:\n\n```\nvolumes:\n  - {{ HM_DATA_DIR }}/my_data:/some_data_dir\n  - {{ HM_DATA_DIR }}/foo:/home/foo\n  - {{ HM_CACHE_DIR }}/my_cache:/some_cache_dir\n```\n",
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/stavros/harbormaster',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
