# refinebio-py

A python client for the refine.bio API.

## Usage

`pyrefinebio` can be installed via pip

```
$ pip install pyrefinebio
```

You can then import and start using it right away!

```python
import pyrefinebio

pyrefinebio.download_dataset(
    "./ds.zip",
    "foo@bar.com",
    dataset_dict={
        "SRP066781": ["ALL"]
    }
)
```

See the [documentation](https://alexslemonade.github.io/refinebio-py/index.html) for more help!

## Testing

Tests can be run with:

```
python -m unittest discover tests -b
```

## Releasing to PyPI

`pyrefinebio` can automatically be released to PyPI via a GitHub action.

To trigger the action, create a new release via GitHub:
- go to the [GitHub repo's release page](https://github.com/AlexsLemonade/refinebio-py/releases)
- click `Draft a new release`
- fill out the form
    - the Tag version should be in the form `vX.X.X`
- click `Publish release`
- the action should automatically be triggered

## Documentation

The docs are generated using [sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).

### Generating the Docs

Before you can generate the docs you must install pyrefienbio and sphinx requirements.

I recommend setting up a [virtual environment](https://docs.python.org/3/tutorial/venv.html)
before installing the requirements, but that step is optional.

To install the requirements:

```bash
$ pip install -r requirements.txt
$ pip install -r docs-requirements.txt
```

Then, to generate the docs navigate to `./docs` and run the command:

```
$ make html
```

The output will be in `./docs/_build`

Open `./docs/_build/html/*` in a browser to view the docs

### Deploying the Docs to Github Pages

First, set the variable `release` in `./docs/conf.py` to the correct version.

Then, clone the branch `gh-pages` into a folder `./doc-output`

You can use the following command to do this:

```
$ git clone --single-branch --branch gh-pages https://github.com/AlexsLemonade/refinebio-py.git doc-output
```

Navigate tho `./docs` and run the command:

```
$ make github
```

Navigate to `./doc-output` and commit and push any changes
