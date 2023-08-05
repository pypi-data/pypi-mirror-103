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
    'GetFileServerResult',
    'AwaitableGetFileServerResult',
    'get_file_server',
]

@pulumi.output_type
class GetFileServerResult:
    """
    File Server information.
    """
    def __init__(__self__, creation_time=None, data_disks=None, id=None, mount_settings=None, name=None, provisioning_state=None, provisioning_state_transition_time=None, ssh_configuration=None, subnet=None, type=None, vm_size=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if data_disks and not isinstance(data_disks, dict):
            raise TypeError("Expected argument 'data_disks' to be a dict")
        pulumi.set(__self__, "data_disks", data_disks)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if mount_settings and not isinstance(mount_settings, dict):
            raise TypeError("Expected argument 'mount_settings' to be a dict")
        pulumi.set(__self__, "mount_settings", mount_settings)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if provisioning_state_transition_time and not isinstance(provisioning_state_transition_time, str):
            raise TypeError("Expected argument 'provisioning_state_transition_time' to be a str")
        pulumi.set(__self__, "provisioning_state_transition_time", provisioning_state_transition_time)
        if ssh_configuration and not isinstance(ssh_configuration, dict):
            raise TypeError("Expected argument 'ssh_configuration' to be a dict")
        pulumi.set(__self__, "ssh_configuration", ssh_configuration)
        if subnet and not isinstance(subnet, dict):
            raise TypeError("Expected argument 'subnet' to be a dict")
        pulumi.set(__self__, "subnet", subnet)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vm_size and not isinstance(vm_size, str):
            raise TypeError("Expected argument 'vm_size' to be a str")
        pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        Time when the FileServer was created.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="dataDisks")
    def data_disks(self) -> Optional['outputs.DataDisksResponse']:
        """
        Information about disks attached to File Server VM.
        """
        return pulumi.get(self, "data_disks")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="mountSettings")
    def mount_settings(self) -> 'outputs.MountSettingsResponse':
        """
        File Server mount settings.
        """
        return pulumi.get(self, "mount_settings")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the File Server. Possible values: creating - The File Server is getting created; updating - The File Server creation has been accepted and it is getting updated; deleting - The user has requested that the File Server be deleted, and it is in the process of being deleted; failed - The File Server creation has failed with the specified error code. Details about the error code are specified in the message field; succeeded - The File Server creation has succeeded.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="provisioningStateTransitionTime")
    def provisioning_state_transition_time(self) -> str:
        """
        Time when the provisioning state was changed.
        """
        return pulumi.get(self, "provisioning_state_transition_time")

    @property
    @pulumi.getter(name="sshConfiguration")
    def ssh_configuration(self) -> Optional['outputs.SshConfigurationResponse']:
        """
        SSH configuration for accessing the File Server node.
        """
        return pulumi.get(self, "ssh_configuration")

    @property
    @pulumi.getter
    def subnet(self) -> Optional['outputs.ResourceIdResponse']:
        """
        File Server virtual network subnet resource ID.
        """
        return pulumi.get(self, "subnet")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> Optional[str]:
        """
        VM size of the File Server.
        """
        return pulumi.get(self, "vm_size")


class AwaitableGetFileServerResult(GetFileServerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFileServerResult(
            creation_time=self.creation_time,
            data_disks=self.data_disks,
            id=self.id,
            mount_settings=self.mount_settings,
            name=self.name,
            provisioning_state=self.provisioning_state,
            provisioning_state_transition_time=self.provisioning_state_transition_time,
            ssh_configuration=self.ssh_configuration,
            subnet=self.subnet,
            type=self.type,
            vm_size=self.vm_size)


def get_file_server(file_server_name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    workspace_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetFileServerResult:
    """
    File Server information.


    :param str file_server_name: The name of the file server within the specified resource group. File server names can only contain a combination of alphanumeric characters along with dash (-) and underscore (_). The name must be from 1 through 64 characters long.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str workspace_name: The name of the workspace. Workspace names can only contain a combination of alphanumeric characters along with dash (-) and underscore (_). The name must be from 1 through 64 characters long.
    """
    __args__ = dict()
    __args__['fileServerName'] = file_server_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:batchai/v20180501:getFileServer', __args__, opts=opts, typ=GetFileServerResult).value

    return AwaitableGetFileServerResult(
        creation_time=__ret__.creation_time,
        data_disks=__ret__.data_disks,
        id=__ret__.id,
        mount_settings=__ret__.mount_settings,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        provisioning_state_transition_time=__ret__.provisioning_state_transition_time,
        ssh_configuration=__ret__.ssh_configuration,
        subnet=__ret__.subnet,
        type=__ret__.type,
        vm_size=__ret__.vm_size)
