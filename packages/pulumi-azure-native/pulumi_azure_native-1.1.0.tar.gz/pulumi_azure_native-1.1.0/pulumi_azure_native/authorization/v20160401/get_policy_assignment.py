# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetPolicyAssignmentResult',
    'AwaitableGetPolicyAssignmentResult',
    'get_policy_assignment',
]

@pulumi.output_type
class GetPolicyAssignmentResult:
    """
    The policy assignment.
    """
    def __init__(__self__, display_name=None, id=None, name=None, policy_definition_id=None, scope=None, type=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if policy_definition_id and not isinstance(policy_definition_id, str):
            raise TypeError("Expected argument 'policy_definition_id' to be a str")
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        if scope and not isinstance(scope, str):
            raise TypeError("Expected argument 'scope' to be a str")
        pulumi.set(__self__, "scope", scope)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the policy assignment.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the policy assignment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the policy assignment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> Optional[str]:
        """
        The ID of the policy definition.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter
    def scope(self) -> Optional[str]:
        """
        The scope for the policy assignment.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the policy assignment.
        """
        return pulumi.get(self, "type")


class AwaitableGetPolicyAssignmentResult(GetPolicyAssignmentResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyAssignmentResult(
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            policy_definition_id=self.policy_definition_id,
            scope=self.scope,
            type=self.type)


def get_policy_assignment(policy_assignment_name: Optional[str] = None,
                          scope: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyAssignmentResult:
    """
    The policy assignment.


    :param str policy_assignment_name: The name of the policy assignment to get.
    :param str scope: The scope of the policy assignment.
    """
    __args__ = dict()
    __args__['policyAssignmentName'] = policy_assignment_name
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:authorization/v20160401:getPolicyAssignment', __args__, opts=opts, typ=GetPolicyAssignmentResult).value

    return AwaitableGetPolicyAssignmentResult(
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        policy_definition_id=__ret__.policy_definition_id,
        scope=__ret__.scope,
        type=__ret__.type)
