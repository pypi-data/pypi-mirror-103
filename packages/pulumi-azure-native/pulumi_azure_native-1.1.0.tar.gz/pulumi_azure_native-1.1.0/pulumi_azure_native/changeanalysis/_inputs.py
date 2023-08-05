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
    'AzureMonitorWorkspacePropertiesArgs',
    'ConfigurationProfileResourcePropertiesArgs',
    'NotificationSettingsArgs',
    'ResourceIdentityArgs',
]

@pulumi.input_type
class AzureMonitorWorkspacePropertiesArgs:
    def __init__(__self__, *,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 workspace_resource_id: Optional[pulumi.Input[str]] = None):
        """
        Configuration properties of an Azure Monitor workspace that receives change notifications.
        :param pulumi.Input[str] workspace_id: The Azure Monitor workspace ID - the unique identifier for the Log Analytics workspace.
        :param pulumi.Input[str] workspace_resource_id: The Azure Monitor workspace ARM Resource ID. The resource ID should be in the following format: /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}
        """
        if workspace_id is not None:
            pulumi.set(__self__, "workspace_id", workspace_id)
        if workspace_resource_id is not None:
            pulumi.set(__self__, "workspace_resource_id", workspace_resource_id)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Monitor workspace ID - the unique identifier for the Log Analytics workspace.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_id", value)

    @property
    @pulumi.getter(name="workspaceResourceId")
    def workspace_resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Azure Monitor workspace ARM Resource ID. The resource ID should be in the following format: /subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}
        """
        return pulumi.get(self, "workspace_resource_id")

    @workspace_resource_id.setter
    def workspace_resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_resource_id", value)


@pulumi.input_type
class ConfigurationProfileResourcePropertiesArgs:
    def __init__(__self__, *,
                 notifications: Optional[pulumi.Input['NotificationSettingsArgs']] = None):
        """
        The properties of a configuration profile.
        :param pulumi.Input['NotificationSettingsArgs'] notifications: Settings of change notification configuration for a subscription.
        """
        if notifications is not None:
            pulumi.set(__self__, "notifications", notifications)

    @property
    @pulumi.getter
    def notifications(self) -> Optional[pulumi.Input['NotificationSettingsArgs']]:
        """
        Settings of change notification configuration for a subscription.
        """
        return pulumi.get(self, "notifications")

    @notifications.setter
    def notifications(self, value: Optional[pulumi.Input['NotificationSettingsArgs']]):
        pulumi.set(self, "notifications", value)


@pulumi.input_type
class NotificationSettingsArgs:
    def __init__(__self__, *,
                 activation_state: Optional[pulumi.Input[Union[str, 'NotificationsState']]] = None,
                 azure_monitor_workspace_properties: Optional[pulumi.Input['AzureMonitorWorkspacePropertiesArgs']] = None):
        """
        Settings of change notification configuration for a subscription.
        :param pulumi.Input[Union[str, 'NotificationsState']] activation_state: The state of notifications feature.
        :param pulumi.Input['AzureMonitorWorkspacePropertiesArgs'] azure_monitor_workspace_properties: Configuration properties of an Azure Monitor workspace that receives change notifications.
        """
        if activation_state is not None:
            pulumi.set(__self__, "activation_state", activation_state)
        if azure_monitor_workspace_properties is not None:
            pulumi.set(__self__, "azure_monitor_workspace_properties", azure_monitor_workspace_properties)

    @property
    @pulumi.getter(name="activationState")
    def activation_state(self) -> Optional[pulumi.Input[Union[str, 'NotificationsState']]]:
        """
        The state of notifications feature.
        """
        return pulumi.get(self, "activation_state")

    @activation_state.setter
    def activation_state(self, value: Optional[pulumi.Input[Union[str, 'NotificationsState']]]):
        pulumi.set(self, "activation_state", value)

    @property
    @pulumi.getter(name="azureMonitorWorkspaceProperties")
    def azure_monitor_workspace_properties(self) -> Optional[pulumi.Input['AzureMonitorWorkspacePropertiesArgs']]:
        """
        Configuration properties of an Azure Monitor workspace that receives change notifications.
        """
        return pulumi.get(self, "azure_monitor_workspace_properties")

    @azure_monitor_workspace_properties.setter
    def azure_monitor_workspace_properties(self, value: Optional[pulumi.Input['AzureMonitorWorkspacePropertiesArgs']]):
        pulumi.set(self, "azure_monitor_workspace_properties", value)


@pulumi.input_type
class ResourceIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input[Union[str, 'ManagedIdentityTypes']]] = None):
        """
        The identity block returned by ARM resource that supports managed identity.
        :param pulumi.Input[Union[str, 'ManagedIdentityTypes']] type: The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[Union[str, 'ManagedIdentityTypes']]]:
        """
        The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[Union[str, 'ManagedIdentityTypes']]]):
        pulumi.set(self, "type", value)


