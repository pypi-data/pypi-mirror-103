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

__all__ = [
    'AddressSpaceResponse',
    'CreatedByResponse',
    'EncryptionResponse',
    'ManagedIdentityConfigurationResponse',
    'SkuResponse',
    'VirtualNetworkPeeringPropertiesFormatResponseDatabricksVirtualNetwork',
    'VirtualNetworkPeeringPropertiesFormatResponseRemoteVirtualNetwork',
    'WorkspaceCustomBooleanParameterResponse',
    'WorkspaceCustomObjectParameterResponse',
    'WorkspaceCustomParametersResponse',
    'WorkspaceCustomStringParameterResponse',
    'WorkspaceEncryptionParameterResponse',
    'WorkspaceProviderAuthorizationResponse',
]

@pulumi.output_type
class AddressSpaceResponse(dict):
    """
    AddressSpace contains an array of IP address ranges that can be used by subnets of the virtual network.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "addressPrefixes":
            suggest = "address_prefixes"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AddressSpaceResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AddressSpaceResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AddressSpaceResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 address_prefixes: Optional[Sequence[str]] = None):
        """
        AddressSpace contains an array of IP address ranges that can be used by subnets of the virtual network.
        :param Sequence[str] address_prefixes: A list of address blocks reserved for this virtual network in CIDR notation.
        """
        if address_prefixes is not None:
            pulumi.set(__self__, "address_prefixes", address_prefixes)

    @property
    @pulumi.getter(name="addressPrefixes")
    def address_prefixes(self) -> Optional[Sequence[str]]:
        """
        A list of address blocks reserved for this virtual network in CIDR notation.
        """
        return pulumi.get(self, "address_prefixes")


@pulumi.output_type
class CreatedByResponse(dict):
    """
    Provides details of the entity that created/updated the workspace.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "applicationId":
            suggest = "application_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in CreatedByResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        CreatedByResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        CreatedByResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 application_id: str,
                 oid: str,
                 puid: str):
        """
        Provides details of the entity that created/updated the workspace.
        :param str application_id: The application ID of the application that initiated the creation of the workspace. For example, Azure Portal.
        :param str oid: The Object ID that created the workspace.
        :param str puid: The Personal Object ID corresponding to the object ID above
        """
        pulumi.set(__self__, "application_id", application_id)
        pulumi.set(__self__, "oid", oid)
        pulumi.set(__self__, "puid", puid)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> str:
        """
        The application ID of the application that initiated the creation of the workspace. For example, Azure Portal.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter
    def oid(self) -> str:
        """
        The Object ID that created the workspace.
        """
        return pulumi.get(self, "oid")

    @property
    @pulumi.getter
    def puid(self) -> str:
        """
        The Personal Object ID corresponding to the object ID above
        """
        return pulumi.get(self, "puid")


@pulumi.output_type
class EncryptionResponse(dict):
    """
    The object that contains details of encryption used on the workspace.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyName":
            suggest = "key_name"
        elif key == "keySource":
            suggest = "key_source"
        elif key == "keyVaultUri":
            suggest = "key_vault_uri"
        elif key == "keyVersion":
            suggest = "key_version"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in EncryptionResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        EncryptionResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        EncryptionResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_name: Optional[str] = None,
                 key_source: Optional[str] = None,
                 key_vault_uri: Optional[str] = None,
                 key_version: Optional[str] = None):
        """
        The object that contains details of encryption used on the workspace.
        :param str key_name: The name of KeyVault key.
        :param str key_source: The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault
        :param str key_vault_uri: The Uri of KeyVault.
        :param str key_version: The version of KeyVault key.
        """
        if key_name is not None:
            pulumi.set(__self__, "key_name", key_name)
        if key_source is None:
            key_source = 'Default'
        if key_source is not None:
            pulumi.set(__self__, "key_source", key_source)
        if key_vault_uri is not None:
            pulumi.set(__self__, "key_vault_uri", key_vault_uri)
        if key_version is not None:
            pulumi.set(__self__, "key_version", key_version)

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> Optional[str]:
        """
        The name of KeyVault key.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="keySource")
    def key_source(self) -> Optional[str]:
        """
        The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault
        """
        return pulumi.get(self, "key_source")

    @property
    @pulumi.getter(name="keyVaultUri")
    def key_vault_uri(self) -> Optional[str]:
        """
        The Uri of KeyVault.
        """
        return pulumi.get(self, "key_vault_uri")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[str]:
        """
        The version of KeyVault key.
        """
        return pulumi.get(self, "key_version")


@pulumi.output_type
class ManagedIdentityConfigurationResponse(dict):
    """
    The Managed Identity details for storage account.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedIdentityConfigurationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedIdentityConfigurationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedIdentityConfigurationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: str):
        """
        The Managed Identity details for storage account.
        :param str principal_id: The objectId of the Managed Identity that is linked to the Managed Storage account.
        :param str tenant_id: The tenant Id where the Managed Identity is created.
        :param str type: The type of Identity created. It can be either SystemAssigned or UserAssigned.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The objectId of the Managed Identity that is linked to the Managed Storage account.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant Id where the Managed Identity is created.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of Identity created. It can be either SystemAssigned or UserAssigned.
        """
        return pulumi.get(self, "type")


