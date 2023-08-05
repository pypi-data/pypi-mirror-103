# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AddressPrefixType',
    'ConnectivityTopology',
    'DeploymentType',
    'GroupConnectivity',
    'MemberType',
    'ScopeAccesses',
    'SecurityConfigurationRuleAccess',
    'SecurityConfigurationRuleDirection',
    'SecurityConfigurationRuleProtocol',
    'SecurityType',
]


class AddressPrefixType(str, Enum):
    """
    Address prefix type.
    """
    IP_PREFIX = "IPPrefix"
    SERVICE_TAG = "ServiceTag"


class ConnectivityTopology(str, Enum):
    """
    Connectivity topology type.
    """
    HUB_AND_SPOKE_TOPOLOGY = "HubAndSpokeTopology"
    MESH_TOPOLOGY = "MeshTopology"


class DeploymentType(str, Enum):
    """
    Configuration Deployment Type.
    """
    ADMIN_POLICY = "AdminPolicy"
    USER_POLICY = "UserPolicy"
    ROUTING = "Routing"
    CONNECTIVITY = "Connectivity"


class GroupConnectivity(str, Enum):
    """
    Group connectivity type.
    """
    NONE = "None"
    DIRECTLY_CONNECTED = "DirectlyConnected"


class MemberType(str, Enum):
    """
    Group member type.
    """
    VIRTUAL_NETWORK = "VirtualNetwork"
    SUBNET = "Subnet"


class ScopeAccesses(str, Enum):
    SECURITY = "Security"
    ROUTING = "Routing"
    CONNECTIVITY = "Connectivity"


class SecurityConfigurationRuleAccess(str, Enum):
    """
    Indicates the access allowed for this particular rule
    """
    ALLOW = "Allow"
    DENY = "Deny"
    ALWAYS_ALLOW = "AlwaysAllow"


class SecurityConfigurationRuleDirection(str, Enum):
    """
    Indicates if the traffic matched against the rule in inbound or outbound.
    """
    INBOUND = "Inbound"
    OUTBOUND = "Outbound"


class SecurityConfigurationRuleProtocol(str, Enum):
    """
    Network protocol this rule applies to.
    """
    TCP = "Tcp"
    UDP = "Udp"
    ICMP = "Icmp"
    ESP = "Esp"
    ANY = "Any"
    AH = "Ah"


class SecurityType(str, Enum):
    """
    Security Type.
    """
    ADMIN_POLICY = "AdminPolicy"
    USER_POLICY = "UserPolicy"
