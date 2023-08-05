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
    'GetCommunicationServiceResult',
    'AwaitableGetCommunicationServiceResult',
    'get_communication_service',
]

@pulumi.output_type
class GetCommunicationServiceResult:
    """
    A class representing a CommunicationService resource.
    """
    def __init__(__self__, data_location=None, host_name=None, id=None, immutable_resource_id=None, location=None, name=None, notification_hub_id=None, provisioning_state=None, system_data=None, tags=None, type=None, version=None):
        if data_location and not isinstance(data_location, str):
            raise TypeError("Expected argument 'data_location' to be a str")
        pulumi.set(__self__, "data_location", data_location)
        if host_name and not isinstance(host_name, str):
            raise TypeError("Expected argument 'host_name' to be a str")
        pulumi.set(__self__, "host_name", host_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if immutable_resource_id and not isinstance(immutable_resource_id, str):
            raise TypeError("Expected argument 'immutable_resource_id' to be a str")
        pulumi.set(__self__, "immutable_resource_id", immutable_resource_id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notification_hub_id and not isinstance(notification_hub_id, str):
            raise TypeError("Expected argument 'notification_hub_id' to be a str")
        pulumi.set(__self__, "notification_hub_id", notification_hub_id)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="dataLocation")
    def data_location(self) -> str:
        """
        The location where the communication service stores its data at rest.
        """
        return pulumi.get(self, "data_location")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> str:
        """
        FQDN of the CommunicationService instance.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="immutableResourceId")
    def immutable_resource_id(self) -> str:
        """
        The immutable resource Id of the communication service.
        """
        return pulumi.get(self, "immutable_resource_id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        The Azure location where the CommunicationService is running.
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
    @pulumi.getter(name="notificationHubId")
    def notification_hub_id(self) -> str:
        """
        Resource ID of an Azure Notification Hub linked to this resource.
        """
        return pulumi.get(self, "notification_hub_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags of the service which is a list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Version of the CommunicationService resource. Probably you need the same or higher version of client SDKs.
        """
        return pulumi.get(self, "version")


class AwaitableGetCommunicationServiceResult(GetCommunicationServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetCommunicationServiceResult(
            data_location=self.data_location,
            host_name=self.host_name,
            id=self.id,
            immutable_resource_id=self.immutable_resource_id,
            location=self.location,
            name=self.name,
            notification_hub_id=self.notification_hub_id,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            tags=self.tags,
            type=self.type,
            version=self.version)


def get_communication_service(communication_service_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetCommunicationServiceResult:
    """
    A class representing a CommunicationService resource.


    :param str communication_service_name: The name of the CommunicationService resource.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['communicationServiceName'] = communication_service_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:communication/v20200820:getCommunicationService', __args__, opts=opts, typ=GetCommunicationServiceResult).value

    return AwaitableGetCommunicationServiceResult(
        data_location=__ret__.data_location,
        host_name=__ret__.host_name,
        id=__ret__.id,
        immutable_resource_id=__ret__.immutable_resource_id,
        location=__ret__.location,
        name=__ret__.name,
        notification_hub_id=__ret__.notification_hub_id,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        type=__ret__.type,
        version=__ret__.version)
