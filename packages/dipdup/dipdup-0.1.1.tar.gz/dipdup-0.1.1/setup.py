# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dipdup', 'dipdup.datasources', 'dipdup.datasources.tzkt']

package_data = \
{'': ['*'], 'dipdup': ['configs/*', 'templates/*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'aiomysql>=0.0.21,<0.0.22',
 'aiosignalrcore>=0.9.2,<0.10.0',
 'asyncpg>=0.22.0,<0.23.0',
 'datamodel-code-generator>=0.10.0,<0.11.0',
 'pydantic>=1.8.1,<2.0.0',
 'ruamel.yaml>=0.17.2,<0.18.0',
 'tortoise-orm>=0.17.1,<0.18.0']

entry_points = \
{'console_scripts': ['dipdup = dipdup.cli:cli']}

setup_kwargs = {
    'name': 'dipdup',
    'version': '0.1.1',
    'description': 'Python SDK for developing indexers of Tezos smart contracts inspired by The Graph',
    'long_description': '# dipdup\n\n[![PyPI version](https://badge.fury.io/py/dipdup.svg?)](https://badge.fury.io/py/dipdup)\n[![Tests](https://github.com/dipdup-net/dipdup-py/workflows/Tests/badge.svg?)](https://github.com/baking-bad/dipdup/actions?query=workflow%3ATests)\n[![Docker Build Status](https://img.shields.io/docker/cloud/build/bakingbad/dipdup)](https://hub.docker.com/r/bakingbad/dipdup)\n[![Made With](https://img.shields.io/badge/made%20with-python-blue.svg?)](ttps://www.python.org)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\nPython SDK for developing indexers of [Tezos](https://tezos.com/) smart contracts inspired by [The Graph](https://thegraph.com/).\n\n## Installation\n\nPython 3.8+ is required for dipdup to run.\n\n```shell\n$ pip install dipdup\n```\n\n## Creating indexer\n\nIf you want to see dipdup in action before diving into details you can run a demo project and use it as reference. Clone this repo and run the following command in it\'s root directory: \n\n```shell\n$ dipdup -c src/demo_hic_et_nunc/dipdup.yml run\n```\n\nExamples in this guide are simplified Hic Et Nunc demo.\n\n### Write configuration file\n\nCreate a new YAML file and adapt the following example to your needs:\n\n```yaml\nspec_version: 0.0.1\npackage: demo_hic_et_nunc\n\ndatabase:\n  kind: sqlite\n  path: db.sqlite3\n\ncontracts:\n  HEN_objkts: \n    address: ${HEN_OBJKTS:-KT1RJ6PbjHpwc3M5rw5s2Nbmefwbuwbdxton}\n    typename: hen_objkts\n  HEN_minter: \n    address: ${HEN_MINTER:-KT1Hkg5qeNhfwpKW4fXvq7HGZB9z2EnmCCA9}\n    typename: hen_minter\n\ndatasources:\n  tzkt_mainnet:\n    kind: tzkt\n    url: ${TZKT_URL:-https://staging.api.tzkt.io}\n\nindexes:\n  hen_mainnet:\n    kind: operation\n    datasource: tzkt_mainnet\n    contract: HEN_minter\n    handlers:\n      - callback: on_mint\n        pattern:\n          - destination: HEN_minter\n            entrypoint: mint_OBJKT\n          - destination: HEN_objkts\n            entrypoint: mint\n```\n\nEach handler in index config matches an operation group based on operations\' entrypoints and destination addresses in pattern. Matched operation groups will be passed to handlers you define.\n\n### Initialize project structure\n\nRun the following command replacing `config.yml` with path to YAML file you just created:\n\n```shell\n$ dipdup -c config.yml init\n```\n\nThis command will create a new package with the following structure (some lines were omitted for readability):\n\n```\ndemo_hic_et_nunc/\n├── handlers\n│   ├── on_mint.py\n│   └── on_rollback.py\n├── hasura-metadata.json\n├── models.py\n└── types\n    ├── hen_minter\n    │   ├── storage.py\n    │   └── parameter\n    │       └── mint_OBJKT.py\n    └── hen_objkts\n        ├── storage.py\n        └── parameter\n            └── mint.py\n```\n\n`types` directory is Pydantic dataclasses of contract storage and parameter. This directory is autogenerated, you shouldn\'t modify any files in it. `models` and `handlers` modules are placeholders for your future code and will be discussed later.\n\nYou could invoke `init` command on existing project (must be in your `PYTHONPATH`. Do it each time you update contract addresses or models. Code you\'ve wrote won\'t be overwritten.\n\n### Define models\n\nDipdup uses [Tortoise](https://tortoise-orm.readthedocs.io/en/latest/) under the hood, fast asynchronous ORM supporting all major database engines. Check out [examples](https://tortoise-orm.readthedocs.io/en/latest/examples.html) to learn how to use is.\n\nNow open `models.py` file in your project and define some models:\n```python\nfrom tortoise import Model, fields\n\n\nclass Holder(Model):\n    address = fields.CharField(58, pk=True)\n\n\nclass Token(Model):\n    id = fields.BigIntField(pk=True)\n    creator = fields.ForeignKeyField(\'models.Holder\', \'tokens\')\n    supply = fields.IntField()\n    level = fields.BigIntField()\n    timestamp = fields.DatetimeField()\n```\n\n### Write event handlers\n\nNow take a look at `handlers` module generated by `init` command. When operation group matching `pattern` block of corresponding handler at config will arrive callback will be fired. This example will simply save minted Hic Et Nunc tokens and their owners to the database:\n\n```python\nfrom demo_hic_et_nunc.models import Holder, Token\nfrom demo_hic_et_nunc.types.hen_minter.parameter.mint_objkt import MintOBJKT\nfrom demo_hic_et_nunc.types.hen_objkts.parameter.mint import Mint\nfrom dipdup.models import HandlerContext, OperationContext\n\n\nasync def on_mint(\n    ctx: HandlerContext,\n    mint_objkt: OperationContext[MintOBJKT],\n    mint: OperationContext[Mint],\n) -> None:\n    holder, _ = await Holder.get_or_create(address=mint.parameter.address)\n    token = Token(\n        id=mint.parameter.token_id,\n        creator=holder,\n        supply=mint.parameter.amount,\n        level=mint.data.level,\n        timestamp=mint.data.timestamp,\n    )\n    await token.save()\n```\n\nHandler name `on_rollback` is reserved by dipdup, this special handler will be discussed later.\n\n### Atomicity and persistency\n\nHere\'s a few important things to know before running your indexer:\n\n* __WARNING!__ Make sure that database you\'re connecting to is used by dipdup exclusively. When index configuration or models change the whole database will be dropped and indexing will start from scratch.\n* Do not rename existing indexes in config file without cleaning up database first, didpup won\'t handle this renaming automatically and will consider renamed index as a new one.\n* Multiple indexes pointing to different contracts must not reuse the same models because synchronization is performed by index first and then by block.\n* Reorg messages signal about chain reorganizations, when some blocks, including all operations, are rolled back in favor of blocks with higher weight. Chain reorgs happen quite often, so it\'s not something you can ignore. You have to handle such messages correctly, otherwise you will likely accumulate duplicate data or, worse, invalid data. By default Dipdup will start indexing from scratch on such messages. To implement your own rollback logic edit generated `on_rollback` handler.\n\n### Run your dapp\n\nNow everything is ready to run your indexer:\n\n```shell\n$ dipdup -c config.yml run\n```\n\nParameters wrapped with `${VARIABLE:-default_value}` in config could be set from corresponding environment variables. For example if you want to use another TzKT instance:\n\n```shell\n$ TZKT_URL=https://api.tzkt.io dipdup -c config.yml run\n```\n\nYou can interrupt indexing at any moment, it will start from last processed block next time you run your app again.\n\nUse `docker-compose.yml` included in this repo if you prefer to run dipdup in Docker:\n\n```shell\n$ docker-compose build\n$ # example target, edit volumes section to change dipdup config\n$ docker-compose up hic_et_nunc\n```\n\nFor debugging purposes you can index specific block range only and skip realtime indexing. To do this set `first_block` and `last_block` fields in index config.\n\n### Index templates\n\nSometimes you need to run multiple indexes with similar configs whose only difference is contract addresses. In this case you can use index templates like this:\n\n```yaml\ntemplates:\n  trades:\n    kind: operation\n    datasource: tzkt_staging\n    contract: < dex >\n    handlers:\n      - callback: on_fa12_token_to_tez\n        pattern:\n          - destination: < dex >\n            entrypoint: tokenToTezPayment\n          - destination: < token >\n            entrypoint: transfer\n      - callback: on_fa20_tez_to_token\n        pattern:\n          - destination: < dex >\n            entrypoint: tezToTokenPayment\n          - destination: < token >\n            entrypoint: transfer\n\nindexes:\n  trades_fa12:\n    template: trades\n    values:\n      dex: FA12_dex\n      token: FA12_token\n\n  trades_fa20:\n    template: trades\n    values:\n      dex: FA20_dex\n      token: FA20_token\n```\n\nTemplate values mapping could be accessed from within handlers at `ctx.template_values`.\n\n### Optional: configure Hasura GraphQL Engine\n\nWhen using PostgreSQL as a storage solution you can use Hasura integration to get GraphQL API out-of-the-box. Add the following section to your config, Hasura will be configured automatically when you run your indexer.\n\n```yaml\nhasura:\n  url: http://hasura:8080\n  admin_secret: changeme\n```\n\nWhen using included docker-compose example make sure you run Hasura first:\n\n```shell\n$ docker-compose up -d hasura\n```\n\nThen run your indexer and navigate to `127.0.0.1:8080`.\n\n### Optional: configure logging\n\nYou may want to tune logging to get notifications on errors or enable debug messages. Specify path to Python logging config in YAML format at `--logging-config` argument. Default config to start with:\n\n```yml\n  version: 1\n  disable_existing_loggers: false\n  formatters:\n    brief:\n      format: "%(levelname)-8s %(name)-35s %(message)s"\n  handlers:\n    console:\n      level: INFO\n      formatter: brief\n      class: logging.StreamHandler\n      stream : ext://sys.stdout\n  loggers:\n    SignalRCoreClient:\n      formatter: brief\n    dipdup.datasources.tzkt.datasource:\n      level: INFO\n    dipdup.datasources.tzkt.cache:\n      level: INFO\n  root:\n    level: INFO\n    handlers:\n      - console\n```\n\n## Contribution\n\nTo set up development environment you need to install [poetry](https://python-poetry.org/docs/#installation) package manager and GNU Make. Then run one of the following commands at project\'s root:\n\n```shell\n$ # install project dependencies\n$ make install\n$ # run linters\n$ make lint\n$ # run tests\n$ make test cover\n$ # run full CI pipeline\n$ make\n```\n\n## Contact\n* Telegram chat: [@baking_bad_chat](https://t.me/baking_bad_chat)\n* Slack channel: [#baking-bad](https://tezos-dev.slack.com/archives/CV5NX7F2L)\n\n## About\nThis project is maintained by [Baking Bad](https://baking-bad.org/) team.\nDevelopment is supported by [Tezos Foundation](https://tezos.foundation/).\n',
    'author': 'Lev Gorodetskiy',
    'author_email': 'github@droserasprout.space',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pytezos.org',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
