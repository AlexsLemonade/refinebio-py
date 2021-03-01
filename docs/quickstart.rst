
Quickstart
==========

Installation
------------

pyrefinebio can be installed through PyPI:

.. code-block:: shell

   $ pip install pyrefinebio

.. _`Quickstart/Setting up Tokens`:

Setting up Tokens
-----------------

Before you start downloading or interacting with the API you should set up a Token.
Tokens will allow you to be able to download Compendia, Computed Files, and Datasets.

Creating and activating a refine.bio Token indicates agreement with refine.bio's `Terms of Use`_ and
`Privacy Policy`_ so make sure you have read and understood both before you continue.

.. _Terms of Use: https://www.refine.bio/terms
.. _Privacy Policy: https://www.refine.bio/privacy

To create a token, make an object of the Token class:

.. code-block:: python

    import pyrefinebio

    token = pyrefinebio.Token()

Then, to activate your token, call `agree_to_terms_and_conditions()` on it:

.. code-block:: python

    token.agree_to_terms_and_conditions()

Now, your Token is fully set up and will be used in any API requests made during the execution of this script.

If you want to use the same Token in future scripts, you can save it to the Config file:

.. code-block:: python

    token.save_token()

Now, the token will be automatically loaded every time you import pyrefinebio.

If you want to get access to the token that is saved to the config file in the future, you can load it:

.. code-block:: python

    token = pyrefinebio.Token.load_token()

For more information check out the :ref:`Token` class documentation and :ref:`Config`.

Downloading Datasets
--------------------

After you set up and activate a Token you can start creating and downloading Datasets.

pyrefinebio provides the function `download_dataset()` for creating and downloading Datasets.
It will will automatically handle every part of the creation and download process for you.
You will receive the Dataset as a zip file.

`download_dataset()` requires that you pass in the parameters `path`, `email_address`, and either `dataset_dict` or `experiments`.

* `path` is the path that the Dataset will be downloaded to. You specify a path to a zip file or a directory. If you pass in a path to a directory, the name of the zip file will be automatically generated in the format `dataset-<dataset_id>.zip`.

* `email_address` is the email address that will be notified when the Dataset is finished processing.

The parameters `experiments` and `dataset_dict` both control the which Experiments and Samples will be a part of the Dataset.

* `experiments` can be used when you want to add specific Experiments to your Dataset. All the downloadable samples associated with the Experiments that you pass in will be added to the Dataset. 

The `experiments` parameter is just a list of Experiment accession codes or pyrefinebio Experiment objects. Here's an example:

.. code-block:: python

    ex2 = pyrefinebio.Experiment.get("Experiment 2 Accession Code")

    exs = ["Experiment 1 Accession Code", ex2]

* `dataset_dict` should be used when you want to specify specific Samples to be included in the Dataset. It should be in the format:

.. code-block:: python

    dd = {
        "<Experiment 1 Accession Code>": [
            "<Sample 1 Accession Code>",
            "<Sample 2 Accession Code>"
        ],
        "<Experiment 2 Accession Code>": [
            "<Sample 3 Accession Code>",
            "<Sample 4 Accession code>"
        ]
    }


You can also pass in other optional parameters to alter the Dataset itself and to alter how the download process works.

* `aggregation` can be used to change how the Dataset is aggregated. The default is "EXPERIMENT", and the other available choices are "SPECIES" and "ALL". For more information about Dataset aggregation check out `Aggregations`_.

* `transformation` can be used to change the transformation of the Dataset. The default is "NONE", and the other available choices are "MINMAX" and "STANDARD". For more information on Dataset transformation check out `Gene transformations`_. 

* `skip_quantile_normalization` can be used to choose whether or not quantile normalization is skipped for RNA-seq Samples. For more information

* `extract` can be used to choose whether the downloaded zip file should be automatically extracted. It will automatically extract to the same location that you passed in as `path`. So if `path` is a zip file: `./path/to/dataset.zip` it will be extracted to the dir `./path/to/dataset/`, if `path` is a dir: `./path/to/dir/` it will be extracted to `./path/to/dir/[generated-file-name]/`. By default, `extract` is False. 

* `prompt` can be used to choose whether or not you should be prompted before downloading if the Dataset zip file is larger than 1 gigabyte. By default, `prompt` is True.

.. _Aggregations: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=aggregation#aggregations 

.. _Gene transformations: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=quantile#gene-transformations

