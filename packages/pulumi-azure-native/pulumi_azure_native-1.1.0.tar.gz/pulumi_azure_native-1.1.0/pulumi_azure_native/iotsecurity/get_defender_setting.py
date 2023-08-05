# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetDefenderSettingResult',
    'AwaitableGetDefenderSettingResult',
    'get_defender_setting',
]

@pulumi.output_type
class GetDefenderSettingResult:
    """
    IoT Defender settings
    """
    def __init__(__self__, device_quota=None, id=None, name=None, onboarding_kind=None, sentinel_workspace_resource_ids=None, type=None):
        if device_quota and not isinstance(device_quota, int):
            raise TypeError("Expected argument 'device_quota' to be a int")
        pulumi.set(__self__, "device_quota", device_quota)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if onboarding_kind and not isinstance(onboarding_kind, str):
            raise TypeError("Expected argument 'onboarding_kind' to be a str")
        pulumi.set(__self__, "onboarding_kind", onboarding_kind)
        if sentinel_workspace_resource_ids and not isinstance(sentinel_workspace_resource_ids, list):
            raise TypeError("Expected argument 'sentinel_workspace_resource_ids' to be a list")
        pulumi.set(__self__, "sentinel_workspace_resource_ids", sentinel_workspace_resource_ids)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="deviceQuota")
    def device_quota(self) -> int:
        """
        Size of the device quota (as a opposed to a Pay as You Go billing model). Value is required to be in multiples of 1000.
        """
        return pulumi.get(self, "device_quota")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="onboardingKind")
    def onboarding_kind(self) -> str:
        """
        The kind of onboarding for the subscription
        """
        return pulumi.get(self, "onboarding_kind")

    @property
    @pulumi.getter(name="sentinelWorkspaceResourceIds")
    def sentinel_workspace_resource_ids(self) -> Sequence[str]:
        """
        Sentinel Workspace Resource Ids
        """
        return pulumi.get(self, "sentinel_workspace_resource_ids")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetDefenderSettingResult(GetDefenderSettingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDefenderSettingResult(
            device_quota=self.device_quota,
            id=self.id,
            name=self.name,
            onboarding_kind=self.onboarding_kind,
            sentinel_workspace_resource_ids=self.sentinel_workspace_resource_ids,
            type=self.type)


def get_defender_setting(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDefenderSettingResult:
    """
    IoT Defender settings
    API Version: 2021-02-01-preview.
    """
    __args__ = dict()
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:iotsecurity:getDefenderSetting', __args__, opts=opts, typ=GetDefenderSettingResult).value

    return AwaitableGetDefenderSettingResult(
        device_quota=__ret__.device_quota,
        id=__ret__.id,
        name=__ret__.name,
        onboarding_kind=__ret__.onboarding_kind,
        sentinel_workspace_resource_ids=__ret__.sentinel_workspace_resource_ids,
        type=__ret__.type)
