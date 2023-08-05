# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetDnsResourceReferenceByTarResourcesResult',
    'AwaitableGetDnsResourceReferenceByTarResourcesResult',
    'get_dns_resource_reference_by_tar_resources',
]

@pulumi.output_type
class GetDnsResourceReferenceByTarResourcesResult:
    """
    Represents the properties of the Dns Resource Reference Result.
    """
    def __init__(__self__, dns_resource_references=None):
        if dns_resource_references and not isinstance(dns_resource_references, list):
            raise TypeError("Expected argument 'dns_resource_references' to be a list")
        pulumi.set(__self__, "dns_resource_references", dns_resource_references)

    @property
    @pulumi.getter(name="dnsResourceReferences")
    def dns_resource_references(self) -> Optional[Sequence['outputs.DnsResourceReferenceResponse']]:
        """
        The result of dns resource reference request. A list of dns resource references for each of the azure resource in the request
        """
        return pulumi.get(self, "dns_resource_references")


class AwaitableGetDnsResourceReferenceByTarResourcesResult(GetDnsResourceReferenceByTarResourcesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDnsResourceReferenceByTarResourcesResult(
            dns_resource_references=self.dns_resource_references)


def get_dns_resource_reference_by_tar_resources(target_resources: Optional[Sequence[pulumi.InputType['SubResource']]] = None,
                                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDnsResourceReferenceByTarResourcesResult:
    """
    Represents the properties of the Dns Resource Reference Result.


    :param Sequence[pulumi.InputType['SubResource']] target_resources: A list of references to azure resources for which referencing dns records need to be queried.
    """
    __args__ = dict()
    __args__['targetResources'] = target_resources
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20180501:getDnsResourceReferenceByTarResources', __args__, opts=opts, typ=GetDnsResourceReferenceByTarResourcesResult).value

    return AwaitableGetDnsResourceReferenceByTarResourcesResult(
        dns_resource_references=__ret__.dns_resource_references)
