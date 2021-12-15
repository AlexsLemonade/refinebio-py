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

The docs can be found at https://alexslemonade.github.io/refinebio-py/index.html

The docs are generated using [sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).

### Generating the Docs

The docs are regenerated and pushed to Github Pages on every master deploy.
