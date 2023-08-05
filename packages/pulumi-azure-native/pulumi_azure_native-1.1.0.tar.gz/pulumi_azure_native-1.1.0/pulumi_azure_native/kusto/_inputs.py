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
    'AzureSkuArgs',
    'IdentityArgs',
    'KeyVaultPropertiesArgs',
    'OptimizedAutoscaleArgs',
    'TableLevelSharingPropertiesArgs',
    'TrustedExternalTenantArgs',
    'VirtualNetworkConfigurationArgs',
]

@pulumi.input_type
class AzureSkuArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[Union[str, 'AzureSkuName']],
                 tier: pulumi.Input[Union[str, 'AzureSkuTier']],
                 capacity: Optional[pulumi.Input[int]] = None):
        """
        Azure SKU definition.
        :param pulumi.Input[Union[str, 'AzureSkuName']] name: SKU name.
        :param pulumi.Input[Union[str, 'AzureSkuTier']] tier: SKU tier.
        :param pulumi.Input[int] capacity: The number of instances of the cluster.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "tier", tier)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[Union[str, 'AzureSkuName']]:
        """
        SKU name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[Union[str, 'AzureSkuName']]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Input[Union[str, 'AzureSkuTier']]:
        """
        SKU tier.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: pulumi.Input[Union[str, 'AzureSkuTier']]):
        pulumi.set(self, "tier", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The number of instances of the cluster.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[Union[str, 'IdentityType']],
                 user_assigned_identities: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Identity for the resource.
        :param pulumi.Input[Union[str, 'IdentityType']] type: The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove all identities.
        :param pulumi.Input[Mapping[str, Any]] user_assigned_identities: The list of user identities associated with the Kusto cluster. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        pulumi.set(__self__, "type", type)
        if user_assigned_identities is not None:
            pulumi.set(__self__, "user_assigned_identities", user_assigned_identities)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[Union[str, 'IdentityType']]:
        """
        The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove all identities.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[Union[str, 'IdentityType']]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userAssignedIdentities")
    def user_assigned_identities(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        The list of user identities associated with the Kusto cluster. The user identity dictionary key references will be ARM resource ids in the form: '/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identityName}'.
        """
        return pulumi.get(self, "user_assigned_identities")

    @user_assigned_identities.setter
    def user_assigned_identities(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "user_assigned_identities", value)


@pulumi.input_type
class KeyVaultPropertiesArgs:
    def __init__(__self__, *,
                 key_name: pulumi.Input[str],
                 key_vault_uri: pulumi.Input[str],
                 key_version: Optional[pulumi.Input[str]] = None,
                 user_identity: Optional[pulumi.Input[str]] = None):
        """
        Properties of the key vault.
        :param pulumi.Input[str] key_name: The name of the key vault key.
        :param pulumi.Input[str] key_vault_uri: The Uri of the key vault.
        :param pulumi.Input[str] key_version: The version of the key vault key.
        :param pulumi.Input[str] user_identity: The user assigned identity (ARM resource id) that has access to the key.
        """
        pulumi.set(__self__, "key_name", key_name)
        pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)
        if user_identity is not None:
            pulumi.set(__self__, "user_identity", user_identity)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> pulumi.Input[str]:
        """
        The name of the key vault key.
        """
        return pulumi.get(self, "key_name")

    @key_name.setter
    def key_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_name", value)

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> pulumi.Input[str]:
        """
        The Uri of the key vault.
        """
        return pulumi.get(self, "key_vault_uri")

    @key_vault_uri.setter
    def key_vault_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "key_vault_uri", value)

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the key vault key.
        """
        return pulumi.get(self, "key_version")

    @key_version.setter
    def key_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_version", value)

    @property
    @pulumi.getter(name="userIdentity")
    def user_identity(self) -> Optional[pulumi.Input[str]]:
        """
        The user assigned identity (ARM resource id) that has access to the key.
        """
        return pulumi.get(self, "user_identity")

    @user_identity.setter
    def user_identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_identity", value)


@pulumi.input_type
class OptimizedAutoscaleArgs:
    def __init__(__self__, *,
                 is_enabled: pulumi.Input[bool],
                 maximum: pulumi.Input[int],
                 minimum: pulumi.Input[int],
                 version: pulumi.Input[int]):
        """
        A class that contains the optimized auto scale definition.
        :param pulumi.Input[bool] is_enabled: A boolean value that indicate if the optimized autoscale feature is enabled or not.
        :param pulumi.Input[int] maximum: Maximum allowed instances count.
        :param pulumi.Input[int] minimum: Minimum allowed instances count.
        :param pulumi.Input[int] version: The version of the template defined, for instance 1.
        """
        pulumi.set(__self__, "is_enabled", is_enabled)
        pulumi.set(__self__, "maximum", maximum)
        pulumi.set(__self__, "minimum", minimum)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Input[bool]:
        """
        A boolean value that indicate if the optimized autoscale feature is enabled or not.
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "is_enabled", value)

    @property
    @pulumi.getter
    def maximum(self) -> pulumi.Input[int]:
        """
        Maximum allowed instances count.
        """
        return pulumi.get(self, "maximum")

    @maximum.setter
    def maximum(self, value: pulumi.Input[int]):
        pulumi.set(self, "maximum", value)

    @property
    @pulumi.getter
    def minimum(self) -> pulumi.Input[int]:
        """
        Minimum allowed instances count.
        """
        return pulumi.get(self, "minimum")

    @minimum.setter
    def minimum(self, value: pulumi.Input[int]):
        pulumi.set(self, "minimum", value)

    @property
    @pulumi.getter
    def version(self) -> pulumi.Input[int]:
        """
        The version of the template defined, for instance 1.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: pulumi.Input[int]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class TableLevelSharingPropertiesArgs:
    def __init__(__self__, *,
                 external_tables_to_exclude: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 external_tables_to_include: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 materialized_views_to_exclude: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 materialized_views_to_include: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tables_to_exclude: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tables_to_include: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Tables that will be included and excluded in the follower database
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_tables_to_exclude: List of external tables exclude from the follower database
        :param pulumi.Input[Sequence[pulumi.Input[str]]] external_tables_to_include: List of external tables to include in the follower database
        :param pulumi.Input[Sequence[pulumi.Input[str]]] materialized_views_to_exclude: List of materialized views exclude from the follower database
        :param pulumi.Input[Sequence[pulumi.Input[str]]] materialized_views_to_include: List of materialized views to include in the follower database
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tables_to_exclude: List of tables to exclude from the follower database
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tables_to_include: List of tables to include in the follower database
        """
        if external_tables_to_exclude is not None:
            pulumi.set(__self__, "external_tables_to_exclude", external_tables_to_exclude)
        if external_tables_to_include is not None:
            pulumi.set(__self__, "external_tables_to_include", external_tables_to_include)
        if materialized_views_to_exclude is not None:
            pulumi.set(__self__, "materialized_views_to_exclude", materialized_views_to_exclude)
        if materialized_views_to_include is not None:
            pulumi.set(__self__, "materialized_views_to_include", materialized_views_to_include)
        if tables_to_exclude is not None:
            pulumi.set(__self__, "tables_to_exclude", tables_to_exclude)
        if tables_to_include is not None:
            pulumi.set(__self__, "tables_to_include", tables_to_include)

    @property
    @pulumi.getter(name="externalTablesToExclude")
    def external_tables_to_exclude(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of external tables exclude from the follower database
        """
        return pulumi.get(self, "external_tables_to_exclude")

    @external_tables_to_exclude.setter
    def external_tables_to_exclude(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "external_tables_to_exclude", value)

    @property
    @pulumi.getter(name="externalTablesToInclude")
    def external_tables_to_include(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of external tables to include in the follower database
        """
        return pulumi.get(self, "external_tables_to_include")

    @external_tables_to_include.setter
    def external_tables_to_include(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "external_tables_to_include", value)

    @property
    @pulumi.getter(name="materializedViewsToExclude")
    def materialized_views_to_exclude(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of materialized views exclude from the follower database
        """
        return pulumi.get(self, "materialized_views_to_exclude")

    @materialized_views_to_exclude.setter
    def materialized_views_to_exclude(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "materialized_views_to_exclude", value)

    @property
    @pulumi.getter(name="materializedViewsToInclude")
    def materialized_views_to_include(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of materialized views to include in the follower database
        """
        return pulumi.get(self, "materialized_views_to_include")

    @materialized_views_to_include.setter
    def materialized_views_to_include(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "materialized_views_to_include", value)

    @property
    @pulumi.getter(name="tablesToExclude")
    def tables_to_exclude(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of tables to exclude from the follower database
        """
        return pulumi.get(self, "tables_to_exclude")

    @tables_to_exclude.setter
    def tables_to_exclude(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tables_to_exclude", value)

    @property
    @pulumi.getter(name="tablesToInclude")
    def tables_to_include(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of tables to include in the follower database
        """
        return pulumi.get(self, "tables_to_include")

    @tables_to_include.setter
    def tables_to_include(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tables_to_include", value)


@pulumi.input_type
class TrustedExternalTenantArgs:
    def __init__(__self__, *,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Represents a tenant ID that is trusted by the cluster.
        :param pulumi.Input[str] value: GUID representing an external tenant.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        GUID representing an external tenant.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class VirtualNetworkConfigurationArgs:
    def __init__(__self__, *,
                 data_management_public_ip_id: pulumi.Input[str],
                 engine_public_ip_id: pulumi.Input[str],
                 subnet_id: pulumi.Input[str]):
        """
        A class that contains virtual network definition.
        :param pulumi.Input[str] data_management_public_ip_id: Data management's service public IP address resource id.
        :param pulumi.Input[str] engine_public_ip_id: Engine service's public IP address resource id.
        :param pulumi.Input[str] subnet_id: The subnet resource id.
        """
        pulumi.set(__self__, "data_management_public_ip_id", data_management_public_ip_id)
        pulumi.set(__self__, "engine_public_ip_id", engine_public_ip_id)
        pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter(name="dataManagementPublicIpId")
    def data_management_public_ip_id(self) -> pulumi.Input[str]:
        """
        Data management's service public IP address resource id.
        """
        return pulumi.get(self, "data_management_public_ip_id")

    @data_management_public_ip_id.setter
    def data_management_public_ip_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "data_management_public_ip_id", value)

    @property
    @pulumi.getter(name="enginePublicIpId")
    def engine_public_ip_id(self) -> pulumi.Input[str]:
        """
        Engine service's public IP address resource id.
        """
        return pulumi.get(self, "engine_public_ip_id")

    @engine_public_ip_id.setter
    def engine_public_ip_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "engine_public_ip_id", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Input[str]:
        """
        The subnet resource id.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_id", value)