Below is a simple example of downloading a Dataset using `experiments`:

.. code-block:: python

    pyrefinebio.download_dataset(
        "~/path/to/dir/for/dataset/",
        "foo@bar.com",
        experiments=["GSE24528", "GSE30631"]
    )

Below is a simple example of downloading a Dataset using `dataset_dict`:

.. code-block:: python

    pyrefinebio.download_dataset(
        "./path/to/dataset.zip",
        "foo@bar.com",
        dataset_dict={
            "GSE24528": [
                "GSM604796",
                "GSM604797"
            ]
        }
    )

Downloading Compendia
---------------------

You can start downloading Compendia after you set up and activate a Token.

pyrefinebio provides the function `download_compendium()` for downloading Compendium results.
It will will automatically search for Compendia based on organisms and download the results.
You will receive the Compendium as a zip file.

`download_compendium()` requires that you pass in the parameters `path` and `organism`. 

* `path` is the path that the Dataset will be downloaded to. You specify a path to a zip file or a directory. If you pass in a path to a directory, the name of the zip file will be automatically generated in the format `compendium-<compendium_id>.zip`.

* `organism` is the scientific name of the Organism for the Compendium that you want to download.

You can also pass in other optional parameters to alter the type of Compendium you download.

* `version` is the Compendium version. The default is `None` which will get the latest version.

* `quant_sf_only` can be used to choose if the Compendium is quantile normalized. Pass in True for RNA-seq Sample Compendium results or False for quantile normalized. By default, `quant_sf_only` is False. For more information on normalized vs RNA-seq compendia check out `refine.bio Compendia`_.

* `extract` can be used to choose whether the downloaded zip file should be automatically extracted. It will automatically extract to the same location that you passed in as `path`. So if `path` is a zip file: `./path/to/dataset.zip` it will be extracted to the dir `./path/to/dataset/`, if `path` is a dir: `./path/to/dir/` it will be extracted to `./path/to/dir/[generated-file-name]/`. By default, `extract` is False. 

* `prompt` can be used to choose whether or not you should be prompted before downloading if the Dataset zip file is larger than 1 gigabyte. By default, `prompt` is True.

.. _refine.bio Compendia: http://docs.refine.bio/en/latest/main_text.html#refine-bio-compendia

Below is a simple example of Downloading a Compendium result:

.. code-block:: python

    pyrefinebio.download_compendium(
        "./path/to/compendium.zip",
        "DANIO_RERIO",
    )

pyrefinebio also provides the function `download_quantfile_compendium()` which is equivalent to calling `download_compendium(quant_sf_only=True)`.

You can use this function when you want to be explicit to future users of your script that you are downloading quantfile Compendium results.

Below is a simple example of Downloading a Compendium result using `download_quantfile_compendium()`:

.. code-block:: python

    pyrefinebio.download_quantfile_compendium(
        "~/path/to/dir/for/compendium/",
        "HOMO_SAPIENS",
    )

Getting Help
------------

If you are re-reading a script that you wrote and forget what a pyrefinebio function or class does -
or if you just want more information about a pyrefinebio class or function, pyrefinebio has a `help()` function
that can print out information about all its classes/functions.

The `help()` function is probably most useful in the REPL.

Here's and example:

.. code-block:: shell

    >>> import pyrefinebio
    >>> pyrefinebio.help("download_dataset")

This will print out information about the `download_dataset()` function.

This is what the output looks like:

.. code-block:: shell

    download_dataset

        Automatically constructs a Dataset, processes it, waits for it
        to finish processing, then downloads it to the path specified.

        Returns:
            Dataset

        Parameters:
            path (str): the path that the Dataset should be downloaded to

            email_address (str): the email address that will be contacted with info
                                    related to the dataset
            
            dataset_dict (dict): a fully formed Dataset `data` attribute in the form:
                                    {
                                        "Experiment": [
                                            "Sample",
                                            "Sample"
                                        ]
                                    }
                                    use this parameter if you want to specify specific Samples
                                    for your dataset
                                    each part of the dict can be a pyrefinebio object or an accession
                                    code as a string

            experiments (list): a list of Experiments that should be added to the dataset
                                use this parameter if you only care about the Experiments - all 
                                available samples related to each Experiment will be added  
                                the list can contain Experiment objects or accession codes as strings

            aggregation (str): how the Dataset should be aggregated - by `EXPERIMENT` or by `SPECIES`

            transformation (str): the transformation for the dataset - `NONE`, `MINMAX`, or `STANDARD`

            skip_quantile_normalization (bool): control whether or not the dataset should skip quantile
                                                normalization for RNA-seq Samples

            extract (bool): if true, the downloaded zip file will be automatically extracted

            prompt (bool): if true, will prompt before downloading files bigger than 1GB

