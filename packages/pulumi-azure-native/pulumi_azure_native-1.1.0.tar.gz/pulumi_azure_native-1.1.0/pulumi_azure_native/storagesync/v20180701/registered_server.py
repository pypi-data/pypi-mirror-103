# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = ['RegisteredServerArgs', 'RegisteredServer']

@pulumi.input_type
class RegisteredServerArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 storage_sync_service_name: pulumi.Input[str],
                 agent_version: Optional[pulumi.Input[str]] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 last_heart_beat: Optional[pulumi.Input[str]] = None,
                 server_certificate: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 server_os_version: Optional[pulumi.Input[str]] = None,
                 server_role: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a RegisteredServer resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] storage_sync_service_name: Name of Storage Sync Service resource.
        :param pulumi.Input[str] agent_version: Registered Server Agent Version
        :param pulumi.Input[str] cluster_id: Registered Server clusterId
        :param pulumi.Input[str] cluster_name: Registered Server clusterName
        :param pulumi.Input[str] friendly_name: Friendly Name
        :param pulumi.Input[str] last_heart_beat: Registered Server last heart beat
        :param pulumi.Input[str] server_certificate: Registered Server Certificate
        :param pulumi.Input[str] server_id: Registered Server serverId
        :param pulumi.Input[str] server_os_version: Registered Server OS Version
        :param pulumi.Input[str] server_role: Registered Server serverRole
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "storage_sync_service_name", storage_sync_service_name)
        if agent_version is not None:
            pulumi.set(__self__, "agent_version", agent_version)
        if cluster_id is not None:
            pulumi.set(__self__, "cluster_id", cluster_id)
        if cluster_name is not None:
            pulumi.set(__self__, "cluster_name", cluster_name)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if last_heart_beat is not None:
            pulumi.set(__self__, "last_heart_beat", last_heart_beat)
        if server_certificate is not None:
            pulumi.set(__self__, "server_certificate", server_certificate)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if server_os_version is not None:
            pulumi.set(__self__, "server_os_version", server_os_version)
        if server_role is not None:
            pulumi.set(__self__, "server_role", server_role)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="storageSyncServiceName")
    def storage_sync_service_name(self) -> pulumi.Input[str]:
        """
        Name of Storage Sync Service resource.
        """
        return pulumi.get(self, "storage_sync_service_name")

    @storage_sync_service_name.setter
    def storage_sync_service_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_sync_service_name", value)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server Agent Version
        """
        return pulumi.get(self, "agent_version")

    @agent_version.setter
    def agent_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_version", value)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server clusterId
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server clusterName
        """
        return pulumi.get(self, "cluster_name")

    @cluster_name.setter
    def cluster_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_name", value)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly Name
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="lastHeartBeat")
    def last_heart_beat(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server last heart beat
        """
        return pulumi.get(self, "last_heart_beat")

    @last_heart_beat.setter
    def last_heart_beat(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_heart_beat", value)

    @property
    @pulumi.getter(name="serverCertificate")
    def server_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server Certificate
        """
        return pulumi.get(self, "server_certificate")

    @server_certificate.setter
    def server_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_certificate", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server serverId
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter(name="serverOSVersion")
    def server_os_version(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server OS Version
        """
        return pulumi.get(self, "server_os_version")

    @server_os_version.setter
    def server_os_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_os_version", value)

    @property
    @pulumi.getter(name="serverRole")
    def server_role(self) -> Optional[pulumi.Input[str]]:
        """
        Registered Server serverRole
        """
        return pulumi.get(self, "server_role")

    @server_role.setter
    def server_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_role", value)


class RegisteredServer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 last_heart_beat: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_certificate: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 server_os_version: Optional[pulumi.Input[str]] = None,
                 server_role: Optional[pulumi.Input[str]] = None,
                 storage_sync_service_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Registered Server resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] agent_version: Registered Server Agent Version
        :param pulumi.Input[str] cluster_id: Registered Server clusterId
        :param pulumi.Input[str] cluster_name: Registered Server clusterName
        :param pulumi.Input[str] friendly_name: Friendly Name
        :param pulumi.Input[str] last_heart_beat: Registered Server last heart beat
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] server_certificate: Registered Server Certificate
        :param pulumi.Input[str] server_id: Registered Server serverId
        :param pulumi.Input[str] server_os_version: Registered Server OS Version
        :param pulumi.Input[str] server_role: Registered Server serverRole
        :param pulumi.Input[str] storage_sync_service_name: Name of Storage Sync Service resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RegisteredServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Registered Server resource.

        :param str resource_name: The name of the resource.
        :param RegisteredServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RegisteredServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 agent_version: Optional[pulumi.Input[str]] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 cluster_name: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 last_heart_beat: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_certificate: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 server_os_version: Optional[pulumi.Input[str]] = None,
                 server_role: Optional[pulumi.Input[str]] = None,
                 storage_sync_service_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = RegisteredServerArgs.__new__(RegisteredServerArgs)

            __props__.__dict__["agent_version"] = agent_version
            __props__.__dict__["cluster_id"] = cluster_id
            __props__.__dict__["cluster_name"] = cluster_name
            __props__.__dict__["friendly_name"] = friendly_name
            __props__.__dict__["last_heart_beat"] = last_heart_beat
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["server_certificate"] = server_certificate
            __props__.__dict__["server_id"] = server_id
            __props__.__dict__["server_os_version"] = server_os_version
            __props__.__dict__["server_role"] = server_role
            if storage_sync_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'storage_sync_service_name'")
            __props__.__dict__["storage_sync_service_name"] = storage_sync_service_name
            __props__.__dict__["discovery_endpoint_uri"] = None
            __props__.__dict__["last_operation_name"] = None
            __props__.__dict__["last_workflow_id"] = None
            __props__.__dict__["management_endpoint_uri"] = None
            __props__.__dict__["monitoring_configuration"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["resource_location"] = None
            __props__.__dict__["server_managementt_error_code"] = None
            __props__.__dict__["service_location"] = None
            __props__.__dict__["storage_sync_service_uid"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storagesync/v20180701:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20170605preview:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20170605preview:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20180402:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20180402:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20181001:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20181001:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20190201:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190201:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20190301:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190301:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20190601:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20190601:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20191001:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20191001:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20200301:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20200301:RegisteredServer"), pulumi.Alias(type_="azure-native:storagesync/v20200901:RegisteredServer"), pulumi.Alias(type_="azure-nextgen:storagesync/v20200901:RegisteredServer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(RegisteredServer, __self__).__init__(
            'azure-native:storagesync/v20180701:RegisteredServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'RegisteredServer':
        """
        Get an existing RegisteredServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RegisteredServerArgs.__new__(RegisteredServerArgs)

        __props__.__dict__["agent_version"] = None
        __props__.__dict__["cluster_id"] = None
        __props__.__dict__["cluster_name"] = None
        __props__.__dict__["discovery_endpoint_uri"] = None
        __props__.__dict__["friendly_name"] = None
        __props__.__dict__["last_heart_beat"] = None
        __props__.__dict__["last_operation_name"] = None
        __props__.__dict__["last_workflow_id"] = None
        __props__.__dict__["management_endpoint_uri"] = None
        __props__.__dict__["monitoring_configuration"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["resource_location"] = None
        __props__.__dict__["server_certificate"] = None
        __props__.__dict__["server_id"] = None
        __props__.__dict__["server_managementt_error_code"] = None
        __props__.__dict__["server_os_version"] = None
        __props__.__dict__["server_role"] = None
        __props__.__dict__["service_location"] = None
        __props__.__dict__["storage_sync_service_uid"] = None
        __props__.__dict__["type"] = None
        return RegisteredServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server Agent Version
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server clusterId
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="clusterName")
    def cluster_name(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server clusterName
        """
        return pulumi.get(self, "cluster_name")

    @property
    @pulumi.getter(name="discoveryEndpointUri")
    def discovery_endpoint_uri(self) -> pulumi.Output[Optional[str]]:
        """
        Resource discoveryEndpointUri
        """
        return pulumi.get(self, "discovery_endpoint_uri")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Friendly Name
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="lastHeartBeat")
    def last_heart_beat(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server last heart beat
        """
        return pulumi.get(self, "last_heart_beat")

    @property
    @pulumi.getter(name="lastOperationName")
    def last_operation_name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Last Operation Name
        """
        return pulumi.get(self, "last_operation_name")

    @property
    @pulumi.getter(name="lastWorkflowId")
    def last_workflow_id(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server lastWorkflowId
        """
        return pulumi.get(self, "last_workflow_id")

    @property
    @pulumi.getter(name="managementEndpointUri")
    def management_endpoint_uri(self) -> pulumi.Output[Optional[str]]:
        """
        Management Endpoint Uri
        """
        return pulumi.get(self, "management_endpoint_uri")

    @property
    @pulumi.getter(name="monitoringConfiguration")
    def monitoring_configuration(self) -> pulumi.Output[Optional[str]]:
        """
        Monitoring Configuration
        """
        return pulumi.get(self, "monitoring_configuration")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server Provisioning State
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceLocation")
    def resource_location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, "resource_location")

    @property
    @pulumi.getter(name="serverCertificate")
    def server_certificate(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server Certificate
        """
        return pulumi.get(self, "server_certificate")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server serverId
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter(name="serverManagementtErrorCode")
    def server_managementt_error_code(self) -> pulumi.Output[Optional[int]]:
        """
        Registered Server Management Error Code
        """
        return pulumi.get(self, "server_managementt_error_code")

    @property
    @pulumi.getter(name="serverOSVersion")
    def server_os_version(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server OS Version
        """
        return pulumi.get(self, "server_os_version")

    @property
    @pulumi.getter(name="serverRole")
    def server_role(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server serverRole
        """
        return pulumi.get(self, "server_role")

    @property
    @pulumi.getter(name="serviceLocation")
    def service_location(self) -> pulumi.Output[Optional[str]]:
        """
        Service Location
        """
        return pulumi.get(self, "service_location")

    @property
    @pulumi.getter(name="storageSyncServiceUid")
    def storage_sync_service_uid(self) -> pulumi.Output[Optional[str]]:
        """
        Registered Server storageSyncServiceUid
        """
        return pulumi.get(self, "storage_sync_service_uid")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

