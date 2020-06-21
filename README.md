# PV226-Adapting process mining in JIRA
[![Build Status](https://travis-ci.org/MichalCervenansky/PV226-Process-mining-project.svg?branch=master)](https://travis-ci.org/MichalCervenansky/PV226-Process-mining-project)
### Project summary:
Goal of this project is to develop script, that enables gathering Jira issues selected by JQL to .xes format. This format can be visualized in process mining software like Disco.

### Installation and prerequisites:
* Clone this repository
* Install pipenv using `pip install pipenv`
* Locate Pipfile and change `python_version = "3.7"` to version of python3 installed on your computer. You can check your python version running `python --version`
* Run `pipenv install` to install all dependencies

### Usage:
* Run gather_jira.py with specified server, Jira query and optional output file name e.g.
`python jira-pm/__main__.py --jira-server https://issues.redhat.com --query 'project=WFLY AND type="Feature Request"'`
