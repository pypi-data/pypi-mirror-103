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
    'GetDeploymentAtSubscriptionScopeResult',
    'AwaitableGetDeploymentAtSubscriptionScopeResult',
    'get_deployment_at_subscription_scope',
]

@pulumi.output_type
class GetDeploymentAtSubscriptionScopeResult:
    """
    Deployment information.
    """
    def __init__(__self__, id=None, location=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the deployment.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        the location of the deployment.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the deployment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.DeploymentPropertiesExtendedResponse':
        """
        Deployment properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the deployment.
        """
        return pulumi.get(self, "type")


class AwaitableGetDeploymentAtSubscriptionScopeResult(GetDeploymentAtSubscriptionScopeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDeploymentAtSubscriptionScopeResult(
            id=self.id,
            location=self.location,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_deployment_at_subscription_scope(deployment_name: Optional[str] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDeploymentAtSubscriptionScopeResult:
    """
    Deployment information.


    :param str deployment_name: The name of the deployment to get.
    """
    __args__ = dict()
    __args__['deploymentName'] = deployment_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:resources/v20180501:getDeploymentAtSubscriptionScope', __args__, opts=opts, typ=GetDeploymentAtSubscriptionScopeResult).value

    return AwaitableGetDeploymentAtSubscriptionScopeResult(
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)
