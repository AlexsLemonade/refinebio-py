
.. _Using the CLI:

Using the CLI
=============

Before you can use the CLI to download Datasets and Compendia, you need to create and activate a Token.

See :ref:`Using the CLI/Setting up Tokens` for information on setting up Tokens using the CLI.

Or you can go to :ref:`Quickstart/Setting up Tokens` for a tutorial on setting up a Token using python.


.. _Using the CLI/Setting up Tokens:

Setting up Tokens
-----------------

pyrefinebio provides the CLI command :code:`create-token` which can automatically create, activate, and save a Token for you.

By default, :code:`create-token` will prompt you before activating and saving the Token it creates.

Alternatively, it has the flag :code:`--silent` or :code:`-s` which you can use to bypass the prompts.

If you use the silent flag, the created Token will be automatically activated and saved to the config file located by default at :code:`~/.refinebio.yaml`.
You must save the Token in order for it to be used in future CLI commands.

For more information about pyrefinebio's Config see :ref:`Config`.

Here's an example of creating, activating, and saving a Token with prompts:

.. code-block:: shell

    $ refinebio create-token
    Please review the refine.bio Terms of Use: https://www.refine.bio/terms and Privacy Policy: https://www.refine.bio/privacy
    Do you understand and accept both documents? (y/N)y
    Would you like to save your Token to the Config file for future use? (y/N)y

Here's an example of creating, activating, and saving a Token without prompts:

.. code-block:: shell

    $ refinebio create-token -s


Downloading Datasets
--------------------

After you set up and activate a Token you can use the CLI to start creating and downloading Datasets.

See :ref:`Using the CLI/Setting up Tokens` for information on setting up Tokens using the CLI.

Or you can go to :ref:`Quickstart/Setting up Tokens` for a tutorial on setting up a Token using python.

pyrefinebio provides the CLI command :code:`download-dataset` for creating and downloading Datasets.
It will automatically handle every part of the creation and download process for you.
You will receive the Dataset as a zip file.

`download-dataset` requires that you pass in the options :code:`email-address`, and either :code:`experiments` or :code:`dataset-dict`.

* **email_address** - The email address that will be notified when the Dataset is finished processing.

The options :code:`experiments` and :code:`dataset-dict` both control which Experiments and Samples will be a part of the Dataset.

* **experiments** can be used when you want to add specific Experiments to your Dataset. All the downloadable samples associated with the Experiments that you pass in will be added to the Dataset. 

The :code:`experiments` option is just a space separated list of Experiment accession codes. Here's an example:

.. code-block:: shell

    $ refinebio download-dataset --experiments "<Experiment 1 Accession Code> <Experiment 2 Accession Code>"


* **dataset-dict** should be used when you want to specify specific Samples to be included in the Dataset. However, you can pass in "ALL" instead of specific Sample accession codes to add all downloadable Samples associated with that Experiment to the Dataset.

The :code:`dataset-dict` option is a JSON object in the following format:

.. code-block:: shell

    $ dataset-json='{"<Experiment 1 Accession Code>": ["<Sample 1 Accession Code>", "<Sample 2 Accession Code>"], "<Experiment 2 Accession Code>": ["ALL"]}'
    $ refinebio download-dataset --dataset-dict 

You can also pass in other optional command options to alter the Dataset itself and to alter how the download process works.

* **path** - The path that the Dataset will be downloaded to. You specify a path to a zip file or a directory. If you pass in a path to a directory, the name of the zip file will be automatically generated in the format :code:`dataset-<dataset_id>.zip`. By default, :code:`path` will be set to the current directory.

* **aggregation** - Can be used to change how the Dataset is aggregated. The default is "EXPERIMENT", and the other available choices are "SPECIES" and "ALL". For more information about Dataset aggregation check out `Aggregations`_.

* **transformation** - Can be used to change the transformation of the Dataset. The default is "NONE", and the other available choices are "MINMAX" and "STANDARD". For more information on Dataset transformation check out `Gene transformations`_. 

* **skip-quantile-normalization** - Can be used to disable quantile normalization for RNA-seq Samples, which is performed by default. For more information check out `Quantile normalization`_.

* **extract** - Can be used to choose whether the downloaded zip file should be automatically extracted. It will automatically extract to the same location that you passed in as :code:`path`. So if :code:`path` is a zip file: :code:`./path/to/dataset.zip` it will be extracted to the dir :code:`./path/to/dataset/`, if :code:`path` is a dir: :code:`./path/to/dir/` it will be extracted to :code:`./path/to/dir/[generated-file-name]/`. By default, :code:`extract` is False. 

