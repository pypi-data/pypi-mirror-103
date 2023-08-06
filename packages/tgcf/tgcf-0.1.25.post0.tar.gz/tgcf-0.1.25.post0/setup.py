# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'plugins'}

packages = \
['tgcf', 'tgcf_filter', 'tgcf_replace']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.1.2,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Telethon>=1.20,<2.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cryptg>=0.2.post2,<0.3',
 'hachoir>=3.1.2,<4.0.0',
 'pydantic>=1.8.1,<2.0.0',
 'python-dotenv>=0.17.0,<0.18.0',
 'requests>=2.25.1,<3.0.0',
 'tg-login>=0.0.1,<0.0.2',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tgcf = tgcf.cli:app']}

setup_kwargs = {
    'name': 'tgcf',
    'version': '0.1.25.post0',
    'description': 'The ultimate tool to automate telegram message forwarding.',
    'long_description': '<!-- markdownlint-disable -->\n\n<p align="center">\n<a href = "https://github.com/aahnik/tgcf" > <img src = "https://user-images.githubusercontent.com/66209958/115183360-3fa4d500-a0f9-11eb-9c0f-c5ed03a9ae17.png" alt = "tgcf logo"  width=120> </a>\n</p>\n\n<h1 align="center"> tgcf </h1>\n\n<p align="center">\nThe ultimate tool to automate telegram message forwarding.\n</p>\n\n<p align="center"><a href="https://github.com/aahnik/tgcf/blob/main/LICENSE"><img src="https://img.shields.io/github/license/aahnik/tgcf" alt="GitHub license"></a>\n<a href="https://github.com/aahnik/tgcf/stargazers"><img src="https://img.shields.io/github/stars/aahnik/tgcf?style=social" alt="GitHub stars"></a>\n<a href="https://github.com/aahnik/tgcf/issues"><img src="https://img.shields.io/github/issues/aahnik/tgcf" alt="GitHub issues"></a>\n<img src="https://img.shields.io/pypi/v/tgcf" alt="PyPI">\n<a href="https://twitter.com/intent/tweet?text=Wow:&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf"><img src="https://img.shields.io/twitter/url?style=social&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf" alt="Twitter"></a></p>\n\n<br>\n\n<!-- markdownlint-enable -->\n\nThe *key features* are:\n\n1. Two **[modes of operation](https://github.com/aahnik/tgcf/wiki/Past-vs-Live-modes-explained)**\nare _past_ or _live_ for dealing with either existing or upcoming messages.\n2. Supports **[login](https://github.com/aahnik/tgcf/wiki/Login-with-a-bot-or-user-account)**\nwith both telegram _bot_ account as well as _user_ account.\n3. Custom **[filter](https://github.com/aahnik/tgcf/wiki/How-to-use-filters-%3F)  [replace](https://github.com/aahnik/tgcf/wiki/Text-Replacement-feature-explained)  [watermark](https://github.com/aahnik/tgcf/wiki/How-to-use--watermarking-%3F)  [ocr](https://github.com/aahnik/tgcf/wiki/You-can-do-OCR-!)** and whatever you need !\n4. Detailed **[docs 📚](https://github.com/aahnik/tgcf/wiki)** +\nVideo tutorial + Fast help in **[discussion forum 😎](https://github.com/aahnik/tgcf/discussions)**.\n5. If you are a python developer, writing **[plugins 🔌](https://github.com/aahnik/tgcf/wiki/How-to-write-a-plugin-for-tgcf-%3F)**\nis like stealing candy from a baby.\n\nWhat are you waiting for? Star 🌟 the repo and click Watch 🕵 to recieve updates.\n\nYou can also join the official [Telegram Channel](https://telegram.me/tg_cf),\nto recieve updates without any ads.\n\n<!-- markdownlint-disable -->\n## Video Tutorial 📺\n\nA youtube video is coming soon. [Subscribe](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg) to get notified.\n\n<!-- markdownlint-enable -->\n\n## Run Locally 🔥\n\n> **Note:** Make sure you have Python 3.8 or above installed.\nGo to [python.org](https://python.org) to download python.\n\nClick on your platform of choice for a more detailed guide.\n\n| Platform | Supported |\n| -------- | :-------: |\n| [Windows](https://github.com/aahnik/tgcf/wiki/Run-tgcf-on-Windows)  |     ✅    |\n| Mac      |     ✅     |\n| Linux    |     ✅     |\n| [Android](https://github.com/aahnik/tgcf/wiki/Run-on-Android-using-Termux)  |     ✅     |\n\nIf you are familiar with **Docker**, you may [go that way](https://github.com/aahnik/tgcf/wiki/Install-and-run-using-docker)\nfor an easier life.\n\nOpen your terminal and run the following commands.\n\n```shell\npip install --upgrade tgcf\n```\n\nTo check if the installation succeeded, run\n\n```shell\ntgcf --version\n```\n\nIf you see an error, that means installation failed.\n\n### Configuration 🛠️\n\nConfiguring `tgcf` is easy. You just need two files in your present directory\n(from which tgcf is invoked).\n\n- [`.env`](https://github.com/aahnik/tgcf/wiki/Environment-Variables) : To\ndefine your environment variables easily.\n\n- [`tgcf.config.yml`](https://github.com/aahnik/tgcf/wiki/How-to-configure-tgcf-%3F) :\nAn `yaml` file to configure how `tgcf` behaves.\n\n### Start `tgcf` ✨\n\nIn your terminal, just run `tgcf live` or `tgcf past` to start `tgcf`.\nIt will prompt you to enter your phone no. or bot token, when you run it\nfor the first time.\n\nFor more details run `tgcf --help` or [read docs](https://github.com/aahnik/tgcf/wiki/CLI-Usage).\n\n## Run on Cloud 🌩️\n\nDeploying to a cloud server is an easier alternative if you cannot install\non your own machine.\nCloud servers are very reliable and great for running `tgcf` in live mode\nfor a long time.\n\n<!-- markdownlint-disable -->\n\n| Platform                                                     | Pros                    | Cons                        |\n| ------------------------------------------------------------ | ----------------------- | --------------------------- |\n| <a href="https://github.com/aahnik/tgcf/wiki/Deploy-to-Heroku">   <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" width=155></a> | free for 450 hr/mo      | can\'t use tgcf in past mode |\n| <a href="https://github.com/aahnik/tgcf/wiki/Deploy-to-Digital-Ocean">  <img src="https://www.deploytodo.com/do-btn-blue.svg" alt="Deploy to DO" width=220></a> | speed and reliability   | starts from $5/mo           |\n| <a href="https://github.com/aahnik/tgcf/wiki/Run-for-free-on-Gitpod">  <img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Run on Gitpod" width=160></a> | easily edit config file | only 50 hr/mo free          |\n\n\n**Other options**\n\n- [Python Anywhere](https://github.com/aahnik/tgcf/wiki/Run-on-PythonAnywhere)\n- [Google Cloud Run](https://github.com/aahnik/tgcf/wiki/Run-on-Google-Cloud)\n- Scheduled using [GitHub Actions](https://github.com/aahnik/tgcf/wiki/Run-tgcf-in-past-mode-periodically)\n\n\n<!-- markdownlint-enable -->\n\n## Getting Help 💁🏻\n\n- First of all [read the wiki](https://github.com/aahnik/tgcf/wiki)\nand [watch the videos](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg)\nto get started.\n- Search your problem everywhere !\n- Feel free to ask your questions in the [Discussion forum](https://github.com/aahnik/tgcf/discussions/new).\n- For reporting bugs or requesting a feature please use the [issue tracker](https://github.com/aahnik/tgcf/issues/new)\nfor this repo.\n\n## Contributing 🙏\n\nPRs most welcome! Read the [contributing guidelines](/.github/CONTRIBUTING.md) to get started.\n\nAlso read:\n\n- [How to write a plugin for tgcf](https://github.com/aahnik/tgcf/wiki/How-to-write-a-plugin-for-tgcf-%3F)\n- [Package management with Poetry](https://python-poetry.org/docs/)\n- [Telethon documentation](https://docs.telethon.dev/en/latest/)\n\nIf you are not a developer, you may also contribute financially to\nincentivise the development of any custom feature you need.\n',
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aahnik/tgcf',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
