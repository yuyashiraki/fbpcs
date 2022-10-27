#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging

from fbpcs.private_computation.entity.private_computation_status import (
    PrivateComputationInstanceStatus,
)
from fbpcs.private_computation.service.constants import DEFAULT_RUN_PID_TIMEOUT_IN_SEC
from fbpcs.private_computation.service.private_computation_stage_service import (
    PrivateComputationStageService,
    PrivateComputationStageServiceArgs,
)
from fbpcs.private_computation.stage_flows.private_computation_base_stage_flow import (
    PrivateComputationBaseStageFlow,
    PrivateComputationStageFlowData,
)


class PrivateComputationPIDOnlyTestStageFlow(PrivateComputationBaseStageFlow):
    """
    - PID Only Test Stage Flow -
    This enum lists all of the supported stage types and maps to their possible statuses.
    It also provides methods to get information about the next or previous stage.

    NOTE: The order in which the enum members appear is the order in which the stages are intended
    to run. The _order_ variable is used to ensure member order is consistent (class attribute, removed during class creation).
    An exception is raised at runtime if _order_ is inconsistent with the actual member order.
    """

    # Specifies the order of the stages. Don't change this unless you know what you are doing.
    # pyre-fixme[15]: `_order_` overrides attribute defined in `Enum` inconsistently.
    _order_ = "CREATED PID_SHARD PID_PREPARE ID_MATCH ID_MATCH_POST_PROCESS"
    # Regarding typing fixme above, Pyre appears to be wrong on this one. _order_ only appears in the EnumMeta metaclass __new__ method
    # and is not actually added as a variable on the enum class. I think this is why pyre gets confused.

    CREATED = PrivateComputationStageFlowData(
        initialized_status=PrivateComputationInstanceStatus.CREATION_INITIALIZED,
        started_status=PrivateComputationInstanceStatus.CREATION_STARTED,
        completed_status=PrivateComputationInstanceStatus.CREATED,
        failed_status=PrivateComputationInstanceStatus.CREATION_FAILED,
        is_joint_stage=False,
    )
    PID_SHARD = PrivateComputationStageFlowData(
        initialized_status=PrivateComputationInstanceStatus.PID_SHARD_INITIALIZED,
        started_status=PrivateComputationInstanceStatus.PID_SHARD_STARTED,
        completed_status=PrivateComputationInstanceStatus.PID_SHARD_COMPLETED,
        failed_status=PrivateComputationInstanceStatus.PID_SHARD_FAILED,
        is_joint_stage=False,
    )
    PID_PREPARE = PrivateComputationStageFlowData(
        initialized_status=PrivateComputationInstanceStatus.PID_PREPARE_INITIALIZED,
        started_status=PrivateComputationInstanceStatus.PID_PREPARE_STARTED,
        completed_status=PrivateComputationInstanceStatus.PID_PREPARE_COMPLETED,
        failed_status=PrivateComputationInstanceStatus.PID_PREPARE_FAILED,
        is_joint_stage=False,
    )
    ID_MATCH = PrivateComputationStageFlowData(
        initialized_status=PrivateComputationInstanceStatus.ID_MATCHING_INITIALIZED,
        started_status=PrivateComputationInstanceStatus.ID_MATCHING_STARTED,
        completed_status=PrivateComputationInstanceStatus.ID_MATCHING_COMPLETED,
        failed_status=PrivateComputationInstanceStatus.ID_MATCHING_FAILED,
        is_joint_stage=True,
        is_retryable=True,
        timeout=DEFAULT_RUN_PID_TIMEOUT_IN_SEC,
    )
    ID_MATCH_POST_PROCESS = PrivateComputationStageFlowData(
        initialized_status=PrivateComputationInstanceStatus.ID_MATCHING_POST_PROCESS_INITIALIZED,
        started_status=PrivateComputationInstanceStatus.ID_MATCHING_POST_PROCESS_STARTED,
        completed_status=PrivateComputationInstanceStatus.ID_MATCHING_POST_PROCESS_COMPLETED,
        failed_status=PrivateComputationInstanceStatus.ID_MATCHING_POST_PROCESS_FAILED,
        is_joint_stage=False,
    )

    def get_stage_service(
        self, args: PrivateComputationStageServiceArgs
    ) -> PrivateComputationStageService:
        """
        Maps PrivateComputationPIDOnlyTestStageFlow instances to StageService instances

        Arguments:
            args: Common arguments initialized in PrivateComputationService that are consumed by stage services

        Returns:
            An instantiated StageService object corresponding to the StageFlow enum member caller.
        """
        logging.info("Start PID Only Test stage flow")
        return self.get_default_stage_service(args)
