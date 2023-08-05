# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetPropertyResult',
    'AwaitableGetPropertyResult',
    'get_property',
]

@pulumi.output_type
class GetPropertyResult:
    """
    Property details.
    """
    def __init__(__self__, display_name=None, id=None, name=None, secret=None, tags=None, type=None, value=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if secret and not isinstance(secret, bool):
            raise TypeError("Expected argument 'secret' to be a bool")
        pulumi.set(__self__, "secret", secret)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        Unique name of Property. It may contain only letters, digits, period, dash, and underscore characters.
        """
        return pulumi.get(self, "display_name")

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
    @pulumi.getter
    def secret(self) -> Optional[bool]:
        """
        Determines whether the value is a secret and should be encrypted or not. Default value is false.
        """
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Sequence[str]]:
        """
        Optional tags that when provided can be used to filter the property list.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type for API Management resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Value of the property. Can contain policy expressions. It may not be empty or consist only of whitespace.
        """
        return pulumi.get(self, "value")


class AwaitableGetPropertyResult(GetPropertyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPropertyResult(
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            secret=self.secret,
            tags=self.tags,
            type=self.type,
            value=self.value)


def get_property(prop_id: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 service_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPropertyResult:
    """
    Property details.


    :param str prop_id: Identifier of the property.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['propId'] = prop_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20180101:getProperty', __args__, opts=opts, typ=GetPropertyResult).value

    return AwaitableGetPropertyResult(
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        secret=__ret__.secret,
        tags=__ret__.tags,
        type=__ret__.type,
        value=__ret__.value)
