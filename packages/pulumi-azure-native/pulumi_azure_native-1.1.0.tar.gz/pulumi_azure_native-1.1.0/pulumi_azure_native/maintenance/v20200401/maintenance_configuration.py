# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = ['MaintenanceConfigurationArgs', 'MaintenanceConfiguration']

@pulumi.input_type
class MaintenanceConfigurationArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 extension_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_scope: Optional[pulumi.Input[Union[str, 'MaintenanceScope']]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 resource_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a MaintenanceConfiguration resource.
        :param pulumi.Input[str] resource_group_name: Resource Group Name
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] extension_properties: Gets or sets extensionProperties of the maintenanceConfiguration. This is for future use only and would be a set of key value pairs for additional information e.g. whether to follow SDP etc.
        :param pulumi.Input[str] location: Gets or sets location of the resource
        :param pulumi.Input[Union[str, 'MaintenanceScope']] maintenance_scope: Gets or sets maintenanceScope of the configuration. It represent the impact area of the maintenance
        :param pulumi.Input[str] namespace: Gets or sets namespace of the resource e.g. Microsoft.Maintenance or Microsoft.Sql
        :param pulumi.Input[str] resource_name: Resource Identifier
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets tags of the resource
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if extension_properties is not None:
            pulumi.set(__self__, "extension_properties", extension_properties)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if maintenance_scope is not None:
            pulumi.set(__self__, "maintenance_scope", maintenance_scope)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if resource_name is not None:
            pulumi.set(__self__, "resource_name", resource_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Resource Group Name
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="extensionProperties")
    def extension_properties(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Gets or sets extensionProperties of the maintenanceConfiguration. This is for future use only and would be a set of key value pairs for additional information e.g. whether to follow SDP etc.
        """
        return pulumi.get(self, "extension_properties")

    @extension_properties.setter
    def extension_properties(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "extension_properties", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets location of the resource
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="maintenanceScope")
    def maintenance_scope(self) -> Optional[pulumi.Input[Union[str, 'MaintenanceScope']]]:
        """
        Gets or sets maintenanceScope of the configuration. It represent the impact area of the maintenance
        """
        return pulumi.get(self, "maintenance_scope")

    @maintenance_scope.setter
    def maintenance_scope(self, value: Optional[pulumi.Input[Union[str, 'MaintenanceScope']]]):
        pulumi.set(self, "maintenance_scope", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets namespace of the resource e.g. Microsoft.Maintenance or Microsoft.Sql
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Identifier
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Gets or sets tags of the resource
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class MaintenanceConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 extension_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_scope: Optional[pulumi.Input[Union[str, 'MaintenanceScope']]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Maintenance configuration record type

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] extension_properties: Gets or sets extensionProperties of the maintenanceConfiguration. This is for future use only and would be a set of key value pairs for additional information e.g. whether to follow SDP etc.
        :param pulumi.Input[str] location: Gets or sets location of the resource
        :param pulumi.Input[Union[str, 'MaintenanceScope']] maintenance_scope: Gets or sets maintenanceScope of the configuration. It represent the impact area of the maintenance
        :param pulumi.Input[str] namespace: Gets or sets namespace of the resource e.g. Microsoft.Maintenance or Microsoft.Sql
        :param pulumi.Input[str] resource_group_name: Resource Group Name
        :param pulumi.Input[str] resource_name_: Resource Identifier
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Gets or sets tags of the resource
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MaintenanceConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Maintenance configuration record type

        :param str resource_name: The name of the resource.
        :param MaintenanceConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MaintenanceConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 extension_properties: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 maintenance_scope: Optional[pulumi.Input[Union[str, 'MaintenanceScope']]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = MaintenanceConfigurationArgs.__new__(MaintenanceConfigurationArgs)

            __props__.__dict__["extension_properties"] = extension_properties
            __props__.__dict__["location"] = location
            __props__.__dict__["maintenance_scope"] = maintenance_scope
            __props__.__dict__["namespace"] = namespace
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:maintenance/v20200401:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:maintenance:MaintenanceConfiguration"), pulumi.Alias(type_="azure-nextgen:maintenance:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:maintenance/v20180601preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-nextgen:maintenance/v20180601preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:maintenance/v20200701preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-nextgen:maintenance/v20200701preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-native:maintenance/v20210401preview:MaintenanceConfiguration"), pulumi.Alias(type_="azure-nextgen:maintenance/v20210401preview:MaintenanceConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(MaintenanceConfiguration, __self__).__init__(
            'azure-native:maintenance/v20200401:MaintenanceConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'MaintenanceConfiguration':
        """
        Get an existing MaintenanceConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = MaintenanceConfigurationArgs.__new__(MaintenanceConfigurationArgs)

        __props__.__dict__["extension_properties"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["maintenance_scope"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["namespace"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return MaintenanceConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="extensionProperties")
    def extension_properties(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Gets or sets extensionProperties of the maintenanceConfiguration. This is for future use only and would be a set of key value pairs for additional information e.g. whether to follow SDP etc.
        """
        return pulumi.get(self, "extension_properties")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets location of the resource
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maintenanceScope")
    def maintenance_scope(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets maintenanceScope of the configuration. It represent the impact area of the maintenance
        """
        return pulumi.get(self, "maintenance_scope")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets namespace of the resource e.g. Microsoft.Maintenance or Microsoft.Sql
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Gets or sets tags of the resource
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource
        """
        return pulumi.get(self, "type")

