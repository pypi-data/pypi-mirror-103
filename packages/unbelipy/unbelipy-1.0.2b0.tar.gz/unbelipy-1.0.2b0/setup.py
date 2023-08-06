# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unbelipy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0,<4.0.0', 'aiolimiter>=1.0.0b1,<2.0.0']

setup_kwargs = {
    'name': 'unbelipy',
    'version': '1.0.2b0',
    'description': "Asynchronous wrapper for UnbelievaBoat's API written in python",
    'long_description': '[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)\n\n[![PyPI status](https://img.shields.io/pypi/status/unbelipy.svg)](https://pypi.python.org/pypi/unbelipy/)\n[![PyPI version fury.io](https://badge.fury.io/py/unbelipy.svg)](https://pypi.python.org/pypi/unbelipy/)\n[![PyPI license](https://img.shields.io/pypi/l/unbelipy.svg)](https://pypi.python.org/pypi/unbelipy/)\n\n# unbelipy\n\nAsynchronous wrapper for UnbelievaBoat\'s API written in python\n\n## Characteristics\n- Easy to use\n- Full error handling\n- Type hinted readable code\n\n## Project status\nEarly beta may be used in production after extensive testing\n\n## Installation\n\n`pip install unbelipy`\n\n## Use:\n\n```python\nfrom unbelipy import UnbeliClient\nimport asyncio\nTOKEN = "Token generated through Unbelievaboat\'s portal"\n\nclient = UnbeliClient(token=TOKEN)\n\nasync def main():\n    # get guild information\n    guild_info = await client.get_guild(guild_id=305129477627969547)\n    print(guild_info)\n    # get guild leaderboard\n    guild_leaderboard = await client.get_leaderboard(guild_id=305129477627969547)\n    print(guild_leaderboard)\n    # get user balance\n    balance = await client.get_balance(guild_id=305129477627969547, member_id=80821761460928512)\n    print(balance)\n    # put balance (set to x amount)\n    balance = await client.set_balance(guild_id=305129477627969547, \n                                       member_id=80821761460928512,\n                                       cash=1000,\n                                       reason="Showing off put method")\n    # patch balance (increment or decrement by x amount)\n    balance = await client.edit_balance(guild_id=305129477627969547, \n                                       member_id=80821761460928512,\n                                       cash=-500,\n                                       reason="Showing off patch method")\n    print(balance)\n\nasyncio.run(main())\n```\n\n"balance" is a returned Dataclass with balance information containing:\n- total: total amount of currency (cash + bank)\n- bank: amount in bank\n- cash: amount in cash\n- user_id: id of the user for which the amount is set\n- guild_id: id for the guild the user belongs to\n- rank: rank of the user in the guild according to query parameters\n\n"guild_info" is a dataclass with guild info containing:\n- id\n- name \n- icon\n- owner_id  \n- member_count  \n- symbol (currency)\n\n### UnbeliClient init parameters:\n- `token` unbelivaboat\'s client token.\n- `prevent_rate_limits` (bool) if enabled (True, the default) the client will do its best \n  to prevent 429 type errors (rate limits). This will work even on concurrent tasts or loops.\n- `retry_rate_limits` (bool) if enabled (True, default is False) the client will retry requests after \n  getting a 429 error. It will sleep through the retry_after time stipulated by UnbelivaBoat\'s API\n  \n### UnbeliClient public attributes\n- `rate_limits`: this class features attributes about the state of each route. They Update after each request. \n  Bucket Attributes. Each of the following contain an async context manager to prevent 429s in case its enabled and \n  contain information about the specific route rate limit headers.\n    `rate_limits.get_balance`\n    `rate_limits.edit_balance`\n    `rate_limits.set_balance`\n    `rate_limits.get_leaderboard`\n    `rate_limits.get_guild`\n    `rate_limits.get_permissions`\n  rate limit Methods:\n    `rate_limits.currently_limited()` - returns a dictionary containing the bucket name, and a boolean indicating \n        if they\'re currently limited\n    `rate_limits.any_limited()` - returns a bool indicating if any bucket is currently being limited\n    `rate_limits.is_limited(name: str)` - returns a bool indicating if the specified bucket is being limited\n  \n# Know Issues:\n- `\'-Infinity\'` is accepted by the API as a parameter for cash or bank (edit_balance and set_balance), \n  but it doesn\'t work.\n- `client.edit_balace` which sends a patch request sometimes comes back with a 404 error even when \n  the url and data parameterns are correct, even on repeated requests with the exact same data.\n  \n# Credits\n- Currently global rate limit is handled by Martijn Pieters\' [aiolimiter](https://github.com/mjpieters/aiolimiter).',
    'author': 'chrisdewa',
    'author_email': 'alexdewa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrisdewa/unbelipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
