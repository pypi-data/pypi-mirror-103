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

"""
This module provides the definitions for a settings container.

.. currentmodule:: hifis_surveyval.settings
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from datetime import datetime
from enum import Enum, auto, unique
from pathlib import Path
from typing import List, Set


@unique
class OutputFormat(Enum):
    """An Abstraction of the supported output formats for generated images."""

    SCREEN = auto()
    PDF = auto()
    PNG = auto()
    SVG = auto()

    @staticmethod
    def list_supported() -> str:
        """Generate a string listing the supported output formats."""
        values: List[str] = list(value.name for value in OutputFormat)
        return ", ".join(values)


class Settings(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbosity: int = logging.NOTSET

        # Path in which modules to be executed are located which defaults
        # to "scripts" folder.
        self.script_folder: Path = Path("scripts")

        # List of selected module names to be executed which defaults to
        # an empty list for all modules in the module folder.
        self.script_names: List[str] = []

        # The Format in which the data should be output
        self.output_format: OutputFormat = OutputFormat.SCREEN

        # Folder, into which the output file goes
        # if the output format is not screen
        self.output_folder: Path = Path("output")

        # The date prefix is used to identify the run
        # (e.g. for saving output images)
        self.run_timestamp: str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Path to sub-folder which holds all output files of a single
        # analysis run
        self.__analysis_output_path: Path = None

        # Set path to sub-folder and create sub-folder in one go
        self.analysis_output_path = self.output_folder / self.run_timestamp

        # Using a set for true_values and false_values to avoid duplicates and
        # because order does not matter
        self.true_values: Set[str] = {"True", "Yes", "Y", "On", "1"}
        """
        A set of strings to be interpreted as boolean 'True' when
        parsing the input data.
        """

        self.false_values: Set[str] = {"False", "No", "N", "Off", "0"}
        """
        A set of strings to be interpreted as boolean 'False' when
        parsing the input data.
        """

        # Add upper- and lowercase variants for
        # 'true_values' and 'false_values'.
        additional_lower: Set[str] = set(map(str.lower, self.true_values))
        additional_upper: Set[str] = set(map(str.upper, self.true_values))
        self.true_values.update(additional_lower.union(additional_upper))

        additional_lower: Set[str] = set(map(str.lower, self.false_values))
        additional_upper: Set[str] = set(map(str.upper, self.false_values))
        self.false_values.update(additional_lower.union(additional_upper))

    @property
    def analysis_output_path(self) -> Path:
        """
        Getter method of property.

        Returns:
            analysis_output_path (Path): Path to sub-folder which holds all
                                         output files of a single analysis run.
        """
        return self.__analysis_output_path

    @analysis_output_path.setter
    def analysis_output_path(self, analysis_output_path: Path) -> None:
        """
        Setter method of property that sets value only once and creates folder.

        This setter method not only sets the path of the analysis output folder
        once per analysis run but also takes care of the creation of the
        sub-folder as well.

        Args:
            analysis_output_path (Path): Path to sub-folder which holds all
                                         output files of a single analysis run.
        """
        if self.__analysis_output_path is None:
            self.__analysis_output_path = analysis_output_path
        self.__create_analysis_output_folder()

    def __create_analysis_output_folder(self) -> None:
        """
        Create a unique sub-folder to hold all output files of an analysis run.

        The sub-folder for the output of the analysis run is only created
        if path property is set and only created once per analysis run.
        """
        if self.analysis_output_path is not None:
            if not self.analysis_output_path.exists():
                self.analysis_output_path.mkdir(parents=True)
