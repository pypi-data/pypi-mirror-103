# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['CassandraDataCenterArgs', 'CassandraDataCenter']

@pulumi.input_type
class CassandraDataCenterArgs:
    def __init__(__self__, *,
                 cluster_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 data_center_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['DataCenterResourcePropertiesArgs']] = None):
        """
        The set of arguments for constructing a CassandraDataCenter resource.
        :param pulumi.Input[str] cluster_name: Managed Cassandra cluster name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] data_center_name: Data center name in a managed Cassandra cluster.
        :param pulumi.Input['DataCenterResourcePropertiesArgs'] properties: Properties of a managed Cassandra data center.
        """
        pulumi.set(__self__, "cluster_name", cluster_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if data_center_name is not None:
            pulumi.set(__self__, "data_center_name", data_center_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Input[str]:
        """
        Managed Cassandra cluster name.
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="dataCenterName")
    def data_center_name(self) -> Optional[pulumi.Input[str]]:
        """
        Data center name in a managed Cassandra cluster.
        """
        return pulumi.get(self, "data_center_name")

    @data_center_name.setter
    def data_center_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_center_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['DataCenterResourcePropertiesArgs']]:
        """
        Properties of a managed Cassandra data center.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['DataCenterResourcePropertiesArgs']]):
        pulumi.set(self, "properties", value)


class CassandraDataCenter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 data_center_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['DataCenterResourcePropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A managed Cassandra data center.
        API Version: 2021-03-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_name: Managed Cassandra cluster name.
        :param pulumi.Input[str] data_center_name: Data center name in a managed Cassandra cluster.
        :param pulumi.Input[pulumi.InputType['DataCenterResourcePropertiesArgs']] properties: Properties of a managed Cassandra data center.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CassandraDataCenterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A managed Cassandra data center.
        API Version: 2021-03-01-preview.

        :param str resource_name: The name of the resource.
        :param CassandraDataCenterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CassandraDataCenterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 data_center_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['DataCenterResourcePropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = CassandraDataCenterArgs.__new__(CassandraDataCenterArgs)

            if cluster_name is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_name'")
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["data_center_name"] = data_center_name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:documentdb:CassandraDataCenter"), pulumi.Alias(type_="azure-native:documentdb/v20210301preview:CassandraDataCenter"), pulumi.Alias(type_="azure-nextgen:documentdb/v20210301preview:CassandraDataCenter")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(CassandraDataCenter, __self__).__init__(
            'azure-native:documentdb:CassandraDataCenter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'CassandraDataCenter':
        """
        Get an existing CassandraDataCenter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = CassandraDataCenterArgs.__new__(CassandraDataCenterArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return CassandraDataCenter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the database account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.DataCenterResourceResponseProperties']:
        """
        Properties of a managed Cassandra data center.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")

