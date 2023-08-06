# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api_schemas', 'api_schemas.compilers']

package_data = \
{'': ['*']}

install_requires = \
['Mako>=1.1.4,<2.0.0', 'autopep8>=1.5.6,<2.0.0', 'lark-parser>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'api-schemas',
    'version': '0.1.3',
    'description': 'Create an intermediate representation of an api schema, that can be used to generate code.',
    'long_description': '# API schemas\n\nCreate an intermediate representation of an api schema, that can be used to generate code.\n\n**In other words**: Same what OpenAPI has already but with fewer options.\n\n**But why?**: Because it is fun 😎\n\n## Example API schema\n```\ntypedef Example\n    a: str\n    b: int\n    c: float\n    d: any\n    e: D {A, B, C}\n    f: E\n        Z = v v\n        ?g[]: bool\n        i: str\n            type = Date\n            format = yyyy-mm-dd HH:MM:ss.SSS\n        j: $Week\n\ntypedef Date str\n    type = Datetime\n    format = yyyy-mm-dd HH:MM:ss.SSS\n    \ntypedef Week {Monday, Tuesday, Wednesday}\n\ntypedef Q\n    a: $Example\n    b: $Date\n    \ntypedef QQ $Q\n\nserver = http://localhost:5000/api/v1\n\npeople\n    uri: /people/<name>\n    GET\n        ->\n        <-\n            200\n                data: $Example\n            404\n                err_msg: str\n            500\n                err_msg: str\n                \nWS\n    ->\n        a\n            i: str\n            b: Name\n                x: str\n                i: int\n        join_team\n            num: str\n    <-\n        update\n            i[]: int\n\n```\n\n## Changelog\n\n### 0.1.3\n\n- Add compilers to build dataclasses for python and dart\n- Add Websocket support\n- Allow Communications that are an array instead of an object',
    'author': 'JulianSobott',
    'author_email': 'julian.sobott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JulianSobott/api_schemas',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
