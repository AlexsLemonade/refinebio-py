
.. _Using the CLI:

Using the CLI
=============

Before you can use the CLI to download Datasets and Compendia, you need to create and activate a Token.

See :ref:`Quickstart/Setting up Tokens` for a tutorial on setting up a Token.

Downloading Datasets
--------------------

After you set up and activate a Token you can use the CLI to start creating and downloading Datasets.

See :ref:`Quickstart/Setting up Tokens` for a tutorial on setting up a Token.

pyrefinebio provides the CLI command `download-dataset` for creating and downloading Datasets.
It will automatically handle every part of the creation and download process for you.
You will receive the Dataset as a zip file.

`download-dataset` requires that you pass in the options `email-address`, and either `experiments` or `dataset-dict`.

* `email_address` is the email address that will be notified when the Dataset is finished processing.

The options `experiments` and `dataset-dict` both control which Experiments and Samples will be a part of the Dataset.

* `experiments` can be used when you want to add specific Experiments to your Dataset. All the downloadable samples associated with the Experiments that you pass in will be added to the Dataset. 

The `experiments` option is just a space separated list of Experiment accession codes. Here's an example:

.. code-block:: shell

    $ refinebio download-datset --experiments "<Experiment 1 Accession Code> <Experiment 2 Accession Code>"


* `dataset-dict` should be used when you want to specify specific Samples to be included in the Dataset. However, you can pass in "ALL" instead of specific Sample accession codes to add all downloadable Samples associated with that Experiment to the Dataset.

The `dataset-dict` option is a JSON object in the following format:

.. code-block:: shell

    $ dataset-json='{"<Experiment 1 Accession Code>": ["<Sample 1 Accession Code>", "<Sample 2 Accession Code>"], "<Experiment 2 Accession Code>": ["ALL"]}'
    $ refinebio download-dataset --dataset-dict 

You can also pass in other optional command options to alter the Dataset itself and to alter how the download process works.

* `path` is the path that the Dataset will be downloaded to. You specify a path to a zip file or a directory. If you pass in a path to a directory, the name of the zip file will be automatically generated in the format `dataset-<dataset_id>.zip`. By default, `path` will be set to the current directory.

* `aggregation` can be used to change how the Dataset is aggregated. The default is "EXPERIMENT", and the other available choices are "SPECIES" and "ALL". For more information about Dataset aggregation check out `Aggregations`_.

* `transformation` can be used to change the transformation of the Dataset. The default is "NONE", and the other available choices are "MINMAX" and "STANDARD". For more information on Dataset transformation check out `Gene transformations`_. 

* `skip-quantile-normalization` can be used to choose whether or not quantile normalization is skipped for RNA-seq Samples. For more information check out `Quantile normalization`_.

* `extract` can be used to choose whether the downloaded zip file should be automatically extracted. It will automatically extract to the same location that you passed in as `path`. So if `path` is a zip file: `./path/to/dataset.zip` it will be extracted to the dir `./path/to/dataset/`, if `path` is a dir: `./path/to/dir/` it will be extracted to `./path/to/dir/[generated-file-name]/`. By default, `extract` is False. 

* `prompt` can be used to choose whether or not you should be prompted before downloading if the Dataset zip file is larger than 1 gigabyte. By default, `prompt` is True.

.. _Aggregations: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=aggregation#aggregations 

.. _Gene transformations: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=quantile#gene-transformations

.. _Quantile normalization: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=quantile%20normalization#quantile-normalization

Below is a simple example of downloading a Dataset using `experiments`:

.. code-block:: shell

    $ refinebio download-dataset --path "~/path/to/dataset/dir/" --email-address "foo@bar.com" --experiments "GSE74410 GSM604796 GSM604797"

Below is a simple example of downloading a Dataset using `dataset_dict`:

.. code-block:: shell

    $ dataset-json='{"GSE74410": ["ALL"], "GSE24528": ["GSM604796", "GSM604797"]}'
    $ refinebio download-dataset --path "./path/to/dataset.zip" --email-address "foo@bar.com" --dataset-dict $dataset-json


Downloading Compendia
---------------------

You can start using the CLI to download Compendia after you set up and activate a Token.

See :ref:`Quickstart/Setting up Tokens` for a tutorial on setting up a Token.

pyrefinebio provides the CLI command `download-compendium` for downloading Compendium results.
It will automatically search for Compendia based on organisms and download the results.
You will receive the Compendium as a zip file.

`download-compendium` requires that you pass in the parameter `organism`. 

* `organism` is the scientific name of the Organism for the Compendium that you want to download.

You can also pass in other optional parameters to alter the type of Compendium you download.

* `path` is the path that the Dataset will be downloaded to. You specify a path to a zip file or a directory. If you pass in a path to a directory, the name of the zip file will be automatically generated in the format `compendium-<compendium_id>.zip`. By default, `path` will be set to the current directory.

* `version` is the Compendium version. The default is `None` which will get the latest version.

* `quant-sf-only` can be used to choose if the Compendium is quantile normalized. Pass in True for RNA-seq Sample Compendium results or False for quantile normalized. By default, `quant_sf_only` is False. For more information on normalized vs RNA-seq compendia check out `refine.bio Compendia`_.

* `extract` can be used to choose whether the downloaded zip file should be automatically extracted. It will automatically extract to the same location that you passed in as `path`. So if `path` is a zip file: `./path/to/dataset.zip` it will be extracted to the dir `./path/to/dataset/`, if `path` is a dir: `./path/to/dir/` it will be extracted to `./path/to/dir/[generated-file-name]/`. By default, `extract` is False. 

* `prompt` can be used to choose whether or not you should be prompted before downloading if the Dataset zip file is larger than 1 gigabyte. By default, `prompt` is True.

.. _refine.bio Compendia: http://docs.refine.bio/en/latest/main_text.html#refine-bio-compendia

Below is a simple example of Downloading a Compendium result:

.. code-block:: shell

    $ refinebio download--compendium --path "~/path/to/dir/for/compendium/" --organism "HOMO_SAPIENS"

pyrefinebio also provides the CLI command `download-quantfile-compendium` which is equivalent to using
the command `download-compendium` with the option `quant-sf-only` set to True.

You can use this function when you want to be explicit to future users of your script that you are downloading quantfile Compendium results.

Below is a simple example of Downloading a Compendium result using `download-quantfile-compendium`:

.. code-block:: shell

    $ refinebio download-quantfile-compendium --path "~/path/to/dir/for/compendium/" --organism "HOMO_SAPIENS"

Getting Information About pyrefinebio Classes and Functions
-----------------------------------------------------------

If you are re-reading a script that you wrote and forget what a pyrefinebio function or class does -
or if you just want more information about a pyrefinebio class or function, pyrefinebio exposes its `help()` function
as the command `describe` which can print out information about all pyrefinebio classes/functions.

To get information about a function or class, just pass its name as the first argument to the command.

Here's an example:

.. code-block:: shell

    $ refinebio describe download_dataset 

This will print out information about the pyrefinebio `download_dataset()` function.

To get information about a class method, just pass in `<Class>.<method>` as the first argument to the command.

Here's an example:

.. code-block:: shell

    $ refinebio describe Sample.search 

This will print out information about the pyrefinebio class `Sample`'s search method.

