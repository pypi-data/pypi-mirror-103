# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetDomainServiceResult',
    'AwaitableGetDomainServiceResult',
    'get_domain_service',
]

@pulumi.output_type
class GetDomainServiceResult:
    """
    Domain service.
    """
    def __init__(__self__, deployment_id=None, domain_configuration_type=None, domain_name=None, domain_security_settings=None, etag=None, filtered_sync=None, id=None, ldaps_settings=None, location=None, migration_properties=None, name=None, notification_settings=None, provisioning_state=None, replica_sets=None, resource_forest_settings=None, sku=None, sync_owner=None, system_data=None, tags=None, tenant_id=None, type=None, version=None):
        if deployment_id and not isinstance(deployment_id, str):
            raise TypeError("Expected argument 'deployment_id' to be a str")
        pulumi.set(__self__, "deployment_id", deployment_id)
        if domain_configuration_type and not isinstance(domain_configuration_type, str):
            raise TypeError("Expected argument 'domain_configuration_type' to be a str")
        pulumi.set(__self__, "domain_configuration_type", domain_configuration_type)
        if domain_name and not isinstance(domain_name, str):
            raise TypeError("Expected argument 'domain_name' to be a str")
        pulumi.set(__self__, "domain_name", domain_name)
        if domain_security_settings and not isinstance(domain_security_settings, dict):
            raise TypeError("Expected argument 'domain_security_settings' to be a dict")
        pulumi.set(__self__, "domain_security_settings", domain_security_settings)
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if filtered_sync and not isinstance(filtered_sync, str):
            raise TypeError("Expected argument 'filtered_sync' to be a str")
        pulumi.set(__self__, "filtered_sync", filtered_sync)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ldaps_settings and not isinstance(ldaps_settings, dict):
            raise TypeError("Expected argument 'ldaps_settings' to be a dict")
        pulumi.set(__self__, "ldaps_settings", ldaps_settings)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if migration_properties and not isinstance(migration_properties, dict):
            raise TypeError("Expected argument 'migration_properties' to be a dict")
        pulumi.set(__self__, "migration_properties", migration_properties)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if notification_settings and not isinstance(notification_settings, dict):
            raise TypeError("Expected argument 'notification_settings' to be a dict")
        pulumi.set(__self__, "notification_settings", notification_settings)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if replica_sets and not isinstance(replica_sets, list):
            raise TypeError("Expected argument 'replica_sets' to be a list")
        pulumi.set(__self__, "replica_sets", replica_sets)
        if resource_forest_settings and not isinstance(resource_forest_settings, dict):
            raise TypeError("Expected argument 'resource_forest_settings' to be a dict")
        pulumi.set(__self__, "resource_forest_settings", resource_forest_settings)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if sync_owner and not isinstance(sync_owner, str):
            raise TypeError("Expected argument 'sync_owner' to be a str")
        pulumi.set(__self__, "sync_owner", sync_owner)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if version and not isinstance(version, int):
            raise TypeError("Expected argument 'version' to be a int")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="deploymentId")
    def deployment_id(self) -> str:
        """
        Deployment Id
        """
        return pulumi.get(self, "deployment_id")

    @property
    @pulumi.getter(name="domainConfigurationType")
    def domain_configuration_type(self) -> Optional[str]:
        """
        Domain Configuration Type
        """
        return pulumi.get(self, "domain_configuration_type")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[str]:
        """
        The name of the Azure domain that the user would like to deploy Domain Services to.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="domainSecuritySettings")
    def domain_security_settings(self) -> Optional['outputs.DomainSecuritySettingsResponse']:
        """
        DomainSecurity Settings
        """
        return pulumi.get(self, "domain_security_settings")

    @property
    @pulumi.getter
    def etag(self) -> Optional[str]:
        """
        Resource etag
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="filteredSync")
    def filtered_sync(self) -> Optional[str]:
        """
        Enabled or Disabled flag to turn on Group-based filtered sync
        """
        return pulumi.get(self, "filtered_sync")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ldapsSettings")
    def ldaps_settings(self) -> Optional['outputs.LdapsSettingsResponse']:
        """
        Secure LDAP Settings
        """
        return pulumi.get(self, "ldaps_settings")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="migrationProperties")
    def migration_properties(self) -> 'outputs.MigrationPropertiesResponse':
        """
        Migration Properties
        """
        return pulumi.get(self, "migration_properties")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notificationSettings")
    def notification_settings(self) -> Optional['outputs.NotificationSettingsResponse']:
        """
        Notification Settings
        """
        return pulumi.get(self, "notification_settings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        the current deployment or provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="replicaSets")
    def replica_sets(self) -> Optional[Sequence['outputs.ReplicaSetResponse']]:
        """
        List of ReplicaSets
        """
        return pulumi.get(self, "replica_sets")

    @property
    @pulumi.getter(name="resourceForestSettings")
    def resource_forest_settings(self) -> Optional['outputs.ResourceForestSettingsResponse']:
        """
        Resource Forest Settings
        """
        return pulumi.get(self, "resource_forest_settings")

    @property
    @pulumi.getter
    def sku(self) -> Optional[str]:
        """
        Sku Type
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="syncOwner")
    def sync_owner(self) -> str:
        """
        SyncOwner ReplicaSet Id
        """
        return pulumi.get(self, "sync_owner")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        The system meta data relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        Azure Active Directory Tenant Id
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> int:
        """
        Data Model Version
        """
        return pulumi.get(self, "version")


class AwaitableGetDomainServiceResult(GetDomainServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDomainServiceResult(
            deployment_id=self.deployment_id,
            domain_configuration_type=self.domain_configuration_type,
            domain_name=self.domain_name,
            domain_security_settings=self.domain_security_settings,
            etag=self.etag,
            filtered_sync=self.filtered_sync,
            id=self.id,
            ldaps_settings=self.ldaps_settings,
            location=self.location,
            migration_properties=self.migration_properties,
            name=self.name,
            notification_settings=self.notification_settings,
            provisioning_state=self.provisioning_state,
            replica_sets=self.replica_sets,
            resource_forest_settings=self.resource_forest_settings,
            sku=self.sku,
            sync_owner=self.sync_owner,
            system_data=self.system_data,
            tags=self.tags,
            tenant_id=self.tenant_id,
            type=self.type,
            version=self.version)


def get_domain_service(domain_service_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDomainServiceResult:
    """
    Domain service.
    API Version: 2021-03-01.


    :param str domain_service_name: The name of the domain service.
    :param str resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
    """
    __args__ = dict()
    __args__['domainServiceName'] = domain_service_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:aad:getDomainService', __args__, opts=opts, typ=GetDomainServiceResult).value

    return AwaitableGetDomainServiceResult(
        deployment_id=__ret__.deployment_id,
        domain_configuration_type=__ret__.domain_configuration_type,
        domain_name=__ret__.domain_name,
        domain_security_settings=__ret__.domain_security_settings,
        etag=__ret__.etag,
        filtered_sync=__ret__.filtered_sync,
        id=__ret__.id,
        ldaps_settings=__ret__.ldaps_settings,
        location=__ret__.location,
        migration_properties=__ret__.migration_properties,
        name=__ret__.name,
        notification_settings=__ret__.notification_settings,
        provisioning_state=__ret__.provisioning_state,
        replica_sets=__ret__.replica_sets,
        resource_forest_settings=__ret__.resource_forest_settings,
        sku=__ret__.sku,
        sync_owner=__ret__.sync_owner,
        system_data=__ret__.system_data,
        tags=__ret__.tags,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type,
        version=__ret__.version)
