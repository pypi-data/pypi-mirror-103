<!--
hifis-surveyval
Framework to help developing analysis scripts for the HIFIS Software survey.

SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
-->

# HIFIS-Surveyval

This project is used to develop analysis scripts for the HIFIS Software survey.

## Table of Content

* [Installation](#installation)
* [Getting Started](#getting-started)
* [Development](#development)
* [Start Analysis from Command-Line-Interface](#start-analysis-from-command-line-interface)
* [Contribute with Own Analysis Scripts](#contribute-with-own-analysis-scripts)
* [Resources](#resources)
* [License](#license)

## Getting Started

The project's documentation contains a section to help you
[get started](TODO) as a developer or
user of the analysis scripts.

## Installation
To install the package locally, you can either use [poetry](https://python-poetry.org/)
or `pip`.

### Using pip

```shell
pip install hifis-surveyval
```

After the installation, you can use the tool from the command line with `hifis-surveyval --help`.

### Using poetry

```shell
git clone $PATH_TO_THIS_PROJECT
cd hifis-surveyval
poetry install --no-dev
```

After the installation, you can use the tool from the command line with `poetry run hifis-surveyval --help`
The following documentation references the pip installation.
You can use the same commands with a poetry installation, if you refix you commands with `poetry run COMMAND`.

## Development
If you want to actively contribute changes to the project, you are required to
also install the development packages.
Therefore, use below extended installation options.

```shell
poetry install
```

This installs some packages that are required for performing quality checks.
Usually they are also performed via GitLab CI, but can also be executed locally.

It is common practice to run some checks locally before pushing them online.
Therefore, execute below commands:
```console
$ # Order your imports
$ isort -rc .
$ make lint
```

## Start Analysis from Command-Line-Interface

The survey analysis package is a program to be executed on the
Command-Line-Interface (CLI).

### Quick Start Example: Run Analysis

In order to run the survey analysis you need to copy the data-CSV-file 
for example from the 
[wiki page](https://gitlab.hzdr.de/hifis/survey-about-current-development-practice/-/wikis/home) 
of the associated GitLab project 
[Survey about current Development Practice](https://gitlab.hzdr.de/hifis/survey-about-current-development-practice)
into a central location like the [data/](data/) sub-folder of your local python 
project and tell the program the path to that data file.

Now you can do the following to start the survey analysis from the CLI:

```shell script
hifis-surveyval analyze data/<data_file_name>.csv
```

It tells the program that you would like to do the analysis,
where to find the analysis scripts, the _metadata_-file as well as 
the _data_-file to be taken into account for the analysis.

**Caution:** 
Depending on the Operating System used an issue with the file 
encoding might occur.
There might be data-CSV-files around which are encoded with `UTF-8-BOM`
which causes errors when read in on Windows OS.
In this case you need to change the encoding to `UTF-8` before running
the survey analysis.

### Flags

The program accepts a couple of flags:

1. Help flag
2. Verbosity flag
3. Scripts flag
4. Names flag
5. Output Folder flag
6. Output Format flag

#### Help flag

Calling the program with the _help_-flag is the first thing to do
when being encountered with this program.
It outputs a so-called _Usage_-message to the CLI:

```shell script
$ hifis-surveyval --help
Usage: hifis-surveyval [OPTIONS] COMMAND [ARGS]...

  Analyze a given CSV file with a set of independent python scripts.

Options:
  -v, --verbose             Enable verbose output. Increase verbosity by
                            setting this option up to 3 times.  [default: 0]

  -s, --scripts TEXT        Select the folder containing analysis scripts.
                            [default: scripts]

  -n, --names TEXT          Optionally select the specific script names
                            contained in the scripts folder (while omitting
                            file endings) which should be executed.

  -o, --output-folder TEXT  Select the folder to put the generated output like
                            plots into.  [default: output]

  -f, --output-format TEXT  Designate output format. Supported values are:
                            SCREEN, PDF, PNG, SVG.  [default: screen]

  --help                    Show this message and exit.

Commands:
  analyze  Read the given files into global data and metadata objects.
  version  Get the library version.
```

#### Verbosity flag

The _verbosity_-flag can be provided in order to specify the verbosity
of the output to the CLI.
This flag is called `--verbose` or `-v` for short:

```shell script
hifis-surveyval --verbose <COMMAND>
```
```shell script
hifis-surveyval -v <COMMAND>
```

The verbosity of the output can be increased even more 
by duplicating the flag `--verbose` or `-v` up to two times:

```shell script
hifis-surveyval --verbose --verbose --verbose <COMMAND>
```
```shell script
hifis-surveyval -vvv <COMMAND>
```

#### Scripts flag

Beside verbosity there is a _scripts_-flag called `--scripts` or 
`-s` for short:

```shell script
hifis-surveyval --scripts "scripts" <COMMAND>
```
```shell script
hifis-surveyval -s "scripts" <COMMAND>
```

This will tell the program in which folder to look for the actual 
analysis scripts.
In case the _scripts_-flag is omitted it defaults to sub-folder `scripts/`.

#### Names flag

There is also a _names_-flag called `--names` or `-n` for short:

```shell script
hifis-surveyval --names "example_script_1" --names "example_script_2" <COMMAND>
```
```shell script
hifis-surveyval -n "example_script_1" -n "example_script_2" <COMMAND>
```

This will tell the program which scripts in the scripts folder to execute.
In case the _names_-flag is omitted it defaults to all scripts in the
scripts folder.

#### Output Folder flag

The _output-folder_-flag called `--output-folder` or `-o` for short 
is another option:

```shell script
hifis-surveyval --output-folder "output" <COMMAND>
```
```shell script
hifis-surveyval -o "output" <COMMAND>
```

This will tell the program in which folder to put the generated output 
like plots into.
In case the _output-folder_-flag is omitted it defaults to sub-folder 
`output/`.

#### Output format flag

The user is also able to let the application know in which output format the
diagrams should be generated during the analysis. 
For this purpose there is a flag called `--output-format` or `-f` for short.
Allowed values to this flag are the following:
* SCREEN
* PDF
* PNG
* SVG

On the CLI the actual call looks like this:

```shell script
hifis-surveyval --output-format PNG <COMMAND>
```
```shell script
hifis-surveyval -f PNG <COMMAND>
```

### Commands

There are two different commands implemented which come with different
flags and parameters:

1. Command _version_
2. Command _analyze_

#### Command _version_
 
The `version` command outputs the version number of 
this CLI-program like so:

```shell script
hifis-surveyval version
0.0.1
```

#### Command _analyze_

The more interesting command is the `analyze` command
which comes with a _metadata_-flag `--metadata` or `-m` for short and 
a _data_-parameter.
In case the _metadata_-flag is omitted it assumes the following
path to the metadata file: 
`metadata/HIFIS_Software_Survey_2020_Questions.yml`.
The _data_-parameter can _not_ be omitted and need to be given explicitly
in order to be able to start the analysis.
This is an example of how to do the analysis:

```shell script
hifis-surveyval analyze data/<data_file_name>.csv
```

## Contribute with Own Analysis Scripts

### Essential Criteria for Developing Own Analysis Scripts

As you might have read in the previous sections the actual analysis scripts 
reside in a specific folder called `scripts/`.
All scripts in that folder will be automatically discovered by the package 
`hifis-surveyval` when running the analysis.
In order that the program recognizes the scripts in that folder as
analysis scripts they need to fulfil the following two criteria:

1. The filename need to end on `.py`.
2. The file need to contain a function called `run` without any parameters.

```python
"""
A dummy script for testing the function dispatch

.. currentmodule:: hifis_surveyval.scripts.dummy
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

def run():
    print("Example Script")
```

If both criteria are satisfied the program will execute the `run`-functions
of the analysis scripts in an arbitrary sequence.

### File-System Structure of Core Component

```shell script
$ tree hifis_surveyval/
hifis_surveyval/
├── answer.py
├── cli.py
├── data.py
├── dispatch.py
├── globals.py
├── metadata.py
├── question.py
├── settings.py
└── version.py
```

### Files and Classes Explained

**ToDo**: This section need to be extended to all files and classes
found in package `hifis_surveyval`.

#### Classes to Represent Questions

File `question.py` contains the following classes:
- `AbstractQuestion`: Abstract class providing properties of a question 
like `id` and `text`.
- `Question`: Non-abstract class inheriting from abstract-base-class
`AbstractQuestion`. It represents a question with associated answers.
- `QuestionCollection`: Non-abstract class inheriting from abstract-base-class
`AbstractQuestion`. It represents a question with associated sub-questions.

#### Class to Represent Answers

File `answer.py` contains class `Answer`.
This class provides properties of an answer like `id` and `text`.

## Resources

Below are some handy resource links.

* [Project Documentation](TODO)
* [Click](https://click.palletsprojects.com/en/7.x) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## License

Copyright © 2021 HIFIS Software <support@hifis.net>

This work is licensed under the following license(s):
* Everything else is licensed under [GPL-3.0-or-later](LICENSES/GPL-3.0-or-later.txt)

Please see the individual files for more accurate information.

> **Hint:** We provided the copyright and license information in accordance to the [REUSE Specification 3.0](https://reuse.software/spec/).