# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cjwmodule',
 'cjwmodule.arrow',
 'cjwmodule.http',
 'cjwmodule.i18n',
 'cjwmodule.spec',
 'cjwmodule.testing',
 'cjwmodule.util']

package_data = \
{'': ['*']}

install_requires = \
['google-re2>=0.1.20210401,<0.2.0',
 'httpx>=0.17,<1.0',
 'jsonschema>=3.2.0,<3.3.0',
 'pyarrow>=2.0.0,<4.0.0',
 'pytz>=2021.1,<2022.0',
 'pyyaml>=5.4.1,<5.5.0',
 'rfc3987>=1.3.8,<1.4.0']

entry_points = \
{'console_scripts': ['check-messages = maintenance.i18n:check',
                     'extract-messages = maintenance.i18n:extract']}

setup_kwargs = {
    'name': 'cjwmodule',
    'version': '4.1.8',
    'description': 'Utilities for Workbench modules',
    'long_description': 'Utilities for [CJWorkbench](https://github.com/CJWorkbench/cjworkbench) modules.\n\nWorkbench modules may _optionally_ depend on the latest version of this Python\npackage for its handy utilities:\n\n* `cjwmodule.arrow.condition`: functions to create Arrow table masks.\n* `cjwmodule.arrow.format`: functions to convert Arrow arrays to text.\n* `cjwmodule.arrow.types`: types your Arrow module may accept and return.\n* `cjwmodule.arrow.testing`: helpers for programming tests.\n* `cjwmodule.http`: HTTP helpers, including the handy `httpfile` format.\n* `cjwmodule.i18n`: A `trans()` function for producing translatable text.\n* `cjwmodule.testing`: Functions to help in unit testing.\n* `cjwmodule.util.colnames`: Functions to help build a valid table\'s column names.\n* `cjwmodule.spec`: Functions to load and validate module spec files.\n* `cjwmodule.types`: Types your module may accept and return.\n\nDeveloping\n==========\n\n0. Run `tox` to confirm that unit tests pass\n1. Write a failing unit test in `tests/`. (`tox` should fail now.)\n2. Make it pass by editing code in `cjwmodule/`\n3. Run `poetry run extract-messages` if i18n data changed\n4. Run `tox` to confirm that unit tests pass again\n5. Submit a pull request\n\nPreserve a consistent API. Workbench will upgrade this dependency without module\nauthors\' consent. Add new features; fix bugs. Don\'t alter existing behavior.\n\nI18n\n====\n\n### Marking strings for translation\n\nStrings in `cjwmodule` can be marked for translation using `cjwmodule.i18n._trans_cjwmodule`.\nEach translation message must have a (unique) ID. ICU is supported for the content.\nFor example,\n\n```python\nfrom cjwmodule.i18n import _trans_cjwmodule\n\nerr = "Error 404"\n\nwith_arguments = _trans_cjwmodule(\n    "greatapi.exception.message",\n    "Something is wrong: {error}",\n    {"error": err}\n)\n\nwithout_arguments = _trans_cjwmodule(\n    "greatapi.exception.general",\n    "Something is wrong",\n)\n```\n\nWorkbench is wired to accept the return value of `_trans_cjwmodule` wherever an\nerror/warning or quick fix is expected.\n\n### Creating `po` catalogs\n\nCalls to `_trans_cjwmodule` can (and must) be parsed to create `cjwmodule`\'s\n`.po` files.  Update the `.po` files with:\n\n```\npoetry run extract-messages\n```\n\n### Unit testing\n\nIn case a `_trans_cjwmodule` invocation needs to be unit tested, you can use\n`cjwmodule.testing.i18n.cjwmodule_i18n_message` like this:\n\n```python\nfrom cjwmodule.testing.i18n import cjwmodule_i18n_message\nimport with_arguments, without_arguments\n\nassert with_arguments == cjwmodule_i18n_message("greatapi.exception.message", {"error": "Error 404"})\nassert without_arguments == cjwmodule_i18n_message("greatapi.exception.general")\n```\n\n### Message deprecation\n\nFor backwards compatibility, *messages in `cjwmodule`\'s `po` files are never deleted*!\n\n\nPublishing\n==========\n\n1. Prepend notes to `CHANGELOG.md` about the new version\n2. `git commit`\n3. `git push` and wait for Travis to report success\n4. `git tag v1.x.y && git push --tags`\n5. Wait for Travis to push our changes to PyPI\n',
    'author': 'Adam Hooper',
    'author_email': 'adam@adamhooper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
