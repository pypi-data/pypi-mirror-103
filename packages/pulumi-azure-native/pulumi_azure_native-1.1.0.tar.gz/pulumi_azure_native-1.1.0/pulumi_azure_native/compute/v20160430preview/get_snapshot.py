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
    'GetSnapshotResult',
    'AwaitableGetSnapshotResult',
    'get_snapshot',
]

@pulumi.output_type
class GetSnapshotResult:
    """
    Snapshot resource.
    """
    def __init__(__self__, account_type=None, creation_data=None, disk_size_gb=None, encryption_settings=None, id=None, location=None, name=None, os_type=None, owner_id=None, provisioning_state=None, tags=None, time_created=None, type=None):
        if account_type and not isinstance(account_type, str):
            raise TypeError("Expected argument 'account_type' to be a str")
        pulumi.set(__self__, "account_type", account_type)
        if creation_data and not isinstance(creation_data, dict):
            raise TypeError("Expected argument 'creation_data' to be a dict")
        pulumi.set(__self__, "creation_data", creation_data)
        if disk_size_gb and not isinstance(disk_size_gb, int):
            raise TypeError("Expected argument 'disk_size_gb' to be a int")
        pulumi.set(__self__, "disk_size_gb", disk_size_gb)
        if encryption_settings and not isinstance(encryption_settings, dict):
            raise TypeError("Expected argument 'encryption_settings' to be a dict")
        pulumi.set(__self__, "encryption_settings", encryption_settings)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if time_created and not isinstance(time_created, str):
            raise TypeError("Expected argument 'time_created' to be a str")
        pulumi.set(__self__, "time_created", time_created)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> Optional[str]:
        """
        the storage account type of the disk.
        """
        return pulumi.get(self, "account_type")

    @property
    @pulumi.getter(name="creationData")
    def creation_data(self) -> 'outputs.CreationDataResponse':
        """
        Disk source information. CreationData information cannot be changed after the disk has been created.
        """
        return pulumi.get(self, "creation_data")

    @property
    @pulumi.getter(name="diskSizeGB")
    def disk_size_gb(self) -> Optional[int]:
        """
        If creationData.createOption is Empty, this field is mandatory and it indicates the size of the VHD to create. If this field is present for updates or creation with other options, it indicates a resize. Resizes are only allowed if the disk is not attached to a running VM, and can only increase the disk's size.
        """
        return pulumi.get(self, "disk_size_gb")

    @property
    @pulumi.getter(name="encryptionSettings")
    def encryption_settings(self) -> Optional['outputs.EncryptionSettingsResponse']:
        """
        Encryption settings for disk or snapshot
        """
        return pulumi.get(self, "encryption_settings")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[str]:
        """
        The Operating System type.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        """
        A relative URI containing the VM id that has the disk attached.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The disk provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeCreated")
    def time_created(self) -> str:
        """
        The time when the disk was created.
        """
        return pulumi.get(self, "time_created")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetSnapshotResult(GetSnapshotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSnapshotResult(
            account_type=self.account_type,
            creation_data=self.creation_data,
            disk_size_gb=self.disk_size_gb,
            encryption_settings=self.encryption_settings,
            id=self.id,
            location=self.location,
            name=self.name,
            os_type=self.os_type,
            owner_id=self.owner_id,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            time_created=self.time_created,
            type=self.type)


def get_snapshot(resource_group_name: Optional[str] = None,
                 snapshot_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSnapshotResult:
    """
    Snapshot resource.


    :param str resource_group_name: The name of the resource group.
    :param str snapshot_name: The name of the snapshot within the given subscription and resource group.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['snapshotName'] = snapshot_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:compute/v20160430preview:getSnapshot', __args__, opts=opts, typ=GetSnapshotResult).value

    return AwaitableGetSnapshotResult(
        account_type=__ret__.account_type,
        creation_data=__ret__.creation_data,
        disk_size_gb=__ret__.disk_size_gb,
        encryption_settings=__ret__.encryption_settings,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        os_type=__ret__.os_type,
        owner_id=__ret__.owner_id,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        time_created=__ret__.time_created,
        type=__ret__.type)
