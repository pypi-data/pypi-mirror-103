# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ACLAction',
    'FeatureFlags',
    'PrivateLinkServiceConnectionStatus',
    'ServiceKind',
    'SignalRRequestType',
    'SignalRSkuTier',
]


class ACLAction(str, Enum):
    """
    Default action when no other rule matches
    """
    ALLOW = "Allow"
    DENY = "Deny"


class FeatureFlags(str, Enum):
    """
    FeatureFlags is the supported features of Azure SignalR service.
    - ServiceMode: Flag for backend server for SignalR service. Values allowed: "Default": have your own backend server; "Serverless": your application doesn't have a backend server; "Classic": for backward compatibility. Support both Default and Serverless mode but not recommended; "PredefinedOnly": for future use.
    - EnableConnectivityLogs: "true"/"false", to enable/disable the connectivity log category respectively.
    """
    SERVICE_MODE = "ServiceMode"
    ENABLE_CONNECTIVITY_LOGS = "EnableConnectivityLogs"
    ENABLE_MESSAGING_LOGS = "EnableMessagingLogs"


class PrivateLinkServiceConnectionStatus(str, Enum):
    """
    Indicates whether the connection has been Approved/Rejected/Removed by the owner of the service.
    """
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"


class ServiceKind(str, Enum):
    """
    The kind of the service - e.g. "SignalR", or "RawWebSockets" for "Microsoft.SignalRService/SignalR"
    """
    SIGNAL_R = "SignalR"
    RAW_WEB_SOCKETS = "RawWebSockets"


class SignalRRequestType(str, Enum):
    """
    Allowed request types. The value can be one or more of: ClientConnection, ServerConnection, RESTAPI.
    """
    CLIENT_CONNECTION = "ClientConnection"
    SERVER_CONNECTION = "ServerConnection"
    RESTAPI = "RESTAPI"


class SignalRSkuTier(str, Enum):
    """
    Optional tier of this particular SKU. 'Standard' or 'Free'. 
    
    `Basic` is deprecated, use `Standard` instead.
    """
    FREE = "Free"
    BASIC = "Basic"
    STANDARD = "Standard"
    PREMIUM = "Premium"
