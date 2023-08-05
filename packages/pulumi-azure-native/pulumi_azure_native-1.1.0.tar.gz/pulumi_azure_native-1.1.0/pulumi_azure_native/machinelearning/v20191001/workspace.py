# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['WorkspaceArgs', 'Workspace']

@pulumi.input_type
class WorkspaceArgs:
    def __init__(__self__, *,
                 owner_email: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 user_storage_account_id: pulumi.Input[str],
                 key_vault_identifier_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input['SkuArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Workspace resource.
        :param pulumi.Input[str] owner_email: The email id of the owner for this workspace.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the machine learning workspace belongs.
        :param pulumi.Input[str] user_storage_account_id: The fully qualified arm id of the storage account associated with this workspace.
        :param pulumi.Input[str] key_vault_identifier_id: The key vault identifier used for encrypted workspaces.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input['SkuArgs'] sku: The sku of the workspace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] workspace_name: The name of the machine learning workspace.
        """
        pulumi.set(__self__, "owner_email", owner_email)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "user_storage_account_id", user_storage_account_id)
        if key_vault_identifier_id is not None:
            pulumi.set(__self__, "key_vault_identifier_id", key_vault_identifier_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if workspace_name is not None:
            pulumi.set(__self__, "workspace_name", workspace_name)

    @property
    @pulumi.getter(name="ownerEmail")
    def owner_email(self) -> pulumi.Input[str]:
        """
        The email id of the owner for this workspace.
        """
        return pulumi.get(self, "owner_email")

    @owner_email.setter
    def owner_email(self, value: pulumi.Input[str]):
        pulumi.set(self, "owner_email", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group to which the machine learning workspace belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="userStorageAccountId")
    def user_storage_account_id(self) -> pulumi.Input[str]:
        """
        The fully qualified arm id of the storage account associated with this workspace.
        """
        return pulumi.get(self, "user_storage_account_id")

    @user_storage_account_id.setter
    def user_storage_account_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_storage_account_id", value)

    @property
    @pulumi.getter(name="keyVaultIdentifierId")
    def key_vault_identifier_id(self) -> Optional[pulumi.Input[str]]:
        """
        The key vault identifier used for encrypted workspaces.
        """
        return pulumi.get(self, "key_vault_identifier_id")

    @key_vault_identifier_id.setter
    def key_vault_identifier_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_identifier_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input['SkuArgs']]:
        """
        The sku of the workspace.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input['SkuArgs']]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="workspaceName")
    def workspace_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the machine learning workspace.
        """
        return pulumi.get(self, "workspace_name")

    @workspace_name.setter
    def workspace_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_name", value)


class Workspace(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_vault_identifier_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 owner_email: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_storage_account_id: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An object that represents a machine learning workspace.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] key_vault_identifier_id: The key vault identifier used for encrypted workspaces.
        :param pulumi.Input[str] location: The location of the resource. This cannot be changed after the resource is created.
        :param pulumi.Input[str] owner_email: The email id of the owner for this workspace.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to which the machine learning workspace belongs.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku of the workspace.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] user_storage_account_id: The fully qualified arm id of the storage account associated with this workspace.
        :param pulumi.Input[str] workspace_name: The name of the machine learning workspace.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WorkspaceArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An object that represents a machine learning workspace.

        :param str resource_name: The name of the resource.
        :param WorkspaceArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WorkspaceArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 key_vault_identifier_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 owner_email: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_storage_account_id: Optional[pulumi.Input[str]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WorkspaceArgs.__new__(WorkspaceArgs)

            __props__.__dict__["key_vault_identifier_id"] = key_vault_identifier_id
            __props__.__dict__["location"] = location
            if owner_email is None and not opts.urn:
                raise TypeError("Missing required property 'owner_email'")
            __props__.__dict__["owner_email"] = owner_email
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["sku"] = sku
            __props__.__dict__["tags"] = tags
            if user_storage_account_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_storage_account_id'")
            __props__.__dict__["user_storage_account_id"] = user_storage_account_id
            __props__.__dict__["workspace_name"] = workspace_name
            __props__.__dict__["creation_time"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["studio_endpoint"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["workspace_id"] = None
            __props__.__dict__["workspace_state"] = None
            __props__.__dict__["workspace_type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:machinelearning/v20191001:Workspace"), pulumi.Alias(type_="azure-native:machinelearning:Workspace"), pulumi.Alias(type_="azure-nextgen:machinelearning:Workspace"), pulumi.Alias(type_="azure-native:machinelearning/v20160401:Workspace"), pulumi.Alias(type_="azure-nextgen:machinelearning/v20160401:Workspace")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Workspace, __self__).__init__(
            'azure-native:machinelearning/v20191001:Workspace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Workspace':
        """
        Get an existing Workspace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WorkspaceArgs.__new__(WorkspaceArgs)

        __props__.__dict__["creation_time"] = None
        __props__.__dict__["key_vault_identifier_id"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["owner_email"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["studio_endpoint"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["user_storage_account_id"] = None
        __props__.__dict__["workspace_id"] = None
        __props__.__dict__["workspace_state"] = None
        __props__.__dict__["workspace_type"] = None
        return Workspace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[str]:
        """
        The creation time for this workspace resource.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter(name="keyVaultIdentifierId")
    def key_vault_identifier_id(self) -> pulumi.Output[Optional[str]]:
        """
        The key vault identifier used for encrypted workspaces.
        """
        return pulumi.get(self, "key_vault_identifier_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerEmail")
    def owner_email(self) -> pulumi.Output[str]:
        """
        The email id of the owner for this workspace.
        """
        return pulumi.get(self, "owner_email")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The sku of the workspace.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="studioEndpoint")
    def studio_endpoint(self) -> pulumi.Output[str]:
        """
        The regional endpoint for the machine learning studio service which hosts this workspace.
        """
        return pulumi.get(self, "studio_endpoint")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userStorageAccountId")
    def user_storage_account_id(self) -> pulumi.Output[str]:
        """
        The fully qualified arm id of the storage account associated with this workspace.
        """
        return pulumi.get(self, "user_storage_account_id")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The immutable id associated with this workspace.
        """
        return pulumi.get(self, "workspace_id")

    @property
    @pulumi.getter(name="workspaceState")
    def workspace_state(self) -> pulumi.Output[str]:
        """
        The current state of workspace resource.
        """
        return pulumi.get(self, "workspace_state")

    @property
    @pulumi.getter(name="workspaceType")
    def workspace_type(self) -> pulumi.Output[str]:
        """
        The type of this workspace.
        """
        return pulumi.get(self, "workspace_type")

