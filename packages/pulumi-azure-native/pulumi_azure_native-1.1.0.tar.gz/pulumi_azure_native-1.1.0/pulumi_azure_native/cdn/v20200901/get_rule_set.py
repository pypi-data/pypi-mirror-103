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
    'GetRuleSetResult',
    'AwaitableGetRuleSetResult',
    'get_rule_set',
]

@pulumi.output_type
class GetRuleSetResult:
    """
    Friendly RuleSet name mapping to the any RuleSet or secret related information.
    """
    def __init__(__self__, deployment_status=None, id=None, name=None, provisioning_state=None, system_data=None, type=None):
        if deployment_status and not isinstance(deployment_status, str):
            raise TypeError("Expected argument 'deployment_status' to be a str")
        pulumi.set(__self__, "deployment_status", deployment_status)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> str:
        return pulumi.get(self, "deployment_status")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning status
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetRuleSetResult(GetRuleSetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRuleSetResult(
            deployment_status=self.deployment_status,
            id=self.id,
            name=self.name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            type=self.type)


def get_rule_set(profile_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 rule_set_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRuleSetResult:
    """
    Friendly RuleSet name mapping to the any RuleSet or secret related information.


    :param str profile_name: Name of the CDN profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str rule_set_name: Name of the rule set under the profile which is unique globally.
    """
    __args__ = dict()
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['ruleSetName'] = rule_set_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:cdn/v20200901:getRuleSet', __args__, opts=opts, typ=GetRuleSetResult).value

    return AwaitableGetRuleSetResult(
        deployment_status=__ret__.deployment_status,
        id=__ret__.id,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        type=__ret__.type)
