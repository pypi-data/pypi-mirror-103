# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetProductPolicyResult',
    'AwaitableGetProductPolicyResult',
    'get_product_policy',
]

@pulumi.output_type
class GetProductPolicyResult:
    """
    Policy Contract details.
    """
    def __init__(__self__, content_format=None, id=None, name=None, policy_content=None, type=None):
        if content_format and not isinstance(content_format, str):
            raise TypeError("Expected argument 'content_format' to be a str")
        pulumi.set(__self__, "content_format", content_format)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if policy_content and not isinstance(policy_content, str):
            raise TypeError("Expected argument 'policy_content' to be a str")
        pulumi.set(__self__, "policy_content", policy_content)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="contentFormat")
    def content_format(self) -> Optional[str]:
        """
        Format of the policyContent.
        """
        return pulumi.get(self, "content_format")

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
    @pulumi.getter(name="policyContent")
    def policy_content(self) -> str:
        """
        Json escaped Xml Encoded contents of the Policy.
        """
        return pulumi.get(self, "policy_content")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetProductPolicyResult(GetProductPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProductPolicyResult(
            content_format=self.content_format,
            id=self.id,
            name=self.name,
            policy_content=self.policy_content,
            type=self.type)


def get_product_policy(policy_id: Optional[str] = None,
                       product_id: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       service_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProductPolicyResult:
    """
    Policy Contract details.


    :param str policy_id: The identifier of the Policy.
    :param str product_id: Product identifier. Must be unique in the current API Management service instance.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['policyId'] = policy_id
    __args__['productId'] = product_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20180101:getProductPolicy', __args__, opts=opts, typ=GetProductPolicyResult).value

    return AwaitableGetProductPolicyResult(
        content_format=__ret__.content_format,
        id=__ret__.id,
        name=__ret__.name,
        policy_content=__ret__.policy_content,
        type=__ret__.type)
