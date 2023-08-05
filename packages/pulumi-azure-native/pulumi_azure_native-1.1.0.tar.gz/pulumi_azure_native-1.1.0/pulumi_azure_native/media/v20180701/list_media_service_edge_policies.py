# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'ListMediaServiceEdgePoliciesResult',
    'AwaitableListMediaServiceEdgePoliciesResult',
    'list_media_service_edge_policies',
]

@pulumi.output_type
class ListMediaServiceEdgePoliciesResult:
    def __init__(__self__, usage_data_collection_policy=None):
        if usage_data_collection_policy and not isinstance(usage_data_collection_policy, dict):
            raise TypeError("Expected argument 'usage_data_collection_policy' to be a dict")
        pulumi.set(__self__, "usage_data_collection_policy", usage_data_collection_policy)

    @property
    @pulumi.getter(name="usageDataCollectionPolicy")
    def usage_data_collection_policy(self) -> Optional['outputs.EdgeUsageDataCollectionPolicyResponse']:
        return pulumi.get(self, "usage_data_collection_policy")


class AwaitableListMediaServiceEdgePoliciesResult(ListMediaServiceEdgePoliciesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListMediaServiceEdgePoliciesResult(
            usage_data_collection_policy=self.usage_data_collection_policy)


def list_media_service_edge_policies(account_name: Optional[str] = None,
                                     device_id: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListMediaServiceEdgePoliciesResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The Media Services account name.
    :param str device_id: Unique identifier of the edge device.
    :param str resource_group_name: The name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['deviceId'] = device_id
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:media/v20180701:listMediaServiceEdgePolicies', __args__, opts=opts, typ=ListMediaServiceEdgePoliciesResult).value

    return AwaitableListMediaServiceEdgePoliciesResult(
        usage_data_collection_policy=__ret__.usage_data_collection_policy)
