# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetScopeAssignmentResult',
    'AwaitableGetScopeAssignmentResult',
    'get_scope_assignment',
]

@pulumi.output_type
class GetScopeAssignmentResult:
    """
    The Managed Network resource
    """
    def __init__(__self__, assigned_managed_network=None, etag=None, id=None, location=None, name=None, provisioning_state=None, type=None):
        if assigned_managed_network and not isinstance(assigned_managed_network, str):
            raise TypeError("Expected argument 'assigned_managed_network' to be a str")
        pulumi.set(__self__, "assigned_managed_network", assigned_managed_network)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="assignedManagedNetwork")
    def assigned_managed_network(self) -> Optional[str]:
        """
        The managed network ID with scope will be assigned to.
        """
        return pulumi.get(self, "assigned_managed_network")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource Id for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the ManagedNetwork resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")


class AwaitableGetScopeAssignmentResult(GetScopeAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetScopeAssignmentResult(
            assigned_managed_network=self.assigned_managed_network,
            etag=self.etag,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            type=self.type)


def get_scope_assignment(scope: Optional[str] = None,
                         scope_assignment_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetScopeAssignmentResult:
    """
    The Managed Network resource
    API Version: 2019-06-01-preview.


    :param str scope: The base resource of the scope assignment.
    :param str scope_assignment_name: The name of the scope assignment to get.
    """
    __args__ = dict()
    __args__['scope'] = scope
    __args__['scopeAssignmentName'] = scope_assignment_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:managednetwork:getScopeAssignment', __args__, opts=opts, typ=GetScopeAssignmentResult).value

    return AwaitableGetScopeAssignmentResult(
        assigned_managed_network=__ret__.assigned_managed_network,
        etag=__ret__.etag,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        type=__ret__.type)
