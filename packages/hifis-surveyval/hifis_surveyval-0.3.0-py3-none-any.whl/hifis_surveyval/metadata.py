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
This module provides the definitions for survey metadata.

Survey metadata given in a YAML file is transformed into a dictionary.

.. currentmodule:: hifis_surveyval.metadata
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

import logging
from pathlib import Path
from pydoc import locate
from typing import Dict, List, Optional, Union

import numpy
import yaml

from hifis_surveyval import globals
from hifis_surveyval.answer import Answer, AnswerType, ValidAnswerTypes
from hifis_surveyval.data import DataContainer
from hifis_surveyval.question import AbstractQuestion, Question, QuestionCollection

# The YAML dictionary has a recursive type
YamlDict = Dict[str, Optional[Union[str, "YamlDict"]]]

# This would be cooler as an enum
# How to do that in an elegant way with minimal overhead?
KEYWORD_QUESTIONS: str = "questions"
KEYWORD_ANSWERS: str = "answers"
KEYWORD_ID: str = "id"
KEYWORD_TEXT: str = "text"
KEYWORD_SHORT: str = "short-text"
KEYWORD_DATATYPE: str = "datatype"


def parse_answer(content: YamlDict, question_data_type: type = str) -> Answer:
    """
    Parse an Answer object from YAML.

    Args:
        content:            The YAML representation as a dictionary
        question_data_type: The data type of an answer to a question.

    Returns:
        A newly constructed Answer object.
    """
    assert KEYWORD_ID in content
    assert KEYWORD_TEXT in content

    answer_id: str = content[KEYWORD_ID]
    answer_text: str = content[KEYWORD_TEXT]
    answer_short_text: Optional[str] = (
        content[KEYWORD_SHORT] if KEYWORD_SHORT in content else None
    )
    return Answer(answer_id, answer_text, answer_short_text, question_data_type)


def parse_question(content: YamlDict, collection_id: Optional[str] = None) -> Question:
    """
    Parse a Question object from YAML.

    Args:
        content:        The YAML representation as a dictionary
        collection_id:  (Optional) If the question is part of a question
                        collection, this is the ID of the collection as it will
                        be part of the question ID.
                        Otherwise, just default to None.

    Returns:
        A newly constructed Question object. It will automatically be added to
        globals.survey_questions
    """
    assert KEYWORD_ID in content
    assert KEYWORD_TEXT in content

    question_id: str = content.get(KEYWORD_ID)

    if collection_id:
        question_id = collection_id + "[" + question_id + "]"

    question_text: str = content.get(KEYWORD_TEXT)
    predefined_answers: List[Answer] = []

    # Data types from metadata are given as string.
    # They need to be converted to type with pydoc.locate().
    # The default data type is string.
    question_data_type: type
    if KEYWORD_DATATYPE in content:
        type_string: str = content[KEYWORD_DATATYPE]
        if type_string not in ValidAnswerTypes:
            # TODO is there a more robust way to create the filter string?
            raise ValueError(
                f"Could not parse type name '{type_string}' from metadata "
                f"when constructing question {question_id}"
            )

        question_data_type = locate(type_string)
    else:
        question_data_type = str

    # Check for predefined answers
    if KEYWORD_ANSWERS in content and content[KEYWORD_ANSWERS]:
        answer_yaml: YamlDict
        for answer_yaml in content[KEYWORD_ANSWERS]:
            new_answer: Answer = parse_answer(answer_yaml, question_data_type)
            predefined_answers.append(new_answer)

    new_question: Question = Question(
        question_id, question_text, predefined_answers, question_data_type
    )
    logging.debug(f"Parsed question {new_question}")

    # Put the newly parsed object into the global dictionary
    globals.survey_questions[question_id] = new_question
    return new_question


def parse_question_collection(content: YamlDict) -> None:
    """
    Parse a Question Collection object from YAML.

    Args:
        content:        The YAML representation as a dictionary

    Returns:
        A newly constructed Question Collection object.
        It will automatically be added to globals.survey_questions
    """
    # TODO handle requirements more gracefully
    assert KEYWORD_ID in content
    assert KEYWORD_TEXT in content
    assert KEYWORD_QUESTIONS in content

    collection_id: str = content.get(KEYWORD_ID)
    text: str = content.get(KEYWORD_TEXT)
    questions: List[Question] = []

    for question_yaml in content[KEYWORD_QUESTIONS]:
        questions.append(parse_question(question_yaml, collection_id))

    assert questions

    new_collection: QuestionCollection = QuestionCollection(
        collection_id, text, questions
    )
    logging.debug(f"Parsed question collection {new_collection}")

    # Put the newly parsed object into the global dictionary
    globals.survey_questions[collection_id] = new_collection


