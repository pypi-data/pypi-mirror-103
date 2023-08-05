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
This module provides the definitions for a data container.

The container is meant to serve as the data source for the individual analysis
functions.

.. currentmodule:: hifis_surveyval.data
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

from typing import Dict

from pandas import DataFrame

from .answer import AnswerType


class DataContainer(object):
    """
    The data container holds the data read from the command line.

    It can hand out copies of the data frame so the using function can
    manipulate it in any desired way without interfering with other users.
    The initial data frame used is empty.
    """

    ID_COLUMN_NAME: str = "id"

    def __init__(self):
        """
        Populate the data container with an empty Pandas data frame.

        The frame is supposed to be filled via set_raw_data().
        """
        self._raw_data: DataFrame = DataFrame()

    @property
    def empty(self) -> bool:
        """
        Check if the container holds any data.

        This is considered to be the case if the stored data frame is empty.
        returns: True, if the container is considered empty, False otherwise
        """
        return self._raw_data.empty

    def set_raw_data(self, data_frame: DataFrame):
        """
        Try to set the current raw data frame.

        The data frame stored in the container will only be changed if:
        * The currently stored raw data frame is empty and
        * The provided data frame is not empty
        Otherwise, nothing will be done.
        Attempting to override an already set data frame will result in a
        RuntimeError.

        The ID column will be set as index column for the data frame.

        parameter: data_frame is the new frame to be stored in the container.
        """
        if data_frame.empty:
            return

        if self.empty:
            self._raw_data = data_frame
            self._raw_data.set_index(DataContainer.ID_COLUMN_NAME, inplace=True)
        else:
            raise RuntimeError("Do not re-assign the global data frame")

    @property
    def raw_data(self) -> DataFrame:
        """
        Provide a deep copy of the whole raw data frame.

        It is recommended to cache this copy as long as it is used.
        returns: A copy of the complete Pandas raw data frame.
        """
        return self._raw_data.copy(deep=True)

    def data_for_question(self, question_id: str) -> Dict[str, AnswerType]:
        """
        Obtain the data for each participant for a given question.

        Args:
            question_id: The string used to identify the question.

        Returns:
            An association from participant's ID to the answer the participant
            gave.
            The result may still contain "N/A" or "nan".
        """
        if (
            question_id == DataContainer.ID_COLUMN_NAME
            or question_id not in self._raw_data
        ):
            raise ValueError(f"{question_id} is not a valid question ID")

        per_participant_data: Dict[str, AnswerType] = {}
        column = self._raw_data[question_id]
        for participant in self._raw_data.index:
            per_participant_data[participant] = column[participant]

        return per_participant_data
