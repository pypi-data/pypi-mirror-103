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

__all__ = ['SqlResourceSqlUserDefinedFunctionArgs', 'SqlResourceSqlUserDefinedFunction']

@pulumi.input_type
class SqlResourceSqlUserDefinedFunctionArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 container_name: pulumi.Input[str],
                 database_name: pulumi.Input[str],
                 options: pulumi.Input[Mapping[str, pulumi.Input[str]]],
                 resource: pulumi.Input['SqlUserDefinedFunctionResourceArgs'],
                 resource_group_name: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_defined_function_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SqlResourceSqlUserDefinedFunction resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] container_name: Cosmos DB container name.
        :param pulumi.Input[str] database_name: Cosmos DB database name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        :param pulumi.Input['SqlUserDefinedFunctionResourceArgs'] resource: The standard JSON format of a userDefinedFunction
        :param pulumi.Input[str] resource_group_name: Name of an Azure resource group.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        :param pulumi.Input[str] user_defined_function_name: Cosmos DB userDefinedFunction name.
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "container_name", container_name)
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "options", options)
        pulumi.set(__self__, "resource", resource)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if user_defined_function_name is not None:
            pulumi.set(__self__, "user_defined_function_name", user_defined_function_name)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        Cosmos DB database account name.
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> pulumi.Input[str]:
        """
        Cosmos DB container name.
        """
        return pulumi.get(self, "container_name")

    @container_name.setter
    def container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "container_name", value)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> pulumi.Input[str]:
        """
        Cosmos DB database name.
        """
        return pulumi.get(self, "database_name")

    @database_name.setter
    def database_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "database_name", value)

    @property
    @pulumi.getter
    def options(self) -> pulumi.Input[Mapping[str, pulumi.Input[str]]]:
        """
        A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        """
        return pulumi.get(self, "options")

    @options.setter
    def options(self, value: pulumi.Input[Mapping[str, pulumi.Input[str]]]):
        pulumi.set(self, "options", value)

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Input['SqlUserDefinedFunctionResourceArgs']:
        """
        The standard JSON format of a userDefinedFunction
        """
        return pulumi.get(self, "resource")

    @resource.setter
    def resource(self, value: pulumi.Input['SqlUserDefinedFunctionResourceArgs']):
        pulumi.set(self, "resource", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of an Azure resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="userDefinedFunctionName")
    def user_defined_function_name(self) -> Optional[pulumi.Input[str]]:
        """
        Cosmos DB userDefinedFunction name.
        """
        return pulumi.get(self, "user_defined_function_name")

    @user_defined_function_name.setter
    def user_defined_function_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_defined_function_name", value)


class SqlResourceSqlUserDefinedFunction(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 resource: Optional[pulumi.Input[pulumi.InputType['SqlUserDefinedFunctionResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_defined_function_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An Azure Cosmos DB userDefinedFunction.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] container_name: Cosmos DB container name.
        :param pulumi.Input[str] database_name: Cosmos DB database name.
        :param pulumi.Input[str] location: The location of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] options: A key-value pair of options to be applied for the request. This corresponds to the headers sent with the request.
        :param pulumi.Input[pulumi.InputType['SqlUserDefinedFunctionResourceArgs']] resource: The standard JSON format of a userDefinedFunction
        :param pulumi.Input[str] resource_group_name: Name of an Azure resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        :param pulumi.Input[str] user_defined_function_name: Cosmos DB userDefinedFunction name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SqlResourceSqlUserDefinedFunctionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An Azure Cosmos DB userDefinedFunction.

        :param str resource_name: The name of the resource.
        :param SqlResourceSqlUserDefinedFunctionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SqlResourceSqlUserDefinedFunctionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 options: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 resource: Optional[pulumi.Input[pulumi.InputType['SqlUserDefinedFunctionResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_defined_function_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SqlResourceSqlUserDefinedFunctionArgs.__new__(SqlResourceSqlUserDefinedFunctionArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            if container_name is None and not opts.urn:
                raise TypeError("Missing required property 'container_name'")
            __props__.__dict__["container_name"] = container_name
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__.__dict__["database_name"] = database_name
            __props__.__dict__["location"] = location
            if options is None and not opts.urn:
                raise TypeError("Missing required property 'options'")
            __props__.__dict__["options"] = options
            if resource is None and not opts.urn:
                raise TypeError("Missing required property 'resource'")
            __props__.__dict__["resource"] = resource
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["user_defined_function_name"] = user_defined_function_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:documentdb/v20190801:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20191212:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20191212:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20200301:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200301:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20200401:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200401:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20200601preview:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200601preview:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20200901:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200901:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20210115:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20210115:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20210301preview:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20210301preview:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-native:documentdb/v20210315:SqlResourceSqlUserDefinedFunction"), pulumi.Alias(type_="azure-nextgen:documentdb/v20210315:SqlResourceSqlUserDefinedFunction")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SqlResourceSqlUserDefinedFunction, __self__).__init__(
            'azure-native:documentdb/v20190801:SqlResourceSqlUserDefinedFunction',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SqlResourceSqlUserDefinedFunction':
        """
        Get an existing SqlResourceSqlUserDefinedFunction resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SqlResourceSqlUserDefinedFunctionArgs.__new__(SqlResourceSqlUserDefinedFunctionArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["resource"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return SqlResourceSqlUserDefinedFunction(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The location of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the ARM resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def resource(self) -> pulumi.Output[Optional['outputs.SqlUserDefinedFunctionGetPropertiesResponseResource']]:
        return pulumi.get(self, "resource")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags are a list of key-value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups). A maximum of 15 tags can be provided for a resource. Each tag must have a key no greater than 128 characters and value no greater than 256 characters. For example, the default experience for a template type is set with "defaultExperience": "Cassandra". Current "defaultExperience" values also include "Table", "Graph", "DocumentDB", and "MongoDB".
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")

