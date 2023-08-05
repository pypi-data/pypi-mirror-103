# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'PrivateLinkServiceConnectionStateArgs',
    'ScheduleEntryArgs',
    'SkuArgs',
]

@pulumi.input_type
class PrivateLinkServiceConnectionStateArgs:
    def __init__(__self__, *,
                 actions_required: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]] = None):
        """
        A collection of information about the state of the connection between service consumer and provider.
        :param pulumi.Input[str] actions_required: A message indicating if changes on the service provider require any updates on the consumer.
        :param pulumi.Input[str] description: The reason for approval/rejection of the connection.
        :param pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']] status: Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        if actions_required is not None:
            pulumi.set(__self__, "actions_required", actions_required)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="actionsRequired")
    def actions_required(self) -> Optional[pulumi.Input[str]]:
        """
        A message indicating if changes on the service provider require any updates on the consumer.
        """
        return pulumi.get(self, "actions_required")

    @actions_required.setter
    def actions_required(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "actions_required", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The reason for approval/rejection of the connection.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]:
        """
        Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'PrivateEndpointServiceConnectionStatus']]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class ScheduleEntryArgs:
    def __init__(__self__, *,
                 day_of_week: pulumi.Input['DayOfWeek'],
                 start_hour_utc: pulumi.Input[int],
                 maintenance_window: Optional[pulumi.Input[str]] = None):
        """
        Patch schedule entry for a Premium Redis Cache.
        :param pulumi.Input['DayOfWeek'] day_of_week: Day of the week when a cache can be patched.
        :param pulumi.Input[int] start_hour_utc: Start hour after which cache patching can start.
        :param pulumi.Input[str] maintenance_window: ISO8601 timespan specifying how much time cache patching can take. 
        """
        pulumi.set(__self__, "day_of_week", day_of_week)
        pulumi.set(__self__, "start_hour_utc", start_hour_utc)
        if maintenance_window is not None:
            pulumi.set(__self__, "maintenance_window", maintenance_window)

    @property
    @pulumi.getter(name="dayOfWeek")
    def day_of_week(self) -> pulumi.Input['DayOfWeek']:
        """
        Day of the week when a cache can be patched.
        """
        return pulumi.get(self, "day_of_week")

    @day_of_week.setter
    def day_of_week(self, value: pulumi.Input['DayOfWeek']):
        pulumi.set(self, "day_of_week", value)

    @property
    @pulumi.getter(name="startHourUtc")
    def start_hour_utc(self) -> pulumi.Input[int]:
        """
        Start hour after which cache patching can start.
        """
        return pulumi.get(self, "start_hour_utc")

    @start_hour_utc.setter
    def start_hour_utc(self, value: pulumi.Input[int]):
        pulumi.set(self, "start_hour_utc", value)

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> Optional[pulumi.Input[str]]:
        """
        ISO8601 timespan specifying how much time cache patching can take. 
        """
        return pulumi.get(self, "maintenance_window")

    @maintenance_window.setter
    def maintenance_window(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "maintenance_window", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 capacity: pulumi.Input[int],
                 family: pulumi.Input[Union[str, 'SkuFamily']],
                 name: pulumi.Input[Union[str, 'SkuName']]):
        """
        SKU parameters supplied to the create Redis operation.
        :param pulumi.Input[int] capacity: The size of the Redis cache to deploy. Valid values: for C (Basic/Standard) family (0, 1, 2, 3, 4, 5, 6), for P (Premium) family (1, 2, 3, 4).
        :param pulumi.Input[Union[str, 'SkuFamily']] family: The SKU family to use. Valid values: (C, P). (C = Basic/Standard, P = Premium).
        :param pulumi.Input[Union[str, 'SkuName']] name: The type of Redis cache to deploy. Valid values: (Basic, Standard, Premium)
        """
        pulumi.set(__self__, "capacity", capacity)
        pulumi.set(__self__, "family", family)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def capacity(self) -> pulumi.Input[int]:
        """
        The size of the Redis cache to deploy. Valid values: for C (Basic/Standard) family (0, 1, 2, 3, 4, 5, 6), for P (Premium) family (1, 2, 3, 4).
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: pulumi.Input[int]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> pulumi.Input[Union[str, 'SkuFamily']]:
        """
        The SKU family to use. Valid values: (C, P). (C = Basic/Standard, P = Premium).
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: pulumi.Input[Union[str, 'SkuFamily']]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        The type of Redis cache to deploy. Valid values: (Basic, Standard, Premium)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)