* **prompt** - Can be used to choose whether or not you should be prompted before downloading if the Dataset zip file is larger than 1 gigabyte. By default, :code:`prompt` is True.

.. _Aggregations: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=aggregation#aggregations 

.. _Gene transformations: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=quantile#gene-transformations

.. _Quantile normalization: https://refinebio-docs.readthedocs.io/en/latest/main_text.html?highlight=quantile%20normalization#quantile-normalization

Below is a simple example of downloading a Dataset using :code:`experiments`:

.. code-block:: shell

    $ refinebio download-dataset --path "~/path/to/dataset/dir/" --email-address "foo@bar.com" --experiments "GSE74410 GSM604796 GSM604797"

Below is a simple example of downloading a Dataset using :code:`dataset_dict`:

.. code-block:: shell

    $ dataset-json='{"GSE74410": ["ALL"], "GSE24528": ["GSM604796", "GSM604797"]}'
    $ refinebio download-dataset --path "./path/to/dataset.zip" --email-address "foo@bar.com" --dataset-dict $dataset-json


Downloading Compendia
---------------------

You can start using the CLI to download Compendia after you set up and activate a Token.

See :ref:`Using the CLI/Setting up Tokens` for information on setting up Tokens using the CLI.

Or you can go to :ref:`Quickstart/Setting up Tokens` for a tutorial on setting up a Token using python.

pyrefinebio provides the CLI command :code:`download-compendium` for downloading Compendium results.
It will automatically search for Compendia based on organisms and download the results.
You will receive the Compendium as a zip file.

:code:`download-compendium` requires that you pass in the parameter :code:`organism`. 

* **organism** - The scientific name of the Organism for the Compendium that you want to download.

You can also pass in other optional parameters to alter the type of Compendium you download.

* **path** - The path that the Dataset will be downloaded to. You specify a path to a zip file or a directory. If you pass in a path to a directory, the name of the zip file will be automatically generated in the format :code:`compendium-<compendium_id>.zip`. By default, :code:`path` will be set to the current directory.

* **version** - The Compendium version. The default is :code:`None` which will get the latest version.

* **quant-sf-only** - Can be used to choose if the Compendium is quantile normalized. Pass in True for RNA-seq Sample Compendium results or False for quantile normalized. By default, :code:`quant_sf_only` is False. For more information on normalized vs RNA-seq compendia check out `refine.bio Compendia`_.

* **extract** - Can be used to choose whether the downloaded zip file should be automatically extracted. It will automatically extract to the same location that you passed in as :code:`path`. So if :code:`path` is a zip file: :code:`./path/to/dataset.zip` it will be extracted to the dir :code:`./path/to/dataset/`, if :code:`path` is a dir: :code:`./path/to/dir/` it will be extracted to :code:`./path/to/dir/[generated-file-name]/`. By default, :code:`extract` is False. 

* **prompt** - Can be used to choose whether or not you should be prompted before downloading if the Dataset zip file is larger than 1 gigabyte. By default, :code:`prompt` is True.

.. _refine.bio Compendia: http://docs.refine.bio/en/latest/main_text.html#refine-bio-compendia

Below is a simple example of Downloading a Compendium result:

.. code-block:: shell

    $ refinebio download--compendium --path "~/path/to/dir/for/compendium/" --organism "HOMO_SAPIENS"

pyrefinebio also provides the CLI command :code:`download-quantfile-compendium` which is equivalent to using
the command :code:`download-compendium` with the option :code:`quant-sf-only` set to True.

You can use this function when you want to be explicit to future users of your script that you are downloading quantfile Compendium results.

Below is a simple example of Downloading a Compendium result using :code:`download-quantfile-compendium`:

.. code-block:: shell

    $ refinebio download-quantfile-compendium --path "~/path/to/dir/for/compendium/" --organism "HOMO_SAPIENS"

Getting Information About pyrefinebio Classes and Functions
-----------------------------------------------------------

If you are re-reading a script that you wrote and forget what a pyrefinebio function or class does -
or if you just want more information about a pyrefinebio class or function, pyrefinebio exposes its :code:`help()` function
as the command :code:`describe` which can print out information about all pyrefinebio classes/functions.

To get information about a function or class, just pass its name as the first argument to the command.

Here's an example:

.. code-block:: shell

    $ refinebio describe download_dataset 

This will print out information about the pyrefinebio :code:`download_dataset()` function.

To get information about a class method, just pass in :code:`<Class>.<method>` as the first argument to the command.

Here's an example:

.. code-block:: shell

    $ refinebio describe Sample.search 

This will print out information about the pyrefinebio class :code:`Sample`'s search method.

