# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['SubnetArgs', 'Subnet']

@pulumi.input_type
class SubnetArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 virtual_network_name: pulumi.Input[str],
                 address_prefix: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group: Optional[pulumi.Input['NetworkSecurityGroupArgs']] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_navigation_links: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceNavigationLinkArgs']]]] = None,
                 route_table: Optional[pulumi.Input['RouteTableArgs']] = None,
                 subnet_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Subnet resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] virtual_network_name: The name of the virtual network.
        :param pulumi.Input[str] address_prefix: The address prefix for the subnet.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input['NetworkSecurityGroupArgs'] network_security_group: The reference of the NetworkSecurityGroup resource.
        :param pulumi.Input[str] provisioning_state: The provisioning state of the resource.
        :param pulumi.Input[Sequence[pulumi.Input['ResourceNavigationLinkArgs']]] resource_navigation_links: Gets an array of references to the external resources using subnet.
        :param pulumi.Input['RouteTableArgs'] route_table: The reference of the RouteTable resource.
        :param pulumi.Input[str] subnet_name: The name of the subnet.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "virtual_network_name", virtual_network_name)
        if address_prefix is not None:
            pulumi.set(__self__, "address_prefix", address_prefix)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if network_security_group is not None:
            pulumi.set(__self__, "network_security_group", network_security_group)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_navigation_links is not None:
            pulumi.set(__self__, "resource_navigation_links", resource_navigation_links)
        if route_table is not None:
            pulumi.set(__self__, "route_table", route_table)
        if subnet_name is not None:
            pulumi.set(__self__, "subnet_name", subnet_name)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="virtualNetworkName")
    def virtual_network_name(self) -> pulumi.Input[str]:
        """
        The name of the virtual network.
        """
        return pulumi.get(self, "virtual_network_name")

    @virtual_network_name.setter
    def virtual_network_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "virtual_network_name", value)

    @property
    @pulumi.getter(name="addressPrefix")
    def address_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        The address prefix for the subnet.
        """
        return pulumi.get(self, "address_prefix")

    @address_prefix.setter
    def address_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address_prefix", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="networkSecurityGroup")
    def network_security_group(self) -> Optional[pulumi.Input['NetworkSecurityGroupArgs']]:
        """
        The reference of the NetworkSecurityGroup resource.
        """
        return pulumi.get(self, "network_security_group")

    @network_security_group.setter
    def network_security_group(self, value: Optional[pulumi.Input['NetworkSecurityGroupArgs']]):
        pulumi.set(self, "network_security_group", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter(name="resourceNavigationLinks")
    def resource_navigation_links(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ResourceNavigationLinkArgs']]]]:
        """
        Gets an array of references to the external resources using subnet.
        """
        return pulumi.get(self, "resource_navigation_links")

    @resource_navigation_links.setter
    def resource_navigation_links(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ResourceNavigationLinkArgs']]]]):
        pulumi.set(self, "resource_navigation_links", value)

    @property
    @pulumi.getter(name="routeTable")
    def route_table(self) -> Optional[pulumi.Input['RouteTableArgs']]:
        """
        The reference of the RouteTable resource.
        """
        return pulumi.get(self, "route_table")

    @route_table.setter
    def route_table(self, value: Optional[pulumi.Input['RouteTableArgs']]):
        pulumi.set(self, "route_table", value)

    @property
    @pulumi.getter(name="subnetName")
    def subnet_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the subnet.
        """
        return pulumi.get(self, "subnet_name")

    @subnet_name.setter
    def subnet_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_name", value)


