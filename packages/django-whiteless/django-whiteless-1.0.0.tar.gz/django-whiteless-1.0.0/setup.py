# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whiteless', 'whiteless.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.0,<4.0']

setup_kwargs = {
    'name': 'django-whiteless',
    'version': '1.0.0',
    'description': 'Django template tags for dealing with pesky whitespaces',
    'long_description': '# django-whiteless\n\nDjango template tags which deal with pesky whitespaces!\n\n[![CircleCI](https://circleci.com/gh/denizdogan/django-whiteless/tree/master.svg?style=svg)](https://circleci.com/gh/denizdogan/django-whiteless/tree/master)\n\n- Django 2.x and 3.x\n- Python 3.7, 3.8, 3.9\n\n## Installation\n\nInstall the latest version from PyPI:\n\n```bash\n$ pip install django-whiteless\n```\n\nAdd `"whiteless"` to `INSTALLED_APPS`:\n\n```python\nINSTALLED_APPS = (\n    # ...\n    "whiteless",\n)\n```\n\n## Usage\n\nThe library consists of two template tags, `{% whiteless %}` and `{% eof %}`.\nThis is how you use them.\n\n### Remove all whitespaces\n\n```djangotemplate\n{% whiteless %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove leading whitespaces\n\n```djangotemplate\n{% whiteless leading %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove trailing whitespaces\n\n```djangotemplate\n{% whiteless trailing %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove leading and trailing whitespaces\n\n```djangotemplate\n{% whiteless leading trailing %}\n    ...\n{% endwhiteless %}\n```\n\n### Replace whitespaces with a single space\n\n```djangotemplate\n{% whiteless space %}\n    ...\n{% endwhiteless %}\n```\n\nNote that if there are leading or trailing whitespaces in the block, those will\nalso be replaced by a single space. In order to remove leading and trailing\nwhitespaces and replace all other whitespaces with a single space, use:\n\n```djangotemplate\n{% whiteless space leading trailing %}\n    ...\n{% endwhiteless %}\n```\n\n### Remove trailing whitespaces at end of file\n\n```djangotemplate\nHello there!{% eof %}\n```\n\nThis is useful if e.g. your project style guide requires all files to end with\na newline but that causes issues with your template.\n\nNote that `{% eof %}` cannot be used inside other tags. It only removes\nwhitespaces that immediately follow itself.\n\n## Development\n\n```shell\n$ poetry shell\n$ poetry install\n$ pre-commit install  # install git hooks\n$ tox  # run tests\n```\n\n## License\n\n[MIT](LICENSE)\n',
    'author': 'Deniz Dogan',
    'author_email': 'denizdogan@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/denizdogan/django-whiteless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
