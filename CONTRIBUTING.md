# Contributing
![](https://cloud.githubusercontent.com/assets/1317406/12853560/606e97fa-cbfa-11e5-9af4-5458d9ba625b.png)

We love pull requests from everyone. If you have any questions about contributing, please ask; we're here to help!

First, fork and clone the repo. Set up your machine by following the steps in the README.

Install the dev requirements:

```bash
pip install -r dev-requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/
```

Make your change and format your change to conform to the current coding standards:

```bash
docformatter -r -i --no-blank --wrap-summaries 120 .
yapf --style="{based_on_style: pep8, column_limit: 120}" -r -i .
```

Push to your fork and [submit a pull request](https://help.github.com/articles/using-pull-requests/).

At this point you're waiting on us. We like to at least comment on pull requests
within three business days (and, typically, one business day). We may suggest
some changes or improvements or alternatives.

Some things that will increase the chance that your pull request is accepted:

* Keep the style consistent. (Like follow [PEP-8](http://www.python.org/dev/peps/pep-0008/) for Python code)
* Respect the indent and line ending settings of the project so that 
  extraneous changes do not cloud the real intent of your commits.
* Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).
* Commit in logical units. If you find yourself using "and" in a commit
  message (other than "Add/fix foo and add tests") you should probably
  break the work into multiple commits.
