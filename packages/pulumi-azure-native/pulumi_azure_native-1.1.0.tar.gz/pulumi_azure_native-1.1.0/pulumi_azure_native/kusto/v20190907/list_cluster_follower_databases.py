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
    'ListClusterFollowerDatabasesResult',
    'AwaitableListClusterFollowerDatabasesResult',
    'list_cluster_follower_databases',
]

@pulumi.output_type
class ListClusterFollowerDatabasesResult:
    """
    The list Kusto database principals operation response.
    """
    def __init__(__self__, value=None):
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.FollowerDatabaseDefinitionResponse']]:
        """
        The list of follower database result.
        """
        return pulumi.get(self, "value")


class AwaitableListClusterFollowerDatabasesResult(ListClusterFollowerDatabasesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListClusterFollowerDatabasesResult(
            value=self.value)


def list_cluster_follower_databases(cluster_name: Optional[str] = None,
                                    resource_group_name: Optional[str] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListClusterFollowerDatabasesResult:
    """
    The list Kusto database principals operation response.


    :param str cluster_name: The name of the Kusto cluster.
    :param str resource_group_name: The name of the resource group containing the Kusto cluster.
    """
    __args__ = dict()
    __args__['clusterName'] = cluster_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:kusto/v20190907:listClusterFollowerDatabases', __args__, opts=opts, typ=ListClusterFollowerDatabasesResult).value

    return AwaitableListClusterFollowerDatabasesResult(
        value=__ret__.value)
