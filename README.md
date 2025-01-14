![Main CI](https://github.com/gibsramen/qadabra/actions/workflows/main.yml/badge.svg)

# Qadabra: **Q**uantitative **A**nalysis of **D**ifferential **Ab**undance **Ra**nks

##### (Pronounced *ka-da-bra*)

Qadabra is a Snakemake workflow for running and comparing several differential abundance (DA) methods on the same microbiome dataset.

Importantly, Qadabra focuses on both FDR corrected p-values *and* [feature ranks](https://www.nature.com/articles/s41467-019-10656-5) and generates visualizations of differential abundance results.

![Schematic](images/Qadabra_schematic.svg)

## Installation
```
pip install qadabra
```

Qadabra requires the following dependencies:
* snakemake
* click
* biom-format
* pandas
* numpy
* cython
* iow

## Usage

### 1. Creating the workflow directory

Qadabra can be used on multiple datasets at once.
First, we want to create the workflow directory to perfrom differential abundance with all methods:

```
qadabra create-workflow --workflow-dest <directory_name>
```

This command will initialize the workflow, but we still need to point to our dataset(s) of interest.

### 2. Adding a dataset

We can add datasets one-by-one with the `add-dataset` command:

```
qadabra add-dataset \
    --workflow-dest <directory_name> \
    --table <directory_name>/data/table.biom \
    --metadata <directory_name>/data/metadata.tsv \
    --tree <directory_name>/data/my_tree.nwk \
    --name my_dataset \
    --factor-name case_control \
    --target-level case \
    --reference-level control \
    --confounder confounding_variable(s) <confounding_var> \
    --verbose
```

Let's walkthrough the arguments provided here, which represent the inputs to Qadabra:

* `workflow-dest`: The location of the workflow that we created earlier
* `table`: Feature table (features by samples) in [BIOM](https://biom-format.org/) format
* `metadata`: Sample metadata in TSV format
* `tree`: Phylogenetic tree in .nwk or other tree format (optional)
* `name`: Name to give this dataset
* `factor-name`: Metadata column to use for differential abundance
* `target-level`: The value in the chosen factor to use as the target
* `reference-level`: The reference level to which we want to compare our target
* `confounder`: Any confounding variable metadata columns (optional)
* `verbose`: Flag to show all preprocessing performed by Qadabra

Your dataset should now be added as a line in `my_qadabra/config/datasets.tsv`. 

You can use `qadabra add-dataset --help` for more details. 
To add another dataset, just run this command again with the new dataset information.

### 3. Running the workflow

The previous commands will create a subdirectory, `my_qadabra` in which the workflow structure is contained.
From the command line, execute the following to start the workflow:
```
snakemake --use-conda --cores <number of cores preferred> <other options>
```
Please read the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/executing/cli.html) for how to run Snakemake best on your system.

When this process is completed, you should have directories `figures`, `results`, and `log`.
Each of these directories will have a separate folder for each dataset you added.

### 4. Generating a report

After Qadabra has finished running, you can generate a Snakemake report of the workflow with the following command:

```
snakemake --report report.zip
```

This will create a zipped directory containing the report.
Unzip this file and open the `report.html` file to view the report containing results and visualizations in your browser.

## Tutorial
See the [tutorial](tutorial.md) page for a walkthroughon using Qadabra workflow with a microbiome dataset.

## FAQs
Coming soon: An [FAQs](FAQs.md) page of commonly asked question on the statistics and code pertaining to Qadabra.

## Citation
The manuscript for Qadabra is currently in progress. Please cite this GitHub page if Qadabra is used for your analysis. This project is licensed under the MIT License. See the [license](LICENSE) file for details.