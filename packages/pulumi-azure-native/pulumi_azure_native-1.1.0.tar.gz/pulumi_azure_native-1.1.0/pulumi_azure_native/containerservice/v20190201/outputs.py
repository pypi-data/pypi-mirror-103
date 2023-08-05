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

__all__ = [
    'ContainerServiceLinuxProfileResponse',
    'ContainerServiceNetworkProfileResponse',
    'ContainerServiceSshConfigurationResponse',
    'ContainerServiceSshPublicKeyResponse',
    'CredentialResultResponse',
    'ManagedClusterAADProfileResponse',
    'ManagedClusterAddonProfileResponse',
    'ManagedClusterAgentPoolProfileResponse',
    'ManagedClusterServicePrincipalProfileResponse',
]

@pulumi.output_type
class ContainerServiceLinuxProfileResponse(dict):
    """
    Profile for Linux VMs in the container service cluster.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "adminUsername":
            suggest = "admin_username"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceLinuxProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceLinuxProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerServiceLinuxProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 admin_username: str,
                 ssh: 'outputs.ContainerServiceSshConfigurationResponse'):
        """
        Profile for Linux VMs in the container service cluster.
        :param str admin_username: The administrator username to use for Linux VMs.
        :param 'ContainerServiceSshConfigurationResponse' ssh: SSH configuration for Linux-based VMs running on Azure.
        """
        pulumi.set(__self__, "admin_username", admin_username)
        pulumi.set(__self__, "ssh", ssh)

    @property
    @pulumi.getter(name="adminUsername")
    def admin_username(self) -> str:
        """
        The administrator username to use for Linux VMs.
        """
        return pulumi.get(self, "admin_username")

    @property
    @pulumi.getter
    def ssh(self) -> 'outputs.ContainerServiceSshConfigurationResponse':
        """
        SSH configuration for Linux-based VMs running on Azure.
        """
        return pulumi.get(self, "ssh")


@pulumi.output_type
class ContainerServiceNetworkProfileResponse(dict):
    """
    Profile of network configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dnsServiceIP":
            suggest = "dns_service_ip"
        elif key == "dockerBridgeCidr":
            suggest = "docker_bridge_cidr"
        elif key == "networkPlugin":
            suggest = "network_plugin"
        elif key == "networkPolicy":
            suggest = "network_policy"
        elif key == "podCidr":
            suggest = "pod_cidr"
        elif key == "serviceCidr":
            suggest = "service_cidr"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceNetworkProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceNetworkProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerServiceNetworkProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 dns_service_ip: Optional[str] = None,
                 docker_bridge_cidr: Optional[str] = None,
                 network_plugin: Optional[str] = None,
                 network_policy: Optional[str] = None,
                 pod_cidr: Optional[str] = None,
                 service_cidr: Optional[str] = None):
        """
        Profile of network configuration.
        :param str dns_service_ip: An IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in serviceCidr.
        :param str docker_bridge_cidr: A CIDR notation IP range assigned to the Docker bridge network. It must not overlap with any Subnet IP ranges or the Kubernetes service address range.
        :param str network_plugin: Network plugin used for building Kubernetes network.
        :param str network_policy: Network policy used for building Kubernetes network.
        :param str pod_cidr: A CIDR notation IP range from which to assign pod IPs when kubenet is used.
        :param str service_cidr: A CIDR notation IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges.
        """
        if dns_service_ip is None:
            dns_service_ip = '10.0.0.10'
        if dns_service_ip is not None:
            pulumi.set(__self__, "dns_service_ip", dns_service_ip)
        if docker_bridge_cidr is None:
            docker_bridge_cidr = '172.17.0.1/16'
        if docker_bridge_cidr is not None:
            pulumi.set(__self__, "docker_bridge_cidr", docker_bridge_cidr)
        if network_plugin is None:
            network_plugin = 'kubenet'
        if network_plugin is not None:
            pulumi.set(__self__, "network_plugin", network_plugin)
        if network_policy is not None:
            pulumi.set(__self__, "network_policy", network_policy)
        if pod_cidr is None:
            pod_cidr = '10.244.0.0/16'
        if pod_cidr is not None:
            pulumi.set(__self__, "pod_cidr", pod_cidr)
        if service_cidr is None:
            service_cidr = '10.0.0.0/16'
        if service_cidr is not None:
            pulumi.set(__self__, "service_cidr", service_cidr)

    @property
    @pulumi.getter(name="dnsServiceIP")
    def dns_service_ip(self) -> Optional[str]:
        """
        An IP address assigned to the Kubernetes DNS service. It must be within the Kubernetes service address range specified in serviceCidr.
        """
        return pulumi.get(self, "dns_service_ip")

    @property
    @pulumi.getter(name="dockerBridgeCidr")
    def docker_bridge_cidr(self) -> Optional[str]:
        """
        A CIDR notation IP range assigned to the Docker bridge network. It must not overlap with any Subnet IP ranges or the Kubernetes service address range.
        """
        return pulumi.get(self, "docker_bridge_cidr")

    @property
    @pulumi.getter(name="networkPlugin")
    def network_plugin(self) -> Optional[str]:
        """
        Network plugin used for building Kubernetes network.
        """
        return pulumi.get(self, "network_plugin")

    @property
    @pulumi.getter(name="networkPolicy")
    def network_policy(self) -> Optional[str]:
        """
        Network policy used for building Kubernetes network.
        """
        return pulumi.get(self, "network_policy")

    @property
    @pulumi.getter(name="podCidr")
    def pod_cidr(self) -> Optional[str]:
        """
        A CIDR notation IP range from which to assign pod IPs when kubenet is used.
        """
        return pulumi.get(self, "pod_cidr")

    @property
    @pulumi.getter(name="serviceCidr")
    def service_cidr(self) -> Optional[str]:
        """
        A CIDR notation IP range from which to assign service cluster IPs. It must not overlap with any Subnet IP ranges.
        """
        return pulumi.get(self, "service_cidr")


