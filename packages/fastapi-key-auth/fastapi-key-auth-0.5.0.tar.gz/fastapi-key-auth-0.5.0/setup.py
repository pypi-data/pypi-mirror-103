# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_key_auth']

package_data = \
{'': ['*']}

install_requires = \
['starlette==0.13.6']

setup_kwargs = {
    'name': 'fastapi-key-auth',
    'version': '0.5.0',
    'description': 'API key validation Middleware',
    'long_description': "## FastAPI-Key-Auth\n\n```python\nfrom fastapi import FastAPI\nfrom fastapi_key_auth import AuthorizerMiddleware\n\napp = FastAPI()\n\napp.add_middleware(AuthorizerMiddleware)\n```\n\nAn api key in `headers['x-api-key']` is validated against all values in your apps environment variables starting\nwith `API_KEY_` before passing it on to your `app`.\nIf the api key is not present, ergo invalid, it will return a `401 Unauthorized`.\n",
    'author': 'Benjamin Ramser',
    'author_email': 'legionaerr@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/iwpnd/fastapi-key-auth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
