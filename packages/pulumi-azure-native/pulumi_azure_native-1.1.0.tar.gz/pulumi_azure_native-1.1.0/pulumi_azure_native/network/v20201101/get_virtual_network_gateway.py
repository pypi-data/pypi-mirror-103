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
    'GetVirtualNetworkGatewayResult',
    'AwaitableGetVirtualNetworkGatewayResult',
    'get_virtual_network_gateway',
]

@pulumi.output_type
class GetVirtualNetworkGatewayResult:
    """
    A common class for general resource information.
    """
    def __init__(__self__, active_active=None, bgp_settings=None, custom_routes=None, enable_bgp=None, enable_dns_forwarding=None, enable_private_ip_address=None, etag=None, gateway_default_site=None, gateway_type=None, id=None, inbound_dns_forwarding_endpoint=None, ip_configurations=None, location=None, name=None, provisioning_state=None, resource_guid=None, sku=None, tags=None, type=None, v_net_extended_location_resource_id=None, virtual_network_extended_location=None, vpn_client_configuration=None, vpn_gateway_generation=None, vpn_type=None):
        if active_active and not isinstance(active_active, bool):
            raise TypeError("Expected argument 'active_active' to be a bool")
        pulumi.set(__self__, "active_active", active_active)
        if bgp_settings and not isinstance(bgp_settings, dict):
            raise TypeError("Expected argument 'bgp_settings' to be a dict")
        pulumi.set(__self__, "bgp_settings", bgp_settings)
        if custom_routes and not isinstance(custom_routes, dict):
            raise TypeError("Expected argument 'custom_routes' to be a dict")
        pulumi.set(__self__, "custom_routes", custom_routes)
        if enable_bgp and not isinstance(enable_bgp, bool):
            raise TypeError("Expected argument 'enable_bgp' to be a bool")
        pulumi.set(__self__, "enable_bgp", enable_bgp)
        if enable_dns_forwarding and not isinstance(enable_dns_forwarding, bool):
            raise TypeError("Expected argument 'enable_dns_forwarding' to be a bool")
        pulumi.set(__self__, "enable_dns_forwarding", enable_dns_forwarding)
        if enable_private_ip_address and not isinstance(enable_private_ip_address, bool):
            raise TypeError("Expected argument 'enable_private_ip_address' to be a bool")
        pulumi.set(__self__, "enable_private_ip_address", enable_private_ip_address)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if gateway_default_site and not isinstance(gateway_default_site, dict):
            raise TypeError("Expected argument 'gateway_default_site' to be a dict")
        pulumi.set(__self__, "gateway_default_site", gateway_default_site)
        if gateway_type and not isinstance(gateway_type, str):
            raise TypeError("Expected argument 'gateway_type' to be a str")
        pulumi.set(__self__, "gateway_type", gateway_type)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if inbound_dns_forwarding_endpoint and not isinstance(inbound_dns_forwarding_endpoint, str):
            raise TypeError("Expected argument 'inbound_dns_forwarding_endpoint' to be a str")
        pulumi.set(__self__, "inbound_dns_forwarding_endpoint", inbound_dns_forwarding_endpoint)
        if ip_configurations and not isinstance(ip_configurations, list):
            raise TypeError("Expected argument 'ip_configurations' to be a list")
        pulumi.set(__self__, "ip_configurations", ip_configurations)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_guid and not isinstance(resource_guid, str):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, "resource_guid", resource_guid)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if v_net_extended_location_resource_id and not isinstance(v_net_extended_location_resource_id, str):
            raise TypeError("Expected argument 'v_net_extended_location_resource_id' to be a str")
        pulumi.set(__self__, "v_net_extended_location_resource_id", v_net_extended_location_resource_id)
        if virtual_network_extended_location and not isinstance(virtual_network_extended_location, dict):
            raise TypeError("Expected argument 'virtual_network_extended_location' to be a dict")
        pulumi.set(__self__, "virtual_network_extended_location", virtual_network_extended_location)
        if vpn_client_configuration and not isinstance(vpn_client_configuration, dict):
            raise TypeError("Expected argument 'vpn_client_configuration' to be a dict")
        pulumi.set(__self__, "vpn_client_configuration", vpn_client_configuration)
        if vpn_gateway_generation and not isinstance(vpn_gateway_generation, str):
            raise TypeError("Expected argument 'vpn_gateway_generation' to be a str")
        pulumi.set(__self__, "vpn_gateway_generation", vpn_gateway_generation)
        if vpn_type and not isinstance(vpn_type, str):
            raise TypeError("Expected argument 'vpn_type' to be a str")
        pulumi.set(__self__, "vpn_type", vpn_type)

    @property
    @pulumi.getter(name="activeActive")
    def active_active(self) -> Optional[bool]:
        """
        ActiveActive flag.
        """
        return pulumi.get(self, "active_active")

    @property
    @pulumi.getter(name="bgpSettings")
    def bgp_settings(self) -> Optional['outputs.BgpSettingsResponse']:
        """
        Virtual network gateway's BGP speaker settings.
        """
        return pulumi.get(self, "bgp_settings")

    @property
    @pulumi.getter(name="customRoutes")
    def custom_routes(self) -> Optional['outputs.AddressSpaceResponse']:
        """
        The reference to the address space resource which represents the custom routes address space specified by the customer for virtual network gateway and VpnClient.
        """
        return pulumi.get(self, "custom_routes")

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> Optional[bool]:
        """
        Whether BGP is enabled for this virtual network gateway or not.
        """
        return pulumi.get(self, "enable_bgp")

    @property
    @pulumi.getter(name="enableDnsForwarding")
    def enable_dns_forwarding(self) -> Optional[bool]:
        """
        Whether dns forwarding is enabled or not.
        """
        return pulumi.get(self, "enable_dns_forwarding")

    @property
    @pulumi.getter(name="enablePrivateIpAddress")
    def enable_private_ip_address(self) -> Optional[bool]:
        """
        Whether private IP needs to be enabled on this gateway for connections or not.
        """
        return pulumi.get(self, "enable_private_ip_address")

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="gatewayDefaultSite")
    def gateway_default_site(self) -> Optional['outputs.SubResourceResponse']:
        """
        The reference to the LocalNetworkGateway resource which represents local network site having default routes. Assign Null value in case of removing existing default site setting.
        """
        return pulumi.get(self, "gateway_default_site")

    @property
    @pulumi.getter(name="gatewayType")
    def gateway_type(self) -> Optional[str]:
        """
        The type of this virtual network gateway.
        """
        return pulumi.get(self, "gateway_type")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inboundDnsForwardingEndpoint")
    def inbound_dns_forwarding_endpoint(self) -> str:
        """
        The IP address allocated by the gateway to which dns requests can be sent.
        """
        return pulumi.get(self, "inbound_dns_forwarding_endpoint")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> Optional[Sequence['outputs.VirtualNetworkGatewayIPConfigurationResponse']]:
        """
        IP configurations for virtual network gateway.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the virtual network gateway resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> str:
        """
        The resource GUID property of the virtual network gateway resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.VirtualNetworkGatewaySkuResponse']:
        """
        The reference to the VirtualNetworkGatewaySku resource which represents the SKU selected for Virtual network gateway.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vNetExtendedLocationResourceId")
    def v_net_extended_location_resource_id(self) -> Optional[str]:
        """
        MAS FIJI customer vnet resource id. VirtualNetworkGateway of type local gateway is associated with the customer vnet.
        """
        return pulumi.get(self, "v_net_extended_location_resource_id")

    @property
    @pulumi.getter(name="virtualNetworkExtendedLocation")
    def virtual_network_extended_location(self) -> Optional['outputs.ExtendedLocationResponse']:
        """
        The extended location of type local virtual network gateway.
        """
        return pulumi.get(self, "virtual_network_extended_location")

    @property
    @pulumi.getter(name="vpnClientConfiguration")
    def vpn_client_configuration(self) -> Optional['outputs.VpnClientConfigurationResponse']:
        """
        The reference to the VpnClientConfiguration resource which represents the P2S VpnClient configurations.
        """
        return pulumi.get(self, "vpn_client_configuration")

    @property
    @pulumi.getter(name="vpnGatewayGeneration")
    def vpn_gateway_generation(self) -> Optional[str]:
        """
        The generation for this VirtualNetworkGateway. Must be None if gatewayType is not VPN.
        """
        return pulumi.get(self, "vpn_gateway_generation")

    @property
    @pulumi.getter(name="vpnType")
    def vpn_type(self) -> Optional[str]:
        """
        The type of this virtual network gateway.
        """
        return pulumi.get(self, "vpn_type")


class AwaitableGetVirtualNetworkGatewayResult(GetVirtualNetworkGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkGatewayResult(
            active_active=self.active_active,
            bgp_settings=self.bgp_settings,
            custom_routes=self.custom_routes,
            enable_bgp=self.enable_bgp,
            enable_dns_forwarding=self.enable_dns_forwarding,
            enable_private_ip_address=self.enable_private_ip_address,
            etag=self.etag,
            gateway_default_site=self.gateway_default_site,
            gateway_type=self.gateway_type,
            id=self.id,
            inbound_dns_forwarding_endpoint=self.inbound_dns_forwarding_endpoint,
            ip_configurations=self.ip_configurations,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            resource_guid=self.resource_guid,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            v_net_extended_location_resource_id=self.v_net_extended_location_resource_id,
            virtual_network_extended_location=self.virtual_network_extended_location,
            vpn_client_configuration=self.vpn_client_configuration,
            vpn_gateway_generation=self.vpn_gateway_generation,
            vpn_type=self.vpn_type)


def get_virtual_network_gateway(resource_group_name: Optional[str] = None,
                                virtual_network_gateway_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualNetworkGatewayResult:
    """
    A common class for general resource information.


    :param str resource_group_name: The name of the resource group.
    :param str virtual_network_gateway_name: The name of the virtual network gateway.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['virtualNetworkGatewayName'] = virtual_network_gateway_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20201101:getVirtualNetworkGateway', __args__, opts=opts, typ=GetVirtualNetworkGatewayResult).value

    return AwaitableGetVirtualNetworkGatewayResult(
        active_active=__ret__.active_active,
        bgp_settings=__ret__.bgp_settings,
        custom_routes=__ret__.custom_routes,
        enable_bgp=__ret__.enable_bgp,
        enable_dns_forwarding=__ret__.enable_dns_forwarding,
        enable_private_ip_address=__ret__.enable_private_ip_address,
        etag=__ret__.etag,
        gateway_default_site=__ret__.gateway_default_site,
        gateway_type=__ret__.gateway_type,
        id=__ret__.id,
        inbound_dns_forwarding_endpoint=__ret__.inbound_dns_forwarding_endpoint,
        ip_configurations=__ret__.ip_configurations,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        resource_guid=__ret__.resource_guid,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        v_net_extended_location_resource_id=__ret__.v_net_extended_location_resource_id,
        virtual_network_extended_location=__ret__.virtual_network_extended_location,
        vpn_client_configuration=__ret__.vpn_client_configuration,
        vpn_gateway_generation=__ret__.vpn_gateway_generation,
        vpn_type=__ret__.vpn_type)
