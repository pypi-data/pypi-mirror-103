# -*- coding: utf-8 -*-
# Copyright © 2021 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.api.dtm_pb2 import TraceEvent
from contrast.agent.policy import constants
from contrast.utils.base64_utils import base64_decode


def default_taint_range_validator(taint_ranges, endrange):
    for taint_range in taint_ranges:
        assert taint_range.range == "0:{}".format(endrange)


def _assert_basic_event(event, event_type, action, class_name, method_name):
    assert event.type == event_type
    assert event.action == action
    assert event.signature.class_name == class_name
    assert event.signature.method_name == method_name


def check_event(
    event,
    event_type,
    action,
    class_name,
    method_name,
    source_types,
    first_parent,
    source=None,
    target=None,
    ret_value=None,
    taint_range_validator=default_taint_range_validator,
):
    """

    Assert values for TraceEvent dtm.
    """
    _assert_basic_event(event, event_type, action, class_name, method_name)

    assert all([s.type in source_types for s in event.event_sources])

    assert (
        event.parent_object_ids[0].id == first_parent.object_id
        if first_parent
        else True
    )

    if source:
        assert event.source == source

    if target:
        assert event.target == target

    if ret_value:
        # ret value is the right side of the vulnerability > details page in TS
        assert base64_decode(event.ret.value) == ret_value
        if taint_range_validator is not None:
            taint_range_validator(list(event.taint_ranges), len(ret_value))


def assert_source_event(event, class_name, method_name):
    _assert_basic_event(
        event,
        TraceEvent.TYPE_PROPAGATION,
        TraceEvent.Action.Value(constants.CREATION_TYPE),
        class_name,
        method_name,
    )


def assert_trigger_event(event, class_name, method_name):
    _assert_basic_event(
        event,
        TraceEvent.TYPE_PROPAGATION,
        TraceEvent.Action.Value(constants.TRIGGER_TYPE),
        class_name,
        method_name,
    )


def assert_propagation_event(event, class_name, method_name, a2r=True):
    prop_action = "{}{}{}".format(
        constants.ALL_TYPE if a2r else constants.OBJECT_KEY,
        constants.TO_MARKER,
        constants.RETURN_KEY,
    )

    _assert_basic_event(
        event,
        TraceEvent.TYPE_PROPAGATION,
        TraceEvent.Action.Value(prop_action),
        class_name,
        method_name,
    )
