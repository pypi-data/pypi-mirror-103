# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetDedicatedHsmResult',
    'AwaitableGetDedicatedHsmResult',
    'get_dedicated_hsm',
]

@pulumi.output_type
class GetDedicatedHsmResult:
    """
    Resource information with extended details.
    """
    def __init__(__self__, id=None, location=None, name=None, network_profile=None, provisioning_state=None, sku=None, stamp_id=None, status_message=None, tags=None, type=None, zones=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_profile and not isinstance(network_profile, dict):
            raise TypeError("Expected argument 'network_profile' to be a dict")
        pulumi.set(__self__, "network_profile", network_profile)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if stamp_id and not isinstance(stamp_id, str):
            raise TypeError("Expected argument 'stamp_id' to be a str")
        pulumi.set(__self__, "stamp_id", stamp_id)
        if status_message and not isinstance(status_message, str):
            raise TypeError("Expected argument 'status_message' to be a str")
        pulumi.set(__self__, "status_message", status_message)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The Azure Resource Manager resource ID for the dedicated HSM.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The supported Azure location where the dedicated HSM should be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the dedicated HSM.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkProfile")
    def network_profile(self) -> Optional['outputs.NetworkProfileResponse']:
        """
        Specifies the network interfaces of the dedicated hsm.
        """
        return pulumi.get(self, "network_profile")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        SKU details
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="stampId")
    def stamp_id(self) -> Optional[str]:
        """
        This field will be used when RP does not support Availability zones.
        """
        return pulumi.get(self, "stamp_id")

    @property
    @pulumi.getter(name="statusMessage")
    def status_message(self) -> str:
        """
        Resource Status Message.
        """
        return pulumi.get(self, "status_message")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type of the dedicated HSM.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        The Dedicated Hsm zones.
        """
        return pulumi.get(self, "zones")


class AwaitableGetDedicatedHsmResult(GetDedicatedHsmResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDedicatedHsmResult(
            id=self.id,
            location=self.location,
            name=self.name,
            network_profile=self.network_profile,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            stamp_id=self.stamp_id,
            status_message=self.status_message,
            tags=self.tags,
            type=self.type,
            zones=self.zones)


def get_dedicated_hsm(name: Optional[str] = None,
                      resource_group_name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDedicatedHsmResult:
    """
    Resource information with extended details.
    API Version: 2018-10-31-preview.


    :param str name: The name of the dedicated HSM.
    :param str resource_group_name: The name of the Resource Group to which the dedicated hsm belongs.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:hardwaresecuritymodules:getDedicatedHsm', __args__, opts=opts, typ=GetDedicatedHsmResult).value

    return AwaitableGetDedicatedHsmResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        network_profile=__ret__.network_profile,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        stamp_id=__ret__.stamp_id,
        status_message=__ret__.status_message,
        tags=__ret__.tags,
        type=__ret__.type,
        zones=__ret__.zones)
