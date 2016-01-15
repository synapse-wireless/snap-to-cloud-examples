# Contributing
If you're interesting in contributing a fix or additional examples:

1. Install the dev requirements ```pip install -r dev-requirements.txt --extra-index-url https://update.synapse-wireless.com/pypi/```
1. Make your change
1. Format your change to conform to the current coding standards:
```sh
docformatter -r -i --no-blank --wrap-summaries 120 .
yapf --style="{based_on_style: pep8, column_limit: 120}" -r -i .
```