@pulumi.output_type
class SkuResponse(dict):
    """
    SKU for the resource.
    """
    def __init__(__self__, *,
                 name: str,
                 tier: Optional[str] = None):
        """
        SKU for the resource.
        :param str name: The SKU name.
        :param str tier: The SKU tier.
        """
        pulumi.set(__self__, "name", name)
        if tier is not None:
            pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The SKU name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tier(self) -> Optional[str]:
        """
        The SKU tier.
        """
        return pulumi.get(self, "tier")


@pulumi.output_type
class VirtualNetworkPeeringPropertiesFormatResponseDatabricksVirtualNetwork(dict):
    """
     The remote virtual network should be in the same region. See here to learn more (https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering).
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
         The remote virtual network should be in the same region. See here to learn more (https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering).
        :param str id: The Id of the databricks virtual network.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The Id of the databricks virtual network.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class VirtualNetworkPeeringPropertiesFormatResponseRemoteVirtualNetwork(dict):
    """
     The remote virtual network should be in the same region. See here to learn more (https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering).
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
         The remote virtual network should be in the same region. See here to learn more (https://docs.microsoft.com/en-us/azure/databricks/administration-guide/cloud-configurations/azure/vnet-peering).
        :param str id: The Id of the remote virtual network.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The Id of the remote virtual network.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class WorkspaceCustomBooleanParameterResponse(dict):
    """
    The value which should be used for this field.
    """
    def __init__(__self__, *,
                 type: str,
                 value: bool):
        """
        The value which should be used for this field.
        :param str type: The type of variable that this is
        :param bool value: The value which should be used for this field.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of variable that this is
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> bool:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class WorkspaceCustomObjectParameterResponse(dict):
    """
    The value which should be used for this field.
    """
    def __init__(__self__, *,
                 type: str,
                 value: Any):
        """
        The value which should be used for this field.
        :param str type: The type of variable that this is
        :param Any value: The value which should be used for this field.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of variable that this is
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> Any:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class WorkspaceCustomParametersResponse(dict):
    """
    Custom Parameters used for Cluster Creation.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "resourceTags":
            suggest = "resource_tags"
        elif key == "amlWorkspaceId":
            suggest = "aml_workspace_id"
        elif key == "customPrivateSubnetName":
            suggest = "custom_private_subnet_name"
        elif key == "customPublicSubnetName":
            suggest = "custom_public_subnet_name"
        elif key == "customVirtualNetworkId":
            suggest = "custom_virtual_network_id"
        elif key == "enableNoPublicIp":
            suggest = "enable_no_public_ip"
        elif key == "loadBalancerBackendPoolName":
            suggest = "load_balancer_backend_pool_name"
        elif key == "loadBalancerId":
            suggest = "load_balancer_id"
        elif key == "natGatewayName":
            suggest = "nat_gateway_name"
        elif key == "prepareEncryption":
            suggest = "prepare_encryption"
        elif key == "publicIpName":
            suggest = "public_ip_name"
        elif key == "requireInfrastructureEncryption":
            suggest = "require_infrastructure_encryption"
        elif key == "storageAccountName":
            suggest = "storage_account_name"
        elif key == "storageAccountSkuName":
            suggest = "storage_account_sku_name"
        elif key == "vnetAddressPrefix":
            suggest = "vnet_address_prefix"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceCustomParametersResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceCustomParametersResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceCustomParametersResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 resource_tags: 'outputs.WorkspaceCustomObjectParameterResponse',
                 aml_workspace_id: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 custom_private_subnet_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 custom_public_subnet_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 custom_virtual_network_id: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 enable_no_public_ip: Optional['outputs.WorkspaceCustomBooleanParameterResponse'] = None,
                 encryption: Optional['outputs.WorkspaceEncryptionParameterResponse'] = None,
                 load_balancer_backend_pool_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 load_balancer_id: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 nat_gateway_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 prepare_encryption: Optional['outputs.WorkspaceCustomBooleanParameterResponse'] = None,
                 public_ip_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 require_infrastructure_encryption: Optional['outputs.WorkspaceCustomBooleanParameterResponse'] = None,
                 storage_account_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 storage_account_sku_name: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None,
                 vnet_address_prefix: Optional['outputs.WorkspaceCustomStringParameterResponse'] = None):
        """
        Custom Parameters used for Cluster Creation.
        :param 'WorkspaceCustomObjectParameterResponse' resource_tags: Tags applied to resources under Managed resource group. These can be updated by updating tags at workspace level.
        :param 'WorkspaceCustomStringParameterResponse' aml_workspace_id: The ID of a Azure Machine Learning workspace to link with Databricks workspace
        :param 'WorkspaceCustomStringParameterResponse' custom_private_subnet_name: The name of the Private Subnet within the Virtual Network
        :param 'WorkspaceCustomStringParameterResponse' custom_public_subnet_name: The name of a Public Subnet within the Virtual Network
        :param 'WorkspaceCustomStringParameterResponse' custom_virtual_network_id: The ID of a Virtual Network where this Databricks Cluster should be created
        :param 'WorkspaceCustomBooleanParameterResponse' enable_no_public_ip: Should the Public IP be Disabled?
        :param 'WorkspaceEncryptionParameterResponse' encryption: Contains the encryption details for Customer-Managed Key (CMK) enabled workspace.
        :param 'WorkspaceCustomStringParameterResponse' load_balancer_backend_pool_name: Name of the outbound Load Balancer Backend Pool for Secure Cluster Connectivity (No Public IP).
        :param 'WorkspaceCustomStringParameterResponse' load_balancer_id: Resource URI of Outbound Load balancer for Secure Cluster Connectivity (No Public IP) workspace.
        :param 'WorkspaceCustomStringParameterResponse' nat_gateway_name: Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets.
        :param 'WorkspaceCustomBooleanParameterResponse' prepare_encryption: Prepare the workspace for encryption. Enables the Managed Identity for managed storage account.
        :param 'WorkspaceCustomStringParameterResponse' public_ip_name: Name of the Public IP for No Public IP workspace with managed vNet.
        :param 'WorkspaceCustomBooleanParameterResponse' require_infrastructure_encryption: A boolean indicating whether or not the DBFS root file system will be enabled with secondary layer of encryption with platform managed keys for data at rest.
        :param 'WorkspaceCustomStringParameterResponse' storage_account_name: Default DBFS storage account name.
        :param 'WorkspaceCustomStringParameterResponse' storage_account_sku_name: Storage account SKU name, ex: Standard_GRS, Standard_LRS. Refer https://aka.ms/storageskus for valid inputs.
        :param 'WorkspaceCustomStringParameterResponse' vnet_address_prefix: Address prefix for Managed virtual network. Default value for this input is 10.139.
        """
        pulumi.set(__self__, "resource_tags", resource_tags)
        if aml_workspace_id is not None:
            pulumi.set(__self__, "aml_workspace_id", aml_workspace_id)
        if custom_private_subnet_name is not None:
            pulumi.set(__self__, "custom_private_subnet_name", custom_private_subnet_name)
        if custom_public_subnet_name is not None:
            pulumi.set(__self__, "custom_public_subnet_name", custom_public_subnet_name)
        if custom_virtual_network_id is not None:
            pulumi.set(__self__, "custom_virtual_network_id", custom_virtual_network_id)
        if enable_no_public_ip is not None:
            pulumi.set(__self__, "enable_no_public_ip", enable_no_public_ip)
        if encryption is not None:
            pulumi.set(__self__, "encryption", encryption)
        if load_balancer_backend_pool_name is not None:
            pulumi.set(__self__, "load_balancer_backend_pool_name", load_balancer_backend_pool_name)
        if load_balancer_id is not None:
            pulumi.set(__self__, "load_balancer_id", load_balancer_id)
        if nat_gateway_name is not None:
            pulumi.set(__self__, "nat_gateway_name", nat_gateway_name)
        if prepare_encryption is not None:
            pulumi.set(__self__, "prepare_encryption", prepare_encryption)
        if public_ip_name is not None:
            pulumi.set(__self__, "public_ip_name", public_ip_name)
        if require_infrastructure_encryption is not None:
            pulumi.set(__self__, "require_infrastructure_encryption", require_infrastructure_encryption)
        if storage_account_name is not None:
            pulumi.set(__self__, "storage_account_name", storage_account_name)
        if storage_account_sku_name is not None:
            pulumi.set(__self__, "storage_account_sku_name", storage_account_sku_name)
        if vnet_address_prefix is not None:
            pulumi.set(__self__, "vnet_address_prefix", vnet_address_prefix)

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> 'outputs.WorkspaceCustomObjectParameterResponse':
        """
        Tags applied to resources under Managed resource group. These can be updated by updating tags at workspace level.
        """
        return pulumi.get(self, "resource_tags")

    @property
    @pulumi.getter(name="amlWorkspaceId")
    def aml_workspace_id(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        The ID of a Azure Machine Learning workspace to link with Databricks workspace
        """
        return pulumi.get(self, "aml_workspace_id")

    @property
    @pulumi.getter(name="customPrivateSubnetName")
    def custom_private_subnet_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        The name of the Private Subnet within the Virtual Network
        """
        return pulumi.get(self, "custom_private_subnet_name")

    @property
    @pulumi.getter(name="customPublicSubnetName")
    def custom_public_subnet_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        The name of a Public Subnet within the Virtual Network
        """
        return pulumi.get(self, "custom_public_subnet_name")

    @property
    @pulumi.getter(name="customVirtualNetworkId")
    def custom_virtual_network_id(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        The ID of a Virtual Network where this Databricks Cluster should be created
        """
        return pulumi.get(self, "custom_virtual_network_id")

    @property
    @pulumi.getter(name="enableNoPublicIp")
    def enable_no_public_ip(self) -> Optional['outputs.WorkspaceCustomBooleanParameterResponse']:
        """
        Should the Public IP be Disabled?
        """
        return pulumi.get(self, "enable_no_public_ip")

    @property
    @pulumi.getter
    def encryption(self) -> Optional['outputs.WorkspaceEncryptionParameterResponse']:
        """
        Contains the encryption details for Customer-Managed Key (CMK) enabled workspace.
        """
        return pulumi.get(self, "encryption")

    @property
    @pulumi.getter(name="loadBalancerBackendPoolName")
    def load_balancer_backend_pool_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Name of the outbound Load Balancer Backend Pool for Secure Cluster Connectivity (No Public IP).
        """
        return pulumi.get(self, "load_balancer_backend_pool_name")

    @property
    @pulumi.getter(name="loadBalancerId")
    def load_balancer_id(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Resource URI of Outbound Load balancer for Secure Cluster Connectivity (No Public IP) workspace.
        """
        return pulumi.get(self, "load_balancer_id")

    @property
    @pulumi.getter(name="natGatewayName")
    def nat_gateway_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Name of the NAT gateway for Secure Cluster Connectivity (No Public IP) workspace subnets.
        """
        return pulumi.get(self, "nat_gateway_name")

    @property
    @pulumi.getter(name="prepareEncryption")
    def prepare_encryption(self) -> Optional['outputs.WorkspaceCustomBooleanParameterResponse']:
        """
        Prepare the workspace for encryption. Enables the Managed Identity for managed storage account.
        """
        return pulumi.get(self, "prepare_encryption")

    @property
    @pulumi.getter(name="publicIpName")
    def public_ip_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Name of the Public IP for No Public IP workspace with managed vNet.
        """
        return pulumi.get(self, "public_ip_name")

    @property
    @pulumi.getter(name="requireInfrastructureEncryption")
    def require_infrastructure_encryption(self) -> Optional['outputs.WorkspaceCustomBooleanParameterResponse']:
        """
        A boolean indicating whether or not the DBFS root file system will be enabled with secondary layer of encryption with platform managed keys for data at rest.
        """
        return pulumi.get(self, "require_infrastructure_encryption")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Default DBFS storage account name.
        """
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="storageAccountSkuName")
    def storage_account_sku_name(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Storage account SKU name, ex: Standard_GRS, Standard_LRS. Refer https://aka.ms/storageskus for valid inputs.
        """
        return pulumi.get(self, "storage_account_sku_name")

    @property
    @pulumi.getter(name="vnetAddressPrefix")
    def vnet_address_prefix(self) -> Optional['outputs.WorkspaceCustomStringParameterResponse']:
        """
        Address prefix for Managed virtual network. Default value for this input is 10.139.
        """
        return pulumi.get(self, "vnet_address_prefix")


@pulumi.output_type
class WorkspaceCustomStringParameterResponse(dict):
    """
    The Value.
    """
    def __init__(__self__, *,
                 type: str,
                 value: str):
        """
        The Value.
        :param str type: The type of variable that this is
        :param str value: The value which should be used for this field.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of variable that this is
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class WorkspaceEncryptionParameterResponse(dict):
    """
    The object that contains details of encryption used on the workspace.
    """
    def __init__(__self__, *,
                 type: str,
                 value: Optional['outputs.EncryptionResponse'] = None):
        """
        The object that contains details of encryption used on the workspace.
        :param str type: The type of variable that this is
        :param 'EncryptionResponse' value: The value which should be used for this field.
        """
        pulumi.set(__self__, "type", type)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of variable that this is
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> Optional['outputs.EncryptionResponse']:
        """
        The value which should be used for this field.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class WorkspaceProviderAuthorizationResponse(dict):
    """
    The workspace provider authorization.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "roleDefinitionId":
            suggest = "role_definition_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceProviderAuthorizationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceProviderAuthorizationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceProviderAuthorizationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 role_definition_id: str):
        """
        The workspace provider authorization.
        :param str principal_id: The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources.
        :param str role_definition_id: The provider's role definition identifier. This role will define all the permissions that the provider must have on the workspace's container resource group. This role definition cannot have permission to delete the resource group.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "role_definition_id", role_definition_id)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The provider's principal identifier. This is the identity that the provider will use to call ARM to manage the workspace resources.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="roleDefinitionId")
    def role_definition_id(self) -> str:
        """
        The provider's role definition identifier. This role will define all the permissions that the provider must have on the workspace's container resource group. This role definition cannot have permission to delete the resource group.
        """
        return pulumi.get(self, "role_definition_id")


