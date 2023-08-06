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
This module provides the global definitions for the project.

.. currentmodule:: hifis_surveyval.globals
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import Dict

from hifis_surveyval.core.settings import Settings
from hifis_surveyval.data import DataContainer
from hifis_surveyval.question import AbstractQuestion

#: A global copy-on-read container for providing the survey data
#: to the analysis functions
dataContainer: DataContainer = DataContainer()

#: The settings storage
settings: Settings = Settings()

#: All the survey questions and their associated answers
survey_questions: Dict[str, AbstractQuestion] = {}
