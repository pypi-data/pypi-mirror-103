# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunkai',
 'bunkai.algorithm',
 'bunkai.algorithm.bunkai_sbd',
 'bunkai.algorithm.bunkai_sbd.annotator',
 'bunkai.algorithm.lbd',
 'bunkai.algorithm.tsunoda_sbd',
 'bunkai.algorithm.tsunoda_sbd.annotator',
 'bunkai.base',
 'bunkai.experiment',
 'bunkai.experiment.convert',
 'bunkai.third']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.2,<0.6.0',
 'emoji>=1.2.0',
 'emojis>=0.6.0',
 'janome>=0.4.1,<0.5.0',
 'more_itertools>=8.6.0,<9.0.0',
 'numpy>=1.16.0,<2.0.0',
 'seqeval>=1.2.2,<2.0.0',
 'spans>=1.1.0,<2.0.0',
 'torch>=1.3.0,<2.0.0',
 'tqdm',
 'transformers>=4.3.2,<5.0.0']

entry_points = \
{'console_scripts': ['bunkai = bunkai.cli:main']}

setup_kwargs = {
    'name': 'bunkai',
    'version': '1.1.2',
    'description': 'Sentence boundary disambiguation tool for Japanese texts',
    'long_description': '# Bunkai\n\n[![PyPI version](https://badge.fury.io/py/bunkai.svg)](https://badge.fury.io/py/bunkai)\n[![Python Versions](https://img.shields.io/pypi/pyversions/bunkai.svg)](https://pypi.org/project/bunkai/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n\n[![CircleCI](https://circleci.com/gh/megagonlabs/bunkai.svg?style=svg&circle-token=c555b8070630dfe98f0406a3892fc228b2370951)](https://app.circleci.com/pipelines/github/megagonlabs/bunkai)\n[![Maintainability](https://api.codeclimate.com/v1/badges/640b02fa0164c131da10/maintainability)](https://codeclimate.com/github/megagonlabs/bunkai/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/640b02fa0164c131da10/test_coverage)](https://codeclimate.com/github/megagonlabs/bunkai/test_coverage)\n[![markdownlint](https://img.shields.io/badge/markdown-lint-lightgrey)](https://github.com/markdownlint/markdownlint)\n[![jsonlint](https://img.shields.io/badge/json-lint-lightgrey)](https://github.com/dmeranda/demjson)\n[![yamllint](https://img.shields.io/badge/yaml-lint-lightgrey)](https://github.com/adrienverge/yamllint)\n\nBunkai is a sentence boundary (SB) disambiguation tool for Japanese texts.\n\n## Quick Start\n\n```console\n$ pip install -U bunkai\n$ echo -e \'宿を予約しました♪!まだ2ヶ月も先だけど。早すぎかな(笑)楽しみです★\\n2文書目の先頭行です。▁改行はU+2581で表現します。\' \\\n    | bunkai\n宿を予約しました♪!│まだ2ヶ月も先だけど。│早すぎかな(笑)│楽しみです★\n2文書目の先頭行です。▁│改行はU+2581で表現します。\n```\n\nFeed a document as one line by using ``▁`` (U+2581) for line breaks.\nThe output shows sentence boundaries with ``│`` (U+2502).\n\nIf you want to disambiguate  sentence boundaries for line breaks, please add a `--model` option with the path to the model.\nFirst time, please setup a  model.\n\n```console\n$ bunkai --model bunkai-model-directory --setup\n```\n\nThen, please designate the directory.\n\n```console\n$ echo -e "文の途中で改行を▁入れる文章ってありますよね▁それも対象です。" | bunkai --model bunkai-model-directory\n文の途中で改行を▁入れる文章ってありますよね▁│それも対象です。\n```\n\nFor more information, see [examples](example) or [documents](docs).\n\n## References\n\n- Yuta Hayashibe and Kensuke Mitsuzawa.\n    Sentence Boundary Detection on Line Breaks in Japanese.\n    Proceedings of The 6th Workshop on Noisy User-generated Text (W-NUT 2020), pp.71-75.\n    November 2020.\n    [[PDF]](https://www.aclweb.org/anthology/2020.wnut-1.10.pdf)\n    [[bib]](https://www.aclweb.org/anthology/2020.wnut-1.10.bib)\n\n## License\n\nApache License 2.0\n',
    'author': 'Yuta Hayashibe',
    'author_email': 'hayashibe@megagon.ai',
    'maintainer': 'Yuta Hayashibe',
    'maintainer_email': 'hayashibe@megagon.ai',
    'url': 'https://github.com/megagonlabs/bunkai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
