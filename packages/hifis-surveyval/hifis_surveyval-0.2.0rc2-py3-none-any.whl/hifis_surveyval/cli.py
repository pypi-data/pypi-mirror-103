#!/usr/bin/env python

# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.
    There is also a very helpful `tutorial video
    <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: hifis_surveyval.cli
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import logging
import sys
from pathlib import Path
from typing import List

import click
import pandas

from hifis_surveyval import dispatch, globals
from hifis_surveyval.metadata import (
    construct_questions_from_metadata,
    fetch_participant_answers,
)
from hifis_surveyval.settings import OutputFormat

from .__init__ import __version__


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    default=0,
    show_default=True,
    help="Enable verbose output. "
    "Increase verbosity by setting this option up to 3 times.",
)
@click.option(
    "--scripts",
    "-s",
    default="scripts",
    show_default=True,
    help="Select the folder containing analysis scripts.",
)
@click.option(
    "--names",
    "-n",
    multiple=True,
    default=[],
    help="Optionally select the specific script names contained "
    "in the scripts folder (while omitting file endings) "
    "which should be executed.",
)
@click.option(
    "--output-folder",
    "-o",
    default="output",
    show_default=True,
    help="Select the folder to put the generated output like plots " "into.",
)
@click.option(
    "--output-format",
    "-f",
    default="PNG",
    show_default=True,
    help=f"Designate output format. "
    f"Supported values are: {OutputFormat.list_supported()}.",
)
def cli(
    verbose: int, scripts: str, names: List[str], output_folder: str, output_format: str
) -> None:
    """Analyze a given CSV file with a set of independent python scripts."""
    # NOTE that click takes above documentation for generating help text
    # Thus the documentation refers to the application per se and not the
    # function (as it should)
    set_verbosity(verbose)
    set_output_format(output_format)

    logging.info(f"Selected script folder: {scripts}")
    globals.settings.script_folder = Path(scripts)
    logging.info(f"Selected output folder: {output_folder}")
    globals.settings.output_folder = Path(output_folder)
    # Set a list of selected module names contained in the module folder.
    globals.settings.script_names = names
    sys.path.insert(0, scripts)


@cli.command()
def version() -> None:
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))


@cli.command()
@click.argument("file_name", type=click.File(mode="r"))
@click.option(
    "--metadata",
    "-m",
    default="metadata/meta.yml",
    help="Give file name which contains survey metadata.",
)
def analyze(file_name, metadata: str) -> None:
    """
    Read the given files into global data and metadata objects.

    If the data file can not be parsed by Pandas, an error will be printed and
    the program will abort.
    If the metadata file can not be parsed, an error will be printed and
    the program will abort.
    """
    logging.info(f"Analyzing file {file_name.name}")
    try:
        frame: pandas.DataFrame = pandas.read_csv(
            file_name,
            true_values=globals.settings.true_values,
            false_values=globals.settings.false_values,
        )

        logging.debug("\n" + str(frame))

        # Put the Data Frame into the global container
        globals.dataContainer.set_raw_data(frame)
    except IOError:
        logging.error("Could not parse the given file as CSV")
        exit(1)

    logging.info(f"Attempt to load metadata from {metadata}")

    # Load survey metadata from given YAML file.
    try:
        construct_questions_from_metadata(Path(metadata))

        # When debugging, print all parsed Questions
        if globals.settings.verbosity == logging.DEBUG:
            logging.debug("Parsed Questions:")
            for question in globals.survey_questions.values():
                logging.debug(question)

        fetch_participant_answers()
    except IOError:
        logging.error("Could not parse the metadata file as YAML.")
        exit(1)

    dispatcher = dispatch.Dispatcher(
        globals.settings.script_folder, globals.settings.script_names
    )
    dispatcher.discover()
    dispatcher.load_all_modules()


def set_verbosity(verbose_count: int) -> None:
    """
    Interpret the verbosity option count.

    Set the log levels accordingly.
    The used log level is also stored in the settings.

    Args:
        verbose_count: the amount of verbose option triggers
    """
    verbosity_options: List[int] = [
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]

    max_index: int = len(verbosity_options) - 1

    # Clamp verbose_count to accepted values
    # Note that it shall not be possible to unset the verbosity.
    option_index: int = (
        0
        if verbose_count < 0
        else max_index
        if verbose_count > max_index
        else verbose_count
    )

    new_level: int = verbosity_options[option_index]
    logging.basicConfig(
        level=new_level,
        format="%(asctime)s "
        "[%(levelname)-8s] "
        "%(module)s.%(funcName)s(): "
        "%(message)s",
    )
    globals.settings.verbosity = new_level

    if not new_level == logging.ERROR:
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )


def set_output_format(output_format: str) -> None:
    """
    Attempt to determine the desired output format from the given string.

    The format name is not case sensitive.

    Args:
        output_format: A textual representation of the desired format.
    """
    try:
        chosen_format: OutputFormat = OutputFormat[output_format.upper()]
        globals.settings.output_format = chosen_format
        logging.info(f"Output format set to {chosen_format.name}")
    except KeyError:
        logging.error(
            f"Output Format {output_format} not recognized. "
            f"Supported values are: {OutputFormat.list_supported()}"
        )
        exit(2)
