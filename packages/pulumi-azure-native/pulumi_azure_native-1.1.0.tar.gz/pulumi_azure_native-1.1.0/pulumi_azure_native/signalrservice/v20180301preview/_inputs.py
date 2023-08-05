# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'ResourceSkuArgs',
    'SignalRCreateOrUpdatePropertiesArgs',
]

@pulumi.input_type
class ResourceSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 capacity: Optional[pulumi.Input[int]] = None,
                 family: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[Union[str, 'SignalRSkuTier']]] = None):
        """
        The billing information of the resource.(e.g. basic vs. standard)
        :param pulumi.Input[str] name: The name of the SKU. This is typically a letter + number code, such as A0 or P3.  Required (if sku is specified)
        :param pulumi.Input[int] capacity: Optional, integer. If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not 
               possible for the resource this may be omitted.
        :param pulumi.Input[str] family: Optional, string. If the service has different generations of hardware, for the same SKU, then that can be captured here.
        :param pulumi.Input[str] size: Optional, string. When the name field is the combination of tier and some other value, this would be the standalone code.
        :param pulumi.Input[Union[str, 'SignalRSkuTier']] tier: Optional tier of this particular SKU. `Basic` is deprecated, use `Standard` instead for Basic tier
        """
        pulumi.set(__self__, "name", name)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if family is not None:
            pulumi.set(__self__, "family", family)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the SKU. This is typically a letter + number code, such as A0 or P3.  Required (if sku is specified)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        Optional, integer. If the SKU supports scale out/in then the capacity integer should be included. If scale out/in is not 
        possible for the resource this may be omitted.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def family(self) -> Optional[pulumi.Input[str]]:
        """
        Optional, string. If the service has different generations of hardware, for the same SKU, then that can be captured here.
        """
        return pulumi.get(self, "family")

    @family.setter
    def family(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "family", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        Optional, string. When the name field is the combination of tier and some other value, this would be the standalone code.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[Union[str, 'SignalRSkuTier']]]:
        """
        Optional tier of this particular SKU. `Basic` is deprecated, use `Standard` instead for Basic tier
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[Union[str, 'SignalRSkuTier']]]):
        pulumi.set(self, "tier", value)


@pulumi.input_type
class SignalRCreateOrUpdatePropertiesArgs:
    def __init__(__self__, *,
                 host_name_prefix: Optional[pulumi.Input[str]] = None):
        """
        Settings used to provision or configure the resource.
        :param pulumi.Input[str] host_name_prefix: Prefix for the hostName of the SignalR service. Retained for future use.
               The hostname will be of format: &lt;hostNamePrefix&gt;.service.signalr.net.
        """
        if host_name_prefix is not None:
            pulumi.set(__self__, "host_name_prefix", host_name_prefix)

    @property
    @pulumi.getter(name="hostNamePrefix")
    def host_name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Prefix for the hostName of the SignalR service. Retained for future use.
        The hostname will be of format: &lt;hostNamePrefix&gt;.service.signalr.net.
        """
        return pulumi.get(self, "host_name_prefix")

    @host_name_prefix.setter
    def host_name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_name_prefix", value)


