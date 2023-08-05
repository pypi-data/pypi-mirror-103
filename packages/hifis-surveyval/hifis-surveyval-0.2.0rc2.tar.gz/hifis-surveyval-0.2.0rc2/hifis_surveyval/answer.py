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
This module contains a class to represent survey answers.

.. currentmodule:: hifis_surveyval.answer
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""
from typing import List, Optional, Union

#: Type to represent raw answer data.
#: Supported datatypes of answer data are str, float, int, bool.
AnswerType: type = Union[str, float, int, bool]
#: Representation of type alias 'AnswerType' as a list of type strings.
#: Supported datatypes of answer data are str, float, int, bool.
ValidAnswerTypes: List[str] = ["str", "float", "int", "bool"]


class Answer(object):
    """
    The Answer-class models responses to survey question.

    The use-case is twofold:
    * Answers may be used to represent pre-defined answers which could be
      selected by users
    * Answers also represent - when associated with a participant - the actual
      selection a user made.
    """

    def __init__(
        self,
        answer_id: str,
        answer_data: Optional[AnswerType] = None,
        answer_short_text: Optional[str] = None,
        answer_data_type: type = str,
    ):
        """
        Initialize an Answer from the data or metadata.

        Args:
            answer_id:
                A unique string identifying the answer

            answer_text:
                If the answer is predefined, it is the text the form suggested.
                Otherwise it is the text the user entered. For pre-defining a
                free-text answer the text may be empty.

            answer_short_text:
                An optional string to be used for the string
                representation instead of the full text.

            answer_data_type:
                The type of the data associated with this answer.
                Supported types are bool, int, float and str.
                Defaults to str, if not specified otherwise.

        """
        self._id: str = answer_id
        self._data: Optional[AnswerType] = answer_data
        self._short_text: Optional[str] = answer_short_text
        self._data_type: type = answer_data_type

    def __str__(self) -> str:
        """Generate a string representation of the answer."""
        return f"{self._id}: {self.text}"

    @property
    def id(self) -> str:
        """Obtain the ID of the answer. The ID is unique per question."""
        return self._id

    @property
    def raw_data(self) -> AnswerType:
        """Obtain the raw data that was associated with this answer."""
        return self._data

    @property
    def text(self) -> str:
        """Obtain the full text that was associated with this answer."""
        return str(self._data)

    @property
    def short_text(self) -> Optional[str]:
        """
        Obtain the short text representation for the answer.

        Returns:
            The short text as string if one was set, None otherwise.
        """
        return self._short_text

    @property
    def label(self) -> str:
        """
        Obtain the shortest possible label for the answer.

            Defaults to returning the short text.
            If no short text is defined, the full text will be used instead.

            Returns:
                the short text representation, if available,
                otherwise the full text
        """
        return self._short_text if self._short_text else self.text

    @property
    def data_type(self) -> type:
        """Obtain the data type of the answer."""
        return self._data_type
