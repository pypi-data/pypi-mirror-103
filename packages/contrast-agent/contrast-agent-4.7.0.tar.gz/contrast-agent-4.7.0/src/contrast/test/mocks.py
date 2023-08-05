# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""Central location for commonly used mocks"""
import mock

from contrast.api import send_finding
from contrast.agent.assess.policy import trigger_policy
from contrast.api.dtm_pb2 import UserInput
from contrast.api.settings_pb2 import InputAnalysis, InputAnalysisResult

apply_trigger = mock.patch(
    "contrast.agent.assess.policy.trigger_policy.apply",
    side_effect=trigger_policy.apply,
)

send_finding = mock.patch(
    "contrast.agent.assess.rules.trigger_rule.send_finding", side_effect=send_finding
)

send_finding_static = mock.patch(
    "contrast.agent.assess.rules.static_rule.send_finding", side_effect=send_finding
)


def nosqli_input_analysis():
    """
    Return input analysis results as if Speedracer had processed the input.
    Note that the score_level may be different than what real Speedracer returns.
    """
    result = InputAnalysisResult(
        rule_id="nosql-injection",
        value='{"title": "Record One"}',
        path="user_input",
        key="user_input",
        input_type=UserInput.PARAMETER_VALUE,
        score_level=InputAnalysisResult.DEFINITEATTACK,
        ids=[],
    )

    return InputAnalysis(results=[result])


nosqli_input_analysis_mock = mock.patch(
    "contrast.agent.middlewares.base_middleware.get_input_analysis",
    return_value=nosqli_input_analysis(),
)
