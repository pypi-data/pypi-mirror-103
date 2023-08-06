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
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tgcf = tgcf.cli:app']}

setup_kwargs = {
    'name': 'tgcf',
    'version': '0.1.25',
    'description': 'The ultimate tool to automate telegram message forwarding.',
    'long_description': '<!-- markdownlint-disable -->\n\n<p align="center">\n<a href = "https://github.com/aahnik/tgcf" > <img src = "https://user-images.githubusercontent.com/66209958/115183360-3fa4d500-a0f9-11eb-9c0f-c5ed03a9ae17.png" alt = "tgcf logo"  width=120> </a>\n</p>\n\n<h1 align="center"> tgcf </h1>\n\n<p align="center">\nThe ultimate tool to automate telegram message forwarding.\n</p>\n\n<p align="center"><a href="https://github.com/aahnik/tgcf/blob/main/LICENSE"><img src="https://img.shields.io/github/license/aahnik/tgcf" alt="GitHub license"></a>\n<a href="https://github.com/aahnik/tgcf/stargazers"><img src="https://img.shields.io/github/stars/aahnik/tgcf?style=social" alt="GitHub stars"></a>\n<a href="https://github.com/aahnik/tgcf/issues"><img src="https://img.shields.io/github/issues/aahnik/tgcf" alt="GitHub issues"></a>\n<img src="https://img.shields.io/pypi/v/tgcf" alt="PyPI">\n<a href="https://twitter.com/intent/tweet?text=Wow:&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf"><img src="https://img.shields.io/twitter/url?style=social&amp;url=https%3A%2F%2Fgithub.com%2Faahnik%2Ftgcf" alt="Twitter"></a></p>\n\n<br>\n\n<!-- markdownlint-enable -->\n\nThe *key features* are:\n\n1. Two [modes of operation](https://github.com/aahnik/tgcf/wiki/Past-vs-Live-modes-explained)\nare _past_ or _live_ for dealing with either existing or upcoming messages.\n2. Supports [signing in](https://github.com/aahnik/tgcf/wiki/Signing-in-with-a-bot-or-user-account)\nwith both telegram _bot_ account as well as _user_ account.\n3. Custom [Filtering](https://github.com/aahnik/tgcf/wiki/How-to-use-filters-%3F)\nof messages based on whitelist or blacklist.\n4. Modification of messages like [Text Replacement](https://github.com/aahnik/tgcf/wiki/Text-Replacement-feature-explained),\n[Watermarking](https://github.com/aahnik/tgcf/wiki/How-to-use--watermarking-%3F),\n[OCR](https://github.com/aahnik/tgcf/wiki/You-can-do-OCR-!) etc.\n5. Detailed **[documentation📖](https://github.com/aahnik/tgcf/wiki)** +\nVideo tutorial + Fast help in [discussion forum💬](https://github.com/aahnik/tgcf/discussions).\n6. If you are a python developer, writing [plugins🔌](https://github.com/aahnik/tgcf/wiki/How-to-write-a-plugin-for-tgcf-%3F)\nis like stealing candy from a baby.\n\nWhat are you waiting for? Star 🌟 the repo and click Watch 🕵 to recieve updates.\n\nYou can also join the official [Telegram Channel](https://telegram.me/tg_cf),\nto recieve updates without any ads.\n\n<!-- markdownlint-disable -->\n## Video Tutorial 📺\n\nA youtube video is coming soon. [Subscribe](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg) to get notified.\n\n<!-- markdownlint-enable -->\n\n## Run Locally 🔥\n\n> **Note:** Make sure you have Python 3.8 or above installed.\nGo to [python.org](https://python.org) to download python.\n\n| Platform | Supported |\n| -------- | :-------: |\n| Windows  |     ✅     |\n| Mac      |     ✅     |\n| Linux    |     ✅     |\n| [Android](https://github.com/aahnik/tgcf/wiki/Run-on-Android-using-Termux)  |     ✅     |\n\nIf you are familiar with **Docker**, you may [go that way](https://github.com/aahnik/tgcf/wiki/Install-and-run-using-docker)\nfor an easier life.\n\nOpen your terminal (command prompt) and run the following commands.\n\n```shell\npip install --upgrade tgcf\n```\n\nTo check if the installation succeeded, run\n\n```shell\ntgcf --version\n```\n\nIf you see an error, that means installation failed.\n\n### Configuration 🛠️\n\nConfiguring `tgcf` is easy. You just need two files in your present directory\n(from which tgcf is invoked).\n\n- [`.env`](https://github.com/aahnik/tgcf/wiki/Environment-Variables) : To\ndefine your environment variables easily.\n\n- [`tgcf.config.yml`](https://github.com/aahnik/tgcf/wiki/How-to-configure-tgcf-%3F) :\nAn `yaml` file to configure how `tgcf` behaves.\n\n### Start `tgcf` ✨\n\nIn your terminal, just run `tgcf live` or `tgcf past` to start `tgcf`.\n\nFor more details run `tgcf --help` or [read docs](https://github.com/aahnik/tgcf/wiki/CLI-Usage).\n\n## Run on cloud 🌩️\n\nDeploying to a cloud server is an easier alternative if you cannot install\non your own machine.\nCloud servers are very reliable and great for running `tgcf` in live mode.\n\nWhen you are deploying on a cloud platform, you can configure `tgcf`\nusing [environment variables](https://github.com/aahnik/tgcf/wiki/Environment-Variables).\nThe contents of [`tgcf.config.yml`](https://github.com/aahnik/tgcf/wiki/How-to-configure-tgcf-%3F)\ncan be put inside the environment variable called `TGCF_CONFIG`.\n\nYou may click on the platform name *(left coloumn)* to learn more about the\ndeployment process. Clicking on the "deploy" button *(right coloumn)* will\ndirectly deploy the application to that platform.\n\n<!-- markdownlint-disable -->\n\n<br>\n\n| Platform                                                     |                       One click deploy                       |\n| ------------------------------------------------------------ | :----------------------------------------------------------: |\n| [Heroku](https://github.com/aahnik/tgcf/wiki/Deploy-to-Heroku) | <a href="https://heroku.com/deploy?template=https://github.com/aahnik/tgcf">   <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku" width=155></a> |\n| [Digital Ocean](https://github.com/aahnik/tgcf/wiki/Deploy-to-Digital-Ocean) | <a href="https://cloud.digitalocean.com/apps/new?repo=https://github.com/aahnik/tgcf/tree/main">  <img src="https://www.deploytodo.com/do-btn-blue.svg" alt="Deploy to DO" width=220></a> |\n| [Google Cloud](https://github.com/aahnik/tgcf/wiki/Run-on-Google-Cloud) | <a href="https://deploy.cloud.run/?git_repo=https://github.com/aahnik/tgcf.git"> <img src="https://deploy.cloud.run/button.svg" alt="Run on Google Cloud" width=210></a> |\n| [Gitpod](https://github.com/aahnik/tgcf/wiki/Run-for-free-on-Gitpod) | <a href="https://gitpod.io/#https://github.com/aahnik/tgcf">  <img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Run on Gitpod" width=160></a> |\n\n<br>\n<!-- markdownlint-enable -->\n\nIf you need to run `tgcf` in past mode periodically, then you may set a cron job\nin your computer or  use [GitHub Actions](https://github.com/aahnik/tgcf/wiki/Run-tgcf-in-past-mode-periodically)\nto run a scheduled workflow.\n\n## Getting Help 💁🏻\n\n- First of all [read the wiki](https://github.com/aahnik/tgcf/wiki)\nand [watch](https://www.youtube.com/channel/UCcEbN0d8iLTB6ZWBE_IDugg) the videos.\n- If you still have doubts, you can try searching your problem in discussion\nforum or the issue tracker.\n- Feel free to ask your questions in the [Discussion forum](https://github.com/aahnik/tgcf/discussions/new).\n- For reporting bugs or requesting a feature please use the [issue tracker](https://github.com/aahnik/tgcf/issues/new)\nfor this repo.\n\nPlease do not send me direct messages on Telegram.\n(Exception: Sponsors can message me anytime)\n',
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
