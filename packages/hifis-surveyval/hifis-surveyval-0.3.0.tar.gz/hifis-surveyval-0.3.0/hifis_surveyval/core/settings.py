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
This module handles settings.

It provides:
* settings classes
* getter for settings
* an export function to create a file

.. currentmodule:: hifis_surveyval.core.settings
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from datetime import datetime
from enum import Enum, auto, unique
from pathlib import Path
from typing import Any, Dict, List, Set

import yaml
from pydantic import BaseSettings, validator

config_filename = Path("hifis-surveyval.yml")


@unique
class OutputFormat(Enum):
    """An Abstraction of the supported output formats for generated images."""

    SCREEN = auto()
    PDF = auto()
    PNG = auto()
    SVG = auto()

    @staticmethod
    def list_supported() -> Set:
        """Generate a set listing the supported output formats."""
        return {value.name for value in OutputFormat}


class FileSettings(BaseSettings):
    """Settings, that the user can change."""

    # Path to metadata
    METADATA: Path = Path("metadata/meta.yml")
    # Path in which modules to be executed are located which defaults
    # to "scripts" folder.
    SCRIPT_FOLDER: Path = Path("scripts")

    # List of selected module names to be executed which defaults to
    # an empty list for all modules in the module folder.
    SCRIPT_NAMES: List[str] = []

    # The Format in which the data should be output
    OUTPUT_FORMAT: Any = OutputFormat.PNG

    @validator("OUTPUT_FORMAT", pre=True)
    def set_output_format(cls, to_validate) -> OutputFormat:
        """Parse format to enum object."""
        if isinstance(to_validate, OutputFormat):
            return to_validate
        for output_format in OutputFormat:
            if to_validate == output_format.name:
                return output_format
        raise ValueError(
            f"Wrong output format. Only {OutputFormat.list_supported()} are implemented"
        )

    # Folder, into which the output file goes
    # if the output format is not screen
    OUTPUT_FOLDER: Path = Path("output")

    class Config:
        """Subclass for specification."""

        case_sensitive = True


class Settings(FileSettings):
    """Settings, that are either static or can be changed via the cli interface."""

    VERBOSITY: int = logging.NOTSET

    # The date prefix is used to identify the run
    # (e.g. for saving output images)
    RUN_TIMESTAMP: str = None

    @validator("RUN_TIMESTAMP", pre=True)
    def set_timestamp(cls, to_validate) -> str:
        """Get the current datetime."""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Path to sub-folder which holds all output files of a single
    # analysis run
    ANALYSIS_OUTPUT_PATH: Path = None

    @validator("ANALYSIS_OUTPUT_PATH")
    def assemble_output_path(cls, to_validate, values: Dict[str, Any]) -> Path:
        """Assemble path from user settings and datetime."""
        return values.get("OUTPUT_FOLDER") / values.get("RUN_TIMESTAMP")

    # Using a set for true_values and false_values to avoid duplicates and
    # because order does not matter
    TRUE_VALUES: Set[str] = {"True", "Yes", "Y", "On", "1"}
    """
    A set of strings to be interpreted as boolean 'True' when
    parsing the input data.
    """

    FALSE_VALUES: Set[str] = {"False", "No", "N", "Off", "0"}
    """
    A set of strings to be interpreted as boolean 'False' when
    parsing the input data.
    """

    @validator("FALSE_VALUES", "TRUE_VALUES", pre=True)
    def case_insensitive_values(cls, to_validate) -> Set:
        """Extend list of values to match all cases."""
        additional_lower: Set[str] = set(map(str.lower, to_validate))
        additional_upper: Set[str] = set(map(str.upper, to_validate))
        to_validate.update(additional_lower.union(additional_upper))
        return to_validate


def create_config_file():
    """Create a file to store the config."""
    default_settings = Settings()
    config_dict = {}
    for key in FileSettings.__fields__:
        value = default_settings.__getattribute__(key)
        if isinstance(value, OutputFormat):
            config_dict[key] = value.name
        elif isinstance(value, Path):
            config_dict[key] = str(value)
        else:
            config_dict[key] = value

    with open(config_filename, "w") as config_file:
        yaml.dump(config_dict, config_file)


def get_settings() -> Settings:
    """Return an instance of Settingss."""
    settings: Settings = Settings()

    if Path.is_file(config_filename):
        with open(config_filename, "r") as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
        settings = Settings(**config)

    return settings