def construct_questions_from_metadata(metadata_file: Path) -> None:
    """
    Load metadata from given YAML file.

    Given YAML file with metadata is loaded into a dictionary.

    Raises:
        IOError:    Will be raised if given YAML file could
                    not be opened and loaded.
        ValueError: Will be raised if the provided file does not exist.
    """
    raw_metadata: YamlDict = {}

    if not metadata_file.exists():
        raise ValueError("Metadata file did not exist")

    try:
        with metadata_file.open(mode="r", encoding="utf-8") as file:
            raw_metadata = yaml.load(stream=file, Loader=yaml.Loader)
    except IOError:
        logging.error(f"YAML file {metadata_file} could not be opened.")
        raise

    if len(raw_metadata) == 0:
        logging.error(f"File {metadata_file} was empty.")
        return

    item: YamlDict
    for item in raw_metadata:
        if KEYWORD_QUESTIONS in item:
            parse_question_collection(item)
        else:
            parse_question(item)


def fetch_participant_answers(
    data_source: DataContainer = globals.dataContainer,
) -> None:
    """
    Extract the participants' answers for `globals.survey_questions`.

    The function will iterate through the raw pandas frame in the data
    container and extract the per-participant answers for each question.
    All answers will be stored in the globals.survey_questions dictionary.
    No data will be filtered during this operation, all will be transferred
    as-is.
    Note: Entries with no data tend to be represented as numpy.nan in pandas.
    If the respective column holds boolean or integer values, there is no valid
    representation in these data types for NaN. To preserve clean typing in
    these columns, the numpy.nan will be replaced by None.

    Args:
        data_source:    A DataContainer wrapping the raw data.
                        Defaults to global.dataContainer
    """
    if data_source.empty:
        raise ValueError(
            "Could not initialize participant answers - data source was empty"
        )

    for question_id in globals.survey_questions:
        question: AbstractQuestion = globals.survey_questions[question_id]
        if question.has_subquestions:
            continue  # collections have no answers

        answers: Dict[str, AnswerType] = data_source.data_for_question(question_id)

        participant_id: str
        answer_data: AnswerType
        for (participant_id, answer_data) in answers.items():
            if answer_data is None:
                raise ValueError(
                    f"Received answer with no data "
                    f"for question {question_id}, "
                    f"participant {participant_id}"
                )

            # Convert the given data to their respective values given the
            # Target type.
            if question.data_type is bool:
                try:
                    if answer_data is not numpy.NaN:
                        question.add_given_answer(participant_id, bool(answer_data))
                    else:
                        # numpy.nan is not a valid bool, replace by None
                        question.add_given_answer(participant_id, None)
                except ValueError:
                    logging.warning(
                        f"Could not parse answer to type 'bool' for "
                        f"question {question.id}, "
                        f"participant {participant_id}, "
                        f"answer text '{answer_data}'. "
                        f"Data entry ignored"
                    )

            elif question.data_type is float:
                try:
                    question.add_given_answer(participant_id, float(answer_data))
                except ValueError:
                    logging.warning(
                        f"Could not parse answer to type 'float' for "
                        f"question {question.id}, "
                        f"participant {participant_id}, "
                        f"answer text '{answer_data}'. "
                        f"Data entry ignored"
                    )
            elif question.data_type is int:
                try:
                    if answer_data is not numpy.NaN:
                        question.add_given_answer(participant_id, int(answer_data))
                    else:
                        # numpy.nan is not a valid int, replace by None
                        question.add_given_answer(participant_id, None)
                except ValueError:
                    logging.warning(
                        f"Could not parse answer to type 'int' for "
                        f"question {question.id}, "
                        f"participant {participant_id}, "
                        f"answer text '{answer_data}'. "
                        f"Data entry ignored"
                    )
            else:
                # Note: numpy.nan will be stored as "nan", thus they will be
                # replaced to allow them to be distinguished from valid strings
                # containing the text "nan"
                # TODO: Check for hacks/workarounds that filtered "nan" strings
                if answer_data is not numpy.NaN:
                    question.add_given_answer(participant_id, str(answer_data))
                else:
                    question.add_given_answer(participant_id, None)
