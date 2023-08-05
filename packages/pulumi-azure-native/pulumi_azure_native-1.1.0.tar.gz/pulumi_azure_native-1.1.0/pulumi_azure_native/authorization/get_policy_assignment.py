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
    'GetPolicyAssignmentResult',
    'AwaitableGetPolicyAssignmentResult',
    'get_policy_assignment',
]

@pulumi.output_type
class GetPolicyAssignmentResult:
    """
    The policy assignment.
    """
    def __init__(__self__, description=None, display_name=None, enforcement_mode=None, id=None, identity=None, location=None, metadata=None, name=None, non_compliance_messages=None, not_scopes=None, parameters=None, policy_definition_id=None, scope=None, type=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if enforcement_mode and not isinstance(enforcement_mode, str):
            raise TypeError("Expected argument 'enforcement_mode' to be a str")
        pulumi.set(__self__, "enforcement_mode", enforcement_mode)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if metadata and not isinstance(metadata, dict):
            raise TypeError("Expected argument 'metadata' to be a dict")
        pulumi.set(__self__, "metadata", metadata)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if non_compliance_messages and not isinstance(non_compliance_messages, list):
            raise TypeError("Expected argument 'non_compliance_messages' to be a list")
        pulumi.set(__self__, "non_compliance_messages", non_compliance_messages)
        if not_scopes and not isinstance(not_scopes, list):
            raise TypeError("Expected argument 'not_scopes' to be a list")
        pulumi.set(__self__, "not_scopes", not_scopes)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
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
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        This message will be part of response in case of policy violation.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the policy assignment.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="enforcementMode")
    def enforcement_mode(self) -> Optional[str]:
        """
        The policy assignment enforcement mode. Possible values are Default and DoNotEnforce.
        """
        return pulumi.get(self, "enforcement_mode")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the policy assignment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The managed identity associated with the policy assignment.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The location of the policy assignment. Only required when utilizing managed identity.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def metadata(self) -> Optional[Any]:
        """
        The policy assignment metadata. Metadata is an open ended object and is typically a collection of key value pairs.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the policy assignment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nonComplianceMessages")
    def non_compliance_messages(self) -> Optional[Sequence['outputs.NonComplianceMessageResponse']]:
        """
        The messages that describe why a resource is non-compliant with the policy.
        """
        return pulumi.get(self, "non_compliance_messages")

    @property
    @pulumi.getter(name="notScopes")
    def not_scopes(self) -> Optional[Sequence[str]]:
        """
        The policy's excluded scopes.
        """
        return pulumi.get(self, "not_scopes")

    @property
    @pulumi.getter
    def parameters(self) -> Optional[Mapping[str, 'outputs.ParameterValuesValueResponse']]:
        """
        The parameter values for the assigned policy rule. The keys are the parameter names.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> Optional[str]:
        """
        The ID of the policy definition or policy set definition being assigned.
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter
    def scope(self) -> str:
        """
        The scope for the policy assignment.
        """
        return pulumi.get(self, "scope")

    @property
    @pulumi.getter
    def type(self) -> str:
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
            description=self.description,
            display_name=self.display_name,
            enforcement_mode=self.enforcement_mode,
            id=self.id,
            identity=self.identity,
            location=self.location,
            metadata=self.metadata,
            name=self.name,
            non_compliance_messages=self.non_compliance_messages,
            not_scopes=self.not_scopes,
            parameters=self.parameters,
            policy_definition_id=self.policy_definition_id,
            scope=self.scope,
            type=self.type)


def get_policy_assignment(policy_assignment_name: Optional[str] = None,
                          scope: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyAssignmentResult:
    """
    The policy assignment.
    API Version: 2020-09-01.


    :param str policy_assignment_name: The name of the policy assignment to get.
    :param str scope: The scope of the policy assignment. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}'), resource group (format: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}', or resource (format: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/[{parentResourcePath}/]{resourceType}/{resourceName}'
    """
    __args__ = dict()
    __args__['policyAssignmentName'] = policy_assignment_name
    __args__['scope'] = scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:authorization:getPolicyAssignment', __args__, opts=opts, typ=GetPolicyAssignmentResult).value

    return AwaitableGetPolicyAssignmentResult(
        description=__ret__.description,
        display_name=__ret__.display_name,
        enforcement_mode=__ret__.enforcement_mode,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        metadata=__ret__.metadata,
        name=__ret__.name,
        non_compliance_messages=__ret__.non_compliance_messages,
        not_scopes=__ret__.not_scopes,
        parameters=__ret__.parameters,
        policy_definition_id=__ret__.policy_definition_id,
        scope=__ret__.scope,
        type=__ret__.type)
