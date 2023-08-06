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
This module provides the functions to set up the environment.

It adds the script folder to PATH and creates required folders.

.. currentmodule:: hifis_surveyval.core.environment
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
import sys

from hifis_surveyval.globals import settings


def prepare_environment() -> None:
    """
    Prepare the runtime environment.

    * setting sys path to load scripts
    * creating output folder to save images
    """
    # set syspath to later on load scripts
    sys.path.insert(0, settings.SCRIPT_FOLDER)

    # create folder to output the results
    if settings.ANALYSIS_OUTPUT_PATH is not None:
        if not settings.ANALYSIS_OUTPUT_PATH.exists():
            settings.ANALYSIS_OUTPUT_PATH.mkdir(parents=True)
