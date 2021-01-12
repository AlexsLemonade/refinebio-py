# refinebio-py	
A python client for the refine.bio API.

## Documentation

The docs are generated using [sphinx autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html).

### Generating the Docs

To generate the docs navigate to `./docs` and run the command:

```
$ make html
```

The output will be in `./docs/_build`

Open `./docs/_build/html/*` in a browser to view the docs

### Deploying the Docs to Github Pages

Clone the branch `gh-pages` into a folder `./doc-output`

You can use the following command to do this:

```
$ git clone --single-branch --branch gh-pages https://github.com/AlexsLemonade/refinebio-py.git doc-output
```

Navigate tho `./docs` and run the command:

```
$ make github
```

Navigate to `./doc-output` and commit and push any changes
