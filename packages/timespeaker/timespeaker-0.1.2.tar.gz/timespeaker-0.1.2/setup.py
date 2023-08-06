# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['timespeaker']
install_requires = \
['gtts>=2.1.1,<3.0.0', 'pyttsx3>=2.90,<3.0']

setup_kwargs = {
    'name': 'timespeaker',
    'version': '0.1.2',
    'description': 'Announce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak.',
    'long_description': "# TimeSpeaker\n\nAnnounce the time every hour similar to Mac OS X. Say the Time using Google TTS or espeak.\n\n# Requirements\n\n- python3.6+\n- playsound\n- gtts or pyttsx3\n\nFor development\n\n- poetry \n- flake8\n- black\n- pytest\n\n# TODO\n\n- Use python: [threading.Timer](https://docs.python.org/3/library/threading.html?highlight=timer#threading.Timer)\n- Create tests\n- Update/Fix to PyPi (`pip install timespeaker`)\n- Move Makefile to Parent\n- Configure PULL_REQUESTS AND ISSUES template\n- Configure lint\n- Configure github actions (or circleci)\n- Test i3 configs\n- Add support to Cron\n- Use a global DEBUG\n- When merge to `main` build and publish to PyPi (github actions)\n\n# Install\n\n## Default (Working In Progress)\n\n```\npip install timespeaker\n```\n\n## Local\n\n```bash\n# pyenv shell +3.6.0\npython -m venv .venv \nmake install\n```\n\n# Configure\n\n## AutoStart (Working In Progress)\n\n```\nmake configure-autostart\n```\n\n## i3 (Working In Progress)\n\n```\nmake configure-i3\n```\n\n## Cron (Working In Progress)\n\nComing Soon\n\n```\nsudo make configure-cron\n```\n\n## Systemd (Working In Progress)\n\n```\nsudo make configure-systemd\n```\n\n## Remove configurations\n\n```\n# Systemd\nsudo make remove-systemd\n\n# Autostart\nmake remove-autostart\n\n# i3\n# coming soon\n\n# Cron\n# coming soon\n```\n\n# Usage\n\nDefault usage using gtts to speak and saving in `/tmp/timespeaker/`\n```\npython -m timespeaker start\n\n# OR if configured\n\ntimespeaker start\n```\n\nCustom command:\n```\npython -m timespeaker start --speaker=pyttsx3 --path-folder=/tmp/timespeaker/\n```\n\n# Development\n\nUsing virtualenv:\n\n```\n# create virtualenv\n# virtualenv .venv [-p /path/to/python3.6+] # require virtualenv\npython -m venv .venv\n\n# Enter virtualenv\nsource .venv/bin/activate\n\n# to exit of virtual env run \ndeactivate\n```\n\nDev install (poetry required)\n```\npoetry install\n```\n\nSee more commands with\n```\nmake help\n```\n\n# Tests\n\n```\nmake tests \n```\n\n# License\n\nMIT LICENSE\n\n# Contributing\n\nI encourage you to contribute to this project! Join us!\n\nTrying to report a possible security vulnerability? [Open a issue now](https://github.com/wallacesilva/timespeaker/issues/new)\n\nEveryone interacting in this project and its sub-projects' codebases, issue trackers, chat rooms, and mailing lists is expected to follow the code of conduct (building, but respect everyone).\n",
    'author': 'Wallace Silva',
    'author_email': 'contact@wallacesilva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wallacesilva/timespeaker/',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