@pulumi.output_type
class ContainerServiceSshConfigurationResponse(dict):
    """
    SSH configuration for Linux-based VMs running on Azure.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "publicKeys":
            suggest = "public_keys"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceSshConfigurationResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceSshConfigurationResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerServiceSshConfigurationResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 public_keys: Sequence['outputs.ContainerServiceSshPublicKeyResponse']):
        """
        SSH configuration for Linux-based VMs running on Azure.
        :param Sequence['ContainerServiceSshPublicKeyResponse'] public_keys: The list of SSH public keys used to authenticate with Linux-based VMs. Only expect one key specified.
        """
        pulumi.set(__self__, "public_keys", public_keys)

    @property
    @pulumi.getter(name="publicKeys")
    def public_keys(self) -> Sequence['outputs.ContainerServiceSshPublicKeyResponse']:
        """
        The list of SSH public keys used to authenticate with Linux-based VMs. Only expect one key specified.
        """
        return pulumi.get(self, "public_keys")


@pulumi.output_type
class ContainerServiceSshPublicKeyResponse(dict):
    """
    Contains information about SSH certificate public key data.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "keyData":
            suggest = "key_data"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerServiceSshPublicKeyResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerServiceSshPublicKeyResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerServiceSshPublicKeyResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 key_data: str):
        """
        Contains information about SSH certificate public key data.
        :param str key_data: Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or without headers.
        """
        pulumi.set(__self__, "key_data", key_data)

    @property
    @pulumi.getter(name="keyData")
    def key_data(self) -> str:
        """
        Certificate public key used to authenticate with VMs through SSH. The certificate must be in PEM format with or without headers.
        """
        return pulumi.get(self, "key_data")


