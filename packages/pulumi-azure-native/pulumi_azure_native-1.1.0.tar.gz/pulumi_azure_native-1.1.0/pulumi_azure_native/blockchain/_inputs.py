# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'BlockchainMemberNodesSkuArgs',
    'FirewallRuleArgs',
    'SkuArgs',
]

@pulumi.input_type
class BlockchainMemberNodesSkuArgs:
    def __init__(__self__, *,
                 capacity: Optional[pulumi.Input[int]] = None):
        """
        Payload of the blockchain member nodes Sku for a blockchain member.
        :param pulumi.Input[int] capacity: Gets or sets the nodes capacity.
        """
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        Gets or sets the nodes capacity.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)


@pulumi.input_type
class FirewallRuleArgs:
    def __init__(__self__, *,
                 end_ip_address: Optional[pulumi.Input[str]] = None,
                 rule_name: Optional[pulumi.Input[str]] = None,
                 start_ip_address: Optional[pulumi.Input[str]] = None):
        """
        Ip range for firewall rules
        :param pulumi.Input[str] end_ip_address: Gets or sets the end IP address of the firewall rule range.
        :param pulumi.Input[str] rule_name: Gets or sets the name of the firewall rules.
        :param pulumi.Input[str] start_ip_address: Gets or sets the start IP address of the firewall rule range.
        """
        if end_ip_address is not None:
            pulumi.set(__self__, "end_ip_address", end_ip_address)
        if rule_name is not None:
            pulumi.set(__self__, "rule_name", rule_name)
        if start_ip_address is not None:
            pulumi.set(__self__, "start_ip_address", start_ip_address)

    @property
    @pulumi.getter(name="endIpAddress")
    def end_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the end IP address of the firewall rule range.
        """
        return pulumi.get(self, "end_ip_address")

    @end_ip_address.setter
    def end_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "end_ip_address", value)

    @property
    @pulumi.getter(name="ruleName")
    def rule_name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the name of the firewall rules.
        """
        return pulumi.get(self, "rule_name")

    @rule_name.setter
    def rule_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rule_name", value)

    @property
    @pulumi.getter(name="startIpAddress")
    def start_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets the start IP address of the firewall rule range.
        """
        return pulumi.get(self, "start_ip_address")

    @start_ip_address.setter
    def start_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "start_ip_address", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 tier: Optional[pulumi.Input[str]] = None):
        """
        Blockchain member Sku in payload
        :param pulumi.Input[str] name: Gets or sets Sku name
        :param pulumi.Input[str] tier: Gets or sets Sku tier
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets Sku name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> Optional[pulumi.Input[str]]:
        """
        Gets or sets Sku tier
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tier", value)


