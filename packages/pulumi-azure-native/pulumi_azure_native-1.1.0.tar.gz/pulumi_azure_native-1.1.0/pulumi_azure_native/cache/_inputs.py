# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'EnterpriseSkuArgs',
    'ModuleArgs',
    'PersistenceArgs',
    'PrivateLinkServiceConnectionStateArgs',
    'ScheduleEntryArgs',
    'SkuArgs',
]

@pulumi.input_type
class EnterpriseSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'SkuName']],
                 capacity: Optional[pulumi.Input[int]] = None):
        """
        SKU parameters supplied to the create RedisEnterprise operation.
        :param pulumi.Input[Union[str, 'SkuName']] name: The type of RedisEnterprise cluster to deploy. Possible values: (Enterprise_E10, EnterpriseFlash_F300 etc.)
        :param pulumi.Input[int] capacity: The size of the RedisEnterprise cluster. Defaults to 2 or 3 depending on SKU. Valid values are (2, 4, 6, ...) for Enterprise SKUs and (3, 9, 15, ...) for Flash SKUs.
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'SkuName']]:
        """
        The type of RedisEnterprise cluster to deploy. Possible values: (Enterprise_E10, EnterpriseFlash_F300 etc.)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'SkuName']]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The size of the RedisEnterprise cluster. Defaults to 2 or 3 depending on SKU. Valid values are (2, 4, 6, ...) for Enterprise SKUs and (3, 9, 15, ...) for Flash SKUs.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)


@pulumi.input_type
class ModuleArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 args: Optional[pulumi.Input[str]] = None):
        """
        Specifies configuration of a redis module
        :param pulumi.Input[str] name: The name of the module, e.g. 'RedisBloom', 'RediSearch', 'RedisTimeSeries'
        :param pulumi.Input[str] args: Configuration options for the module, e.g. 'ERROR_RATE 0.00 INITIAL_SIZE 400'.
        """
        pulumi.set(__self__, "name", name)
        if args is not None:
            pulumi.set(__self__, "args", args)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the module, e.g. 'RedisBloom', 'RediSearch', 'RedisTimeSeries'
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def args(self) -> Optional[pulumi.Input[str]]:
        """
        Configuration options for the module, e.g. 'ERROR_RATE 0.00 INITIAL_SIZE 400'.
        """
        return pulumi.get(self, "args")

    @args.setter
    def args(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "args", value)


@pulumi.input_type
class PersistenceArgs:
    def __init__(__self__, *,
                 aof_enabled: Optional[pulumi.Input[bool]] = None,
                 aof_frequency: Optional[pulumi.Input[Union[str, 'AofFrequency']]] = None,
                 rdb_enabled: Optional[pulumi.Input[bool]] = None,
                 rdb_frequency: Optional[pulumi.Input[Union[str, 'RdbFrequency']]] = None):
        """
        Persistence-related configuration for the RedisEnterprise database
        :param pulumi.Input[bool] aof_enabled: Sets whether AOF is enabled.
        :param pulumi.Input[Union[str, 'AofFrequency']] aof_frequency: Sets the frequency at which data is written to disk.
        :param pulumi.Input[bool] rdb_enabled: Sets whether RDB is enabled.
        :param pulumi.Input[Union[str, 'RdbFrequency']] rdb_frequency: Sets the frequency at which a snapshot of the database is created.
        """
        if aof_enabled is not None:
            pulumi.set(__self__, "aof_enabled", aof_enabled)
        if aof_frequency is not None:
            pulumi.set(__self__, "aof_frequency", aof_frequency)
        if rdb_enabled is not None:
            pulumi.set(__self__, "rdb_enabled", rdb_enabled)
        if rdb_frequency is not None:
            pulumi.set(__self__, "rdb_frequency", rdb_frequency)

    @property
    @pulumi.getter(name="aofEnabled")
    def aof_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Sets whether AOF is enabled.
        """
        return pulumi.get(self, "aof_enabled")

    @aof_enabled.setter
    def aof_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "aof_enabled", value)

    @property
    @pulumi.getter(name="aofFrequency")
    def aof_frequency(self) -> Optional[pulumi.Input[Union[str, 'AofFrequency']]]:
        """
        Sets the frequency at which data is written to disk.
        """
        return pulumi.get(self, "aof_frequency")

    @aof_frequency.setter
    def aof_frequency(self, value: Optional[pulumi.Input[Union[str, 'AofFrequency']]]):
        pulumi.set(self, "aof_frequency", value)

    @property
    @pulumi.getter(name="rdbEnabled")
    def rdb_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Sets whether RDB is enabled.
        """
        return pulumi.get(self, "rdb_enabled")

    @rdb_enabled.setter
    def rdb_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "rdb_enabled", value)

    @property
    @pulumi.getter(name="rdbFrequency")
    def rdb_frequency(self) -> Optional[pulumi.Input[Union[str, 'RdbFrequency']]]:
        """
        Sets the frequency at which a snapshot of the database is created.
        """
        return pulumi.get(self, "rdb_frequency")

    @rdb_frequency.setter
    def rdb_frequency(self, value: Optional[pulumi.Input[Union[str, 'RdbFrequency']]]):
        pulumi.set(self, "rdb_frequency", value)


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


