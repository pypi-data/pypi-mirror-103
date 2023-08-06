# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beanie',
 'beanie.executors',
 'beanie.migrations',
 'beanie.migrations.controllers',
 'beanie.odm']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'motor>=2.1.0,<3.0.0',
 'pydantic>=1.8,<2.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['beanie = beanie.executors.migrate:migrations']}

setup_kwargs = {
    'name': 'beanie',
    'version': '0.4.3',
    'description': 'Asynchronous Python ODM for MongoDB',
    'long_description': '[![Beanie](https://raw.githubusercontent.com/roman-right/beanie/main/assets/logo/with_text.svg)](https://github.com/roman-right/beanie)\n\n[Beanie](https://github.com/roman-right/beanie) - is an Asynchronous Python object-document mapper (ODM) for MongoDB, based on [Motor](https://motor.readthedocs.io/en/stable/) and [Pydantic](https://pydantic-docs.helpmanual.io/).\n\nWhen using Beanie each database collection has a corresponding `Document` that is used to interact with that collection.\nIn addition to retrieving data, Beanie allows you to add, update, or delete documents from the collection as well.\n\nBeanie saves you time by removing boiler-plate code and it helps you focus on the parts of your app that actually matter.\n\nData and schema migrations are supported by Beanie out of the box.\n\n### Installation\n\n#### PIP\n\n```shell\npip install beanie\n```\n\n#### Poetry\n\n```shell\npoetry add beanie\n```\n\n### Quick Start\n\n```python\nfrom typing import Optional, List\n\nimport motor\nfrom beanie import Document, init_beanie\nfrom pydantic import BaseModel\n\n\nclass Tag(BaseModel):\n    name: str\n    color: str\n\n\nclass Note(Document):\n    title: str\n    text: Optional[str]\n    tag_list: List[Tag] = []\n\n\nasync def main():\n    # Crete Motor client\n    client = motor.motor_asyncio.AsyncIOMotorClient(\n        "mongodb://user:pass@host:27017"\n    )\n    \n    # Init beanie with the Note document class\n    await init_beanie(database=client.db_name, document_models=[Note])\n\n    # Get all the notes\n    all_notes = await Note.find_all().to_list()\n```\n\n### Documentation\n\n#### ODM\n- **[Tutorial](https://roman-right.github.io/beanie/tutorial/odm/)** - ODM usage examples\n- **[API](https://roman-right.github.io/beanie/documentation/odm/)** - Full list of the ODM classes and\n  methods with descriptions\n\n#### Migrations\n- **[Tutorial](https://roman-right.github.io/beanie/tutorial/odm/)** - Migrations usage examples\n\n### Example Projects\n\n- **[FastAPI Demo](https://github.com/roman-right/beanie-fastapi-demo)** - Beanie and FastAPI collaboration demonstration. CRUD and Aggregation.\n- **[Indexes Demo](https://github.com/roman-right/beanie-index-demo)** - Regular and Geo Indexes usage example wrapped to a microservice. \n\n### Articles\n\n- **[Announcing Beanie - MongoDB ODM](https://dev.to/romanright/announcing-beanie-mongodb-odm-56e)**\n- **[Build a Cocktail API with Beanie and MongoDB](https://developer.mongodb.com/article/beanie-odm-fastapi-cocktails/)**\n- **[MongoDB indexes with Beanie](https://dev.to/romanright/mongodb-indexes-with-beanie-43e8)**\n- **[Beanie Projections. Reducing network and database load.](https://dev.to/romanright/beanie-projections-reducing-network-and-database-load-3bih)**\n\n### Resources\n\n- **[GitHub](https://github.com/roman-right/beanie)** - GitHub page of the project\n- **[Changelog](https://roman-right.github.io/beanie/changelog)** - list of all the valuable changes\n- **[Discord](https://discord.gg/ZTTnM7rMaz)** - ask your questions, share ideas or just say `Hello!!`\n\n----\nSupported by [JetBrains](https://jb.gg/OpenSource)\n\n[![JetBrains](https://raw.githubusercontent.com/roman-right/beanie/main/assets/logo/jetbrains.svg)](https://jb.gg/OpenSource)\n',
    'author': 'Roman',
    'author_email': 'roman-right@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/roman-right/beanie',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
