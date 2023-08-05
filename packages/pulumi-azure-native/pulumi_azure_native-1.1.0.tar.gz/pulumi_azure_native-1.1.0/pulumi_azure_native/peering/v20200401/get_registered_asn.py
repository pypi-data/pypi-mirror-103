# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetRegisteredAsnResult',
    'AwaitableGetRegisteredAsnResult',
    'get_registered_asn',
]

@pulumi.output_type
class GetRegisteredAsnResult:
    """
    The customer's ASN that is registered by the peering service provider.
    """
    def __init__(__self__, asn=None, id=None, name=None, peering_service_prefix_key=None, provisioning_state=None, type=None):
        if asn and not isinstance(asn, int):
            raise TypeError("Expected argument 'asn' to be a int")
        pulumi.set(__self__, "asn", asn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if peering_service_prefix_key and not isinstance(peering_service_prefix_key, str):
            raise TypeError("Expected argument 'peering_service_prefix_key' to be a str")
        pulumi.set(__self__, "peering_service_prefix_key", peering_service_prefix_key)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def asn(self) -> Optional[int]:
        """
        The customer's ASN from which traffic originates.
        """
        return pulumi.get(self, "asn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="peeringServicePrefixKey")
    def peering_service_prefix_key(self) -> str:
        """
        The peering service prefix key that is to be shared with the customer.
        """
        return pulumi.get(self, "peering_service_prefix_key")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetRegisteredAsnResult(GetRegisteredAsnResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegisteredAsnResult(
            asn=self.asn,
            id=self.id,
            name=self.name,
            peering_service_prefix_key=self.peering_service_prefix_key,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_registered_asn(peering_name: Optional[str] = None,
                       registered_asn_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegisteredAsnResult:
    """
    The customer's ASN that is registered by the peering service provider.


    :param str peering_name: The name of the peering.
    :param str registered_asn_name: The name of the registered ASN.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['peeringName'] = peering_name
    __args__['registeredAsnName'] = registered_asn_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:peering/v20200401:getRegisteredAsn', __args__, opts=opts, typ=GetRegisteredAsnResult).value

    return AwaitableGetRegisteredAsnResult(
        asn=__ret__.asn,
        id=__ret__.id,
        name=__ret__.name,
        peering_service_prefix_key=__ret__.peering_service_prefix_key,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)