@pulumi.output_type
class CredentialResultResponse(dict):
    """
    The credential result response.
    """
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        The credential result response.
        :param str name: The name of the credential.
        :param str value: Base64-encoded Kubernetes configuration file.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the credential.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        Base64-encoded Kubernetes configuration file.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class ManagedClusterAADProfileResponse(dict):
    """
    AADProfile specifies attributes for Azure Active Directory integration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientAppID":
            suggest = "client_app_id"
        elif key == "serverAppID":
            suggest = "server_app_id"
        elif key == "serverAppSecret":
            suggest = "server_app_secret"
        elif key == "tenantID":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAADProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAADProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedClusterAADProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_app_id: str,
                 server_app_id: str,
                 server_app_secret: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        AADProfile specifies attributes for Azure Active Directory integration.
        :param str client_app_id: The client AAD application ID.
        :param str server_app_id: The server AAD application ID.
        :param str server_app_secret: The server AAD application secret.
        :param str tenant_id: The AAD tenant ID to use for authentication. If not specified, will use the tenant of the deployment subscription.
        """
        pulumi.set(__self__, "client_app_id", client_app_id)
        pulumi.set(__self__, "server_app_id", server_app_id)
        if server_app_secret is not None:
            pulumi.set(__self__, "server_app_secret", server_app_secret)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="clientAppID")
    def client_app_id(self) -> str:
        """
        The client AAD application ID.
        """
        return pulumi.get(self, "client_app_id")

    @property
    @pulumi.getter(name="serverAppID")
    def server_app_id(self) -> str:
        """
        The server AAD application ID.
        """
        return pulumi.get(self, "server_app_id")

    @property
    @pulumi.getter(name="serverAppSecret")
    def server_app_secret(self) -> Optional[str]:
        """
        The server AAD application secret.
        """
        return pulumi.get(self, "server_app_secret")

    @property
    @pulumi.getter(name="tenantID")
    def tenant_id(self) -> Optional[str]:
        """
        The AAD tenant ID to use for authentication. If not specified, will use the tenant of the deployment subscription.
        """
        return pulumi.get(self, "tenant_id")


@pulumi.output_type
class ManagedClusterAddonProfileResponse(dict):
    """
    A Kubernetes add-on profile for a managed cluster.
    """
    def __init__(__self__, *,
                 enabled: bool,
                 config: Optional[Mapping[str, str]] = None):
        """
        A Kubernetes add-on profile for a managed cluster.
        :param bool enabled: Whether the add-on is enabled or not.
        :param Mapping[str, str] config: Key-value pairs for configuring an add-on.
        """
        pulumi.set(__self__, "enabled", enabled)
        if config is not None:
            pulumi.set(__self__, "config", config)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Whether the add-on is enabled or not.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def config(self) -> Optional[Mapping[str, str]]:
        """
        Key-value pairs for configuring an add-on.
        """
        return pulumi.get(self, "config")