class Subnet(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_prefix: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group: Optional[pulumi.Input[pulumi.InputType['NetworkSecurityGroupArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_navigation_links: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceNavigationLinkArgs']]]]] = None,
                 route_table: Optional[pulumi.Input[pulumi.InputType['RouteTableArgs']]] = None,
                 subnet_name: Optional[pulumi.Input[str]] = None,
                 virtual_network_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Subnet in a virtual network resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_prefix: The address prefix for the subnet.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[pulumi.InputType['NetworkSecurityGroupArgs']] network_security_group: The reference of the NetworkSecurityGroup resource.
        :param pulumi.Input[str] provisioning_state: The provisioning state of the resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceNavigationLinkArgs']]]] resource_navigation_links: Gets an array of references to the external resources using subnet.
        :param pulumi.Input[pulumi.InputType['RouteTableArgs']] route_table: The reference of the RouteTable resource.
        :param pulumi.Input[str] subnet_name: The name of the subnet.
        :param pulumi.Input[str] virtual_network_name: The name of the virtual network.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SubnetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Subnet in a virtual network resource.

        :param str resource_name: The name of the resource.
        :param SubnetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SubnetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_prefix: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group: Optional[pulumi.Input[pulumi.InputType['NetworkSecurityGroupArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_navigation_links: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceNavigationLinkArgs']]]]] = None,
                 route_table: Optional[pulumi.Input[pulumi.InputType['RouteTableArgs']]] = None,
                 subnet_name: Optional[pulumi.Input[str]] = None,
                 virtual_network_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SubnetArgs.__new__(SubnetArgs)

            __props__.__dict__["address_prefix"] = address_prefix
            __props__.__dict__["etag"] = etag
            __props__.__dict__["id"] = id
            __props__.__dict__["name"] = name
            __props__.__dict__["network_security_group"] = network_security_group
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["resource_navigation_links"] = resource_navigation_links
            __props__.__dict__["route_table"] = route_table
            __props__.__dict__["subnet_name"] = subnet_name
            if virtual_network_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_network_name'")
            __props__.__dict__["virtual_network_name"] = virtual_network_name
            __props__.__dict__["ip_configurations"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/v20161201:Subnet"), pulumi.Alias(type_="azure-native:network:Subnet"), pulumi.Alias(type_="azure-nextgen:network:Subnet"), pulumi.Alias(type_="azure-native:network/v20150501preview:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20150501preview:Subnet"), pulumi.Alias(type_="azure-native:network/v20150615:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20150615:Subnet"), pulumi.Alias(type_="azure-native:network/v20160330:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20160330:Subnet"), pulumi.Alias(type_="azure-native:network/v20160601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20160601:Subnet"), pulumi.Alias(type_="azure-native:network/v20160901:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20160901:Subnet"), pulumi.Alias(type_="azure-native:network/v20170301:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170301:Subnet"), pulumi.Alias(type_="azure-native:network/v20170601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170601:Subnet"), pulumi.Alias(type_="azure-native:network/v20170801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170801:Subnet"), pulumi.Alias(type_="azure-native:network/v20170901:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170901:Subnet"), pulumi.Alias(type_="azure-native:network/v20171001:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20171001:Subnet"), pulumi.Alias(type_="azure-native:network/v20171101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20171101:Subnet"), pulumi.Alias(type_="azure-native:network/v20180101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180101:Subnet"), pulumi.Alias(type_="azure-native:network/v20180201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180201:Subnet"), pulumi.Alias(type_="azure-native:network/v20180401:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180401:Subnet"), pulumi.Alias(type_="azure-native:network/v20180601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180601:Subnet"), pulumi.Alias(type_="azure-native:network/v20180701:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180701:Subnet"), pulumi.Alias(type_="azure-native:network/v20180801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180801:Subnet"), pulumi.Alias(type_="azure-native:network/v20181001:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20181001:Subnet"), pulumi.Alias(type_="azure-native:network/v20181101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20181101:Subnet"), pulumi.Alias(type_="azure-native:network/v20181201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20181201:Subnet"), pulumi.Alias(type_="azure-native:network/v20190201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190201:Subnet"), pulumi.Alias(type_="azure-native:network/v20190401:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190401:Subnet"), pulumi.Alias(type_="azure-native:network/v20190601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190601:Subnet"), pulumi.Alias(type_="azure-native:network/v20190701:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190701:Subnet"), pulumi.Alias(type_="azure-native:network/v20190801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190801:Subnet"), pulumi.Alias(type_="azure-native:network/v20190901:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190901:Subnet"), pulumi.Alias(type_="azure-native:network/v20191101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20191101:Subnet"), pulumi.Alias(type_="azure-native:network/v20191201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20191201:Subnet"), pulumi.Alias(type_="azure-native:network/v20200301:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200301:Subnet"), pulumi.Alias(type_="azure-native:network/v20200401:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200401:Subnet"), pulumi.Alias(type_="azure-native:network/v20200501:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200501:Subnet"), pulumi.Alias(type_="azure-native:network/v20200601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200601:Subnet"), pulumi.Alias(type_="azure-native:network/v20200701:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200701:Subnet"), pulumi.Alias(type_="azure-native:network/v20200801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200801:Subnet"), pulumi.Alias(type_="azure-native:network/v20201101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20201101:Subnet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Subnet, __self__).__init__(
            'azure-native:network/v20161201:Subnet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Subnet':
        """
        Get an existing Subnet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SubnetArgs.__new__(SubnetArgs)

        __props__.__dict__["address_prefix"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["ip_configurations"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_security_group"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_navigation_links"] = None
        __props__.__dict__["route_table"] = None
        return Subnet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressPrefix")
    def address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The address prefix for the subnet.
        """
        return pulumi.get(self, "address_prefix")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> pulumi.Output[Sequence['outputs.IPConfigurationResponse']]:
        """
        Gets an array of references to the network interface IP configurations using subnet.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkSecurityGroup")
    def network_security_group(self) -> pulumi.Output[Optional['outputs.NetworkSecurityGroupResponse']]:
        """
        The reference of the NetworkSecurityGroup resource.
        """
        return pulumi.get(self, "network_security_group")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceNavigationLinks")
    def resource_navigation_links(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceNavigationLinkResponse']]]:
        """
        Gets an array of references to the external resources using subnet.
        """
        return pulumi.get(self, "resource_navigation_links")

    @property
    @pulumi.getter(name="routeTable")
    def route_table(self) -> pulumi.Output[Optional['outputs.RouteTableResponse']]:
        """
        The reference of the RouteTable resource.
        """
        return pulumi.get(self, "route_table")

