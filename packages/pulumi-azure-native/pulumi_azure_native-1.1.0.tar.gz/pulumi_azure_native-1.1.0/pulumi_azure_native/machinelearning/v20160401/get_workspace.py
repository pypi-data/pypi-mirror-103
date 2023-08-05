# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetWorkspaceResult',
    'AwaitableGetWorkspaceResult',
    'get_workspace',
]

@pulumi.output_type
class GetWorkspaceResult:
    """
    An object that represents a machine learning workspace.
    """
    def __init__(__self__, creation_time=None, id=None, key_vault_identifier_id=None, location=None, name=None, owner_email=None, studio_endpoint=None, tags=None, type=None, user_storage_account_id=None, workspace_id=None, workspace_state=None, workspace_type=None):
        if creation_time and not isinstance(creation_time, str):
            raise TypeError("Expected argument 'creation_time' to be a str")
        pulumi.set(__self__, "creation_time", creation_time)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key_vault_identifier_id and not isinstance(key_vault_identifier_id, str):
            raise TypeError("Expected argument 'key_vault_identifier_id' to be a str")
        pulumi.set(__self__, "key_vault_identifier_id", key_vault_identifier_id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if owner_email and not isinstance(owner_email, str):
            raise TypeError("Expected argument 'owner_email' to be a str")
        pulumi.set(__self__, "owner_email", owner_email)
        if studio_endpoint and not isinstance(studio_endpoint, str):
            raise TypeError("Expected argument 'studio_endpoint' to be a str")
        pulumi.set(__self__, "studio_endpoint", studio_endpoint)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_storage_account_id and not isinstance(user_storage_account_id, str):
            raise TypeError("Expected argument 'user_storage_account_id' to be a str")
        pulumi.set(__self__, "user_storage_account_id", user_storage_account_id)
        if workspace_id and not isinstance(workspace_id, str):
            raise TypeError("Expected argument 'workspace_id' to be a str")
        pulumi.set(__self__, "workspace_id", workspace_id)
        if workspace_state and not isinstance(workspace_state, str):
            raise TypeError("Expected argument 'workspace_state' to be a str")
        pulumi.set(__self__, "workspace_state", workspace_state)
        if workspace_type and not isinstance(workspace_type, str):
            raise TypeError("Expected argument 'workspace_type' to be a str")
        pulumi.set(__self__, "workspace_type", workspace_type)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> str:
        """
        The creation time for this workspace resource.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="keyVaultIdentifierId")
    def key_vault_identifier_id(self) -> Optional[str]:
        """
        The key vault identifier used for encrypted workspaces.
        """
        return pulumi.get(self, "key_vault_identifier_id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerEmail")
    def owner_email(self) -> str:
        """
        The email id of the owner for this workspace.
        """
        return pulumi.get(self, "owner_email")

    @property
    @pulumi.getter(name="studioEndpoint")
    def studio_endpoint(self) -> str:
        """
        The regional endpoint for the machine learning studio service which hosts this workspace.
        """
        return pulumi.get(self, "studio_endpoint")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userStorageAccountId")
    def user_storage_account_id(self) -> str:
        """
        The fully qualified arm id of the storage account associated with this workspace.
        """
        return pulumi.get(self, "user_storage_account_id")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        The immutable id associated with this workspace.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="workspaceState")
    def workspace_state(self) -> str:
        """
        The current state of workspace resource.
        """
        return pulumi.get(self, "workspace_state")

    @property
    @pulumi.getter(name="workspaceType")
    def workspace_type(self) -> str:
        """
        The type of this workspace.
        """
        return pulumi.get(self, "workspace_type")


class AwaitableGetWorkspaceResult(GetWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspaceResult(
            creation_time=self.creation_time,
            id=self.id,
            key_vault_identifier_id=self.key_vault_identifier_id,
            location=self.location,
            name=self.name,
            owner_email=self.owner_email,
            studio_endpoint=self.studio_endpoint,
            tags=self.tags,
            type=self.type,
            user_storage_account_id=self.user_storage_account_id,
            workspace_id=self.workspace_id,
            workspace_state=self.workspace_state,
            workspace_type=self.workspace_type)


def get_workspace(resource_group_name: Optional[str] = None,
                  workspace_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspaceResult:
    """
    An object that represents a machine learning workspace.


    :param str resource_group_name: The name of the resource group to which the machine learning workspace belongs.
    :param str workspace_name: The name of the machine learning workspace.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:machinelearning/v20160401:getWorkspace', __args__, opts=opts, typ=GetWorkspaceResult).value

    return AwaitableGetWorkspaceResult(
        creation_time=__ret__.creation_time,
        id=__ret__.id,
        key_vault_identifier_id=__ret__.key_vault_identifier_id,
        location=__ret__.location,
        name=__ret__.name,
        owner_email=__ret__.owner_email,
        studio_endpoint=__ret__.studio_endpoint,
        tags=__ret__.tags,
        type=__ret__.type,
        user_storage_account_id=__ret__.user_storage_account_id,
        workspace_id=__ret__.workspace_id,
        workspace_state=__ret__.workspace_state,
        workspace_type=__ret__.workspace_type)