@pulumi.output_type
class ManagedClusterAgentPoolProfileResponse(dict):
    """
    Profile for the container service agent pool.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "vmSize":
            suggest = "vm_size"
        elif key == "availabilityZones":
            suggest = "availability_zones"
        elif key == "enableAutoScaling":
            suggest = "enable_auto_scaling"
        elif key == "maxCount":
            suggest = "max_count"
        elif key == "maxPods":
            suggest = "max_pods"
        elif key == "minCount":
            suggest = "min_count"
        elif key == "orchestratorVersion":
            suggest = "orchestrator_version"
        elif key == "osDiskSizeGB":
            suggest = "os_disk_size_gb"
        elif key == "osType":
            suggest = "os_type"
        elif key == "vnetSubnetID":
            suggest = "vnet_subnet_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterAgentPoolProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterAgentPoolProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedClusterAgentPoolProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 count: int,
                 name: str,
                 provisioning_state: str,
                 vm_size: str,
                 availability_zones: Optional[Sequence[str]] = None,
                 enable_auto_scaling: Optional[bool] = None,
                 max_count: Optional[int] = None,
                 max_pods: Optional[int] = None,
                 min_count: Optional[int] = None,
                 orchestrator_version: Optional[str] = None,
                 os_disk_size_gb: Optional[int] = None,
                 os_type: Optional[str] = None,
                 type: Optional[str] = None,
                 vnet_subnet_id: Optional[str] = None):
        """
        Profile for the container service agent pool.
        :param int count: Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        :param str name: Unique name of the agent pool profile in the context of the subscription and resource group.
        :param str provisioning_state: The current deployment or provisioning state, which only appears in the response.
        :param str vm_size: Size of agent VMs.
        :param Sequence[str] availability_zones: (PREVIEW) Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        :param bool enable_auto_scaling: Whether to enable auto-scaler
        :param int max_count: Maximum number of nodes for auto-scaling
        :param int max_pods: Maximum number of pods that can run on a node.
        :param int min_count: Minimum number of nodes for auto-scaling
        :param str orchestrator_version: Version of orchestrator specified when creating the managed cluster.
        :param int os_disk_size_gb: OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        :param str os_type: OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        :param str type: AgentPoolType represents types of an agent pool
        :param str vnet_subnet_id: VNet SubnetID specifies the VNet's subnet identifier.
        """
        if count is None:
            count = 1
        pulumi.set(__self__, "count", count)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "vm_size", vm_size)
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if enable_auto_scaling is not None:
            pulumi.set(__self__, "enable_auto_scaling", enable_auto_scaling)
        if max_count is not None:
            pulumi.set(__self__, "max_count", max_count)
        if max_pods is not None:
            pulumi.set(__self__, "max_pods", max_pods)
        if min_count is not None:
            pulumi.set(__self__, "min_count", min_count)
        if orchestrator_version is not None:
            pulumi.set(__self__, "orchestrator_version", orchestrator_version)
        if os_disk_size_gb is not None:
            pulumi.set(__self__, "os_disk_size_gb", os_disk_size_gb)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if vnet_subnet_id is not None:
            pulumi.set(__self__, "vnet_subnet_id", vnet_subnet_id)

    @property
    @pulumi.getter
    def count(self) -> int:
        """
        Number of agents (VMs) to host docker containers. Allowed values must be in the range of 1 to 100 (inclusive). The default value is 1. 
        """
        return pulumi.get(self, "count")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Unique name of the agent pool profile in the context of the subscription and resource group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> str:
        """
        Size of agent VMs.
        """
        return pulumi.get(self, "vm_size")

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[Sequence[str]]:
        """
        (PREVIEW) Availability zones for nodes. Must use VirtualMachineScaleSets AgentPoolType.
        """
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter(name="enableAutoScaling")
    def enable_auto_scaling(self) -> Optional[bool]:
        """
        Whether to enable auto-scaler
        """
        return pulumi.get(self, "enable_auto_scaling")

    @property
    @pulumi.getter(name="maxCount")
    def max_count(self) -> Optional[int]:
        """
        Maximum number of nodes for auto-scaling
        """
        return pulumi.get(self, "max_count")

    @property
    @pulumi.getter(name="maxPods")
    def max_pods(self) -> Optional[int]:
        """
        Maximum number of pods that can run on a node.
        """
        return pulumi.get(self, "max_pods")

    @property
    @pulumi.getter(name="minCount")
    def min_count(self) -> Optional[int]:
        """
        Minimum number of nodes for auto-scaling
        """
        return pulumi.get(self, "min_count")

    @property
    @pulumi.getter(name="orchestratorVersion")
    def orchestrator_version(self) -> Optional[str]:
        """
        Version of orchestrator specified when creating the managed cluster.
        """
        return pulumi.get(self, "orchestrator_version")

    @property
    @pulumi.getter(name="osDiskSizeGB")
    def os_disk_size_gb(self) -> Optional[int]:
        """
        OS Disk Size in GB to be used to specify the disk size for every machine in this master/agent pool. If you specify 0, it will apply the default osDisk size according to the vmSize specified.
        """
        return pulumi.get(self, "os_disk_size_gb")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[str]:
        """
        OsType to be used to specify os type. Choose from Linux and Windows. Default to Linux.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        AgentPoolType represents types of an agent pool
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vnetSubnetID")
    def vnet_subnet_id(self) -> Optional[str]:
        """
        VNet SubnetID specifies the VNet's subnet identifier.
        """
        return pulumi.get(self, "vnet_subnet_id")


@pulumi.output_type
class ManagedClusterServicePrincipalProfileResponse(dict):
    """
    Information about a service principal identity for the cluster to use for manipulating Azure APIs.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "clientId":
            suggest = "client_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ManagedClusterServicePrincipalProfileResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ManagedClusterServicePrincipalProfileResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ManagedClusterServicePrincipalProfileResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 client_id: str,
                 secret: Optional[str] = None):
        """
        Information about a service principal identity for the cluster to use for manipulating Azure APIs.
        :param str client_id: The ID for the service principal.
        :param str secret: The secret password associated with the service principal in plain text.
        """
        pulumi.set(__self__, "client_id", client_id)
        if secret is not None:
            pulumi.set(__self__, "secret", secret)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The ID for the service principal.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter
    def secret(self) -> Optional[str]:
        """
        The secret password associated with the service principal in plain text.
        """
        return pulumi.get(self, "secret")