You can also get info on class methods by passing in `class.method` to the help function.

Here's an example:

.. code-block:: shell

    >>> import pyrefinebio
    >>> pyrefinebio.help("Sample.search")

Getting Started with the CLI
----------------------------

pyrefinebio provides a CLI that exposes the `download_dataset()`, `download_compendium()`, `download_quantfile_compendium()`, and `help()` functions.

Each function has its own command: `download-dataset`, `download-compendium`, `download-quantfile-compendium`, and `describe`, respectively.

To use the CLI just type `refinebio COMMAND` into a shell.

Each command has the option `--help` which will print out usage information and descriptions for every available option for that command.

If you want usage examples and a more in depth look at each CLI command you can also check out :ref:`Using the CLI`.

Here's an example of downloading a Dataset using the CLI:

.. code-block:: shell

    $ refinebio download-dataset --path "./path/to/dataset.zip" --email-address "foo@bar.com" --dataset-dict '{"GSE74410": ["ALL"]}'

Interacting with the API
------------------------

You can use pyrefinebio to interact with all endpoints of the refine.bio API.

Each endpoint is its own pyrefinebio class.

Most classes provide the `get()` and `search()` methods.

Use `get()` to get one refine.bio API object based on its identifying property.

Here's an example with a refine.bio Sample:

.. code-block:: python

    sample = pyrefinebio.Sample.get("GSM604797")

Use `search()` to look for refine.bio API objects based on filters.

`search()` will return a PaginatedList which can be indexed and iterated through like a regular python list.
For more info checkout the :ref:`PaginatedList` documentation.

Here's an example of searching for a refine.bio Sample:

.. code-block:: python

    samples = pyrefinebio.Sample.search(organism="HOMO_SAPIENS", is_processed=True)
    sample = samples[0]

Other classes provide additional methods like `download()` or `extract()`.

For more information checkout the :ref:`Classes` documentation.

Advanced Dataset Usage
----------------------

pyrefinebio offers the `download_dataset()` function which takes care of creating the Dataset, processing it, waiting for it to finish,
downloading it, and optionally extracting it - all automatically. 

If you only want to do a certain part of this process, however, you can do each step manually as well.

To manually create a Dataset, first create an object of the Dataset class:

.. code-block:: python

    dataset = pyrefinebio.Dataset()

Before you are able to process the Dataset you must add an email address and Experiments/Samples to it.

You can add the email address when creating the Dataset object by passing it into the constructor.
Or you can just set the attribute after creating the object.

Here's an example of both:

.. code-block:: python

    # using the constructor
    dataset = pyrefinebio.Dataset(email_address="foo@bar.com")

    # setting the attribute
    dataset = pyrefinebio.Dataset()
    dataset.email_address = "foo@bar.com"

You can add Experiments and Samples to your dataset by manually setting its `data` attribute or by using the `add_samples()` method.

Here's an example of manually setting its `data`:

.. code-block:: python

    dataset.data = {
        "GSE24528": [
            "GSM604796",
            "GSM604797"
        ]
    }

Here's an example of using the `add_samples()` method.
Notice that `add_samples()` can take pyrefinebio objects as arguments as well as accession codes.

.. code-block:: python

    s = pyrefinebio.Sample.search(experiment_accession_code="GSE60783", is_processed=True)

    dataset.add_samples(
        "GSE60783",
        samples=[s[0], s[1]]
    )

Once you have set the email address and added Experiments/Samples to you Dataset,
you can then start processing the Dataset using the `process()` method:

.. code-block:: python

    dataset.process()

You can check if the Dataset has finished at any time by calling the `check()` method on it:

.. code-block:: python

    if datset.check():
        # do something...

Then once the Dataset has finished processing, you can download it using the `download()` method:

.. code-block:: python

    dataset.download("./path/to/dataset.zip")

Once the Dataset has been downloaded, you can extract the downloaded zip file with the `extract()` method:

.. code-block:: python

    dataset.extract()

For more information checkout the :ref:`Dataset` documentation.